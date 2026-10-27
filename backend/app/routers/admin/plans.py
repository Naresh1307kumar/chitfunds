from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta

from app.database import get_db
from app.models.user import User, UserRole
from app.models.chit_plan import ChitPlan, PlanStatus
from app.schemas.plan import ChitPlanCreate, ChitPlanUpdate, ChitPlanResponse
from app.middleware.auth import get_current_user

router = APIRouter(tags=["Admin Chit Plans"])

def check_admin(user: User = Depends(get_current_user)):
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


@router.post("", response_model=ChitPlanResponse, status_code=201)
def create_chit_plan(
    data: ChitPlanCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    # Auto-calculate values
    total_value = data.monthly_amount * data.total_members
    chit_value = total_value
    net_prize = total_value - (total_value * (data.commission_rate / 100))
    end_date = data.start_date + relativedelta(months=data.duration_months)
    
    plan = ChitPlan(
        plan_name=data.plan_name,
        plan_type=data.plan_type,
        chit_type=data.chit_type,
        monthly_amount=data.monthly_amount,
        total_members=data.total_members,
        duration_months=data.duration_months,
        total_value=total_value,
        chit_value=chit_value,
        commission_rate=data.commission_rate,
        net_prize_amount=net_prize,
        start_date=data.start_date,
        end_date=end_date,
        created_by=admin.id
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


@router.get("", response_model=List[ChitPlanResponse])
def get_all_plans(
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    plans = db.query(ChitPlan).filter(ChitPlan.is_deleted == False).all()
    return plans


@router.get("/{plan_id}", response_model=ChitPlanResponse)
def get_plan_details(
    plan_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    plan = db.query(ChitPlan).filter(ChitPlan.id == plan_id, ChitPlan.is_deleted == False).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.put("/{plan_id}", response_model=ChitPlanResponse)
def update_chit_plan(
    plan_id: int,
    data: ChitPlanUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    plan = db.query(ChitPlan).filter(ChitPlan.id == plan_id, ChitPlan.is_deleted == False).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
        
    # Prevent edits if plan has started
    if plan.status != PlanStatus.draft and data.monthly_amount:
        raise HTTPException(status_code=400, detail="Cannot edit financial details of an active/completed plan")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(plan, key, value)
        
    # Re-calculate if necessary
    if "monthly_amount" in update_data or "total_members" in update_data or "commission_rate" in update_data:
        plan.total_value = plan.monthly_amount * plan.total_members
        plan.net_prize_amount = plan.total_value - (plan.total_value * (plan.commission_rate / 100))
    if "start_date" in update_data or "duration_months" in update_data:
        plan.end_date = plan.start_date + relativedelta(months=plan.duration_months)
        
    db.commit()
    db.refresh(plan)
    return plan


@router.delete("/{plan_id}")
def delete_chit_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    plan = db.query(ChitPlan).filter(ChitPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
        
    if plan.status != PlanStatus.draft:
        raise HTTPException(status_code=400, detail="Cannot delete an active or completed plan")
        
    plan.is_deleted = True
    db.commit()
    return {"message": "Plan deleted successfully"}


@router.get("/{plan_id}/members")
def get_plan_members(
    plan_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    from app.models.plan_member import PlanMember
    members = db.query(PlanMember).filter(PlanMember.plan_id == plan_id).all()
    # We should return the member details along with their status
    results = []
    for pm in members:
        user = db.query(User).filter(User.id == pm.user_id).first()
        results.append({
            "plan_member_id": pm.id,
            "user_id": user.id,
            "name": user.name,
            "phone": user.phone,
            "status": "active" if pm.is_active else "pending",
            "joined_at": pm.joined_date,
            "ticket_number": pm.ticket_number,
            "has_won": pm.has_won,
            "reason": getattr(pm, 'reason', 'personal'),
            "priority_score": getattr(pm, 'priority_score', 5)
        })
    return results


from pydantic import BaseModel
class PlanMemberAction(BaseModel):
    action: str  # "approve" or "reject"

@router.post("/{plan_id}/members/{plan_member_id}/action")
def action_plan_member(
    plan_id: int,
    plan_member_id: int,
    data: PlanMemberAction,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    from app.models.plan_member import PlanMember
    
    plan = db.query(ChitPlan).filter(ChitPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
        
    pm = db.query(PlanMember).filter(PlanMember.id == plan_member_id, PlanMember.plan_id == plan_id).first()
    if not pm:
        raise HTTPException(status_code=404, detail="Plan member request not found")

    if data.action == "approve":
        if plan.current_members >= plan.total_members:
            raise HTTPException(status_code=400, detail="Plan is already full")
        pm.is_active = True
        plan.current_members += 1
        pm.ticket_number = f"TCK-{plan.id}-{plan.current_members:02d}"
    elif data.action == "reject":
        db.delete(pm)
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
        
    db.commit()
    return {"message": f"Member {data.action}d successfully"}

@router.post("/{plan_id}/start")
def start_chit_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    plan = db.query(ChitPlan).filter(ChitPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
        
    if plan.status != PlanStatus.draft:
        raise HTTPException(status_code=400, detail="Plan is already active or completed")
        
    if plan.current_members < plan.total_members:
        raise HTTPException(status_code=400, detail="Cannot start plan. It is not full yet.")
        
    plan.status = PlanStatus.active
    
    # Generate Month 1 Installments
    from app.models.plan_member import PlanMember
    from app.models.installment import Installment, InstallmentStatus
    
    active_members = db.query(PlanMember).filter(
        PlanMember.plan_id == plan_id, 
        PlanMember.is_active == True
    ).all()
    
    base_amount = plan.monthly_amount
    
    for pm in active_members:
        ins = Installment(
            plan_member_id=pm.id,
            plan_id=plan.id,
            month_number=1,
            due_date=datetime.now().date(),
            base_amount=base_amount,
            total_amount=base_amount,
            status=InstallmentStatus.pending
        )
        db.add(ins)
        
    db.commit()
    return {"message": "Plan started successfully and Month 1 installments generated."}

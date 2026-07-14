from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User, UserStatus
from app.models.chit_plan import ChitPlan, PlanStatus
from app.models.plan_member import PlanMember
from app.schemas.plan import ChitPlanResponse
from app.middleware.auth import get_current_user

router = APIRouter(tags=["Member Chit Plans"])

def get_active_member(user: User = Depends(get_current_user)):
    if user.status != UserStatus.active:
        raise HTTPException(status_code=403, detail="Only active verified members can access chit plans")
    return user


@router.get("", response_model=List[ChitPlanResponse])
def get_available_plans(
    db: Session = Depends(get_db),
    member: User = Depends(get_active_member)
):
    """List plans that are in draft or active state and not full."""
    plans = db.query(ChitPlan).filter(
        ChitPlan.is_deleted == False,
        ChitPlan.status.in_([PlanStatus.draft, PlanStatus.active]),
        ChitPlan.current_members < ChitPlan.total_members
    ).all()
    return plans


from pydantic import BaseModel
from datetime import datetime

class JoinPlanRequest(BaseModel):
    ticket_count: int = 1

@router.post("/{plan_id}/join")
def join_chit_plan(
    plan_id: int,
    data: JoinPlanRequest,
    db: Session = Depends(get_db),
    member: User = Depends(get_active_member)
):
    """Request to join a chit plan with 1 or more tickets."""
    plan = db.query(ChitPlan).filter(ChitPlan.id == plan_id, ChitPlan.is_deleted == False).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
        
    if plan.current_members + data.ticket_count > plan.total_members:
        available = plan.total_members - plan.current_members
        raise HTTPException(status_code=400, detail=f"Cannot buy {data.ticket_count} tickets. Only {available} spots left in the plan.")

    # Create multiple entries based on ticket_count
    for i in range(data.ticket_count):
        plan_member = PlanMember(
            plan_id=plan_id,
            user_id=member.id,
            is_active=False,
            joined_date=datetime.now().date()
        )
        db.add(plan_member)
        
    db.commit()
    return {"message": f"Successfully requested {data.ticket_count} ticket(s). Waiting for admin approval."}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User, UserStatus
from app.models.chit_plan import ChitPlan, PlanStatus
from app.models.plan_member import PlanMember
from app.models.draw import MonthlyDraw, DrawStatus
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

    joined_plan_ids = set(
        row[0] for row in db.query(PlanMember.plan_id).filter(PlanMember.user_id == member.id).all()
    )

    results = []
    for plan in plans:
        plan_resp = ChitPlanResponse.model_validate(plan)
        plan_resp.has_joined = plan.id in joined_plan_ids
        results.append(plan_resp)

    return results


from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JoinPlanRequest(BaseModel):
    ticket_count: Optional[int] = 1
    reason: Optional[str] = "personal"

@router.post("/{plan_id}/join")
def join_chit_plan(
    plan_id: int,
    data: JoinPlanRequest,
    db: Session = Depends(get_db),
    member: User = Depends(get_active_member)
):
    """Request to join a chit plan. Each user can join a plan only once."""
    plan = db.query(ChitPlan).filter(ChitPlan.id == plan_id, ChitPlan.is_deleted == False).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # Check if user has already joined this plan
    existing_member = db.query(PlanMember).filter(
        PlanMember.plan_id == plan_id,
        PlanMember.user_id == member.id
    ).first()

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="You have already joined this plan. Each user can join a plan only once."
        )

    if plan.current_members >= plan.total_members:
        raise HTTPException(status_code=400, detail="Plan is already full. No spots left.")

    # Determine priority score
    reason_lower = (data.reason or "personal").lower()
    priority_map = {
        "hospital": 1,
        "medical": 1,
        "education": 2,
        "studies": 2,
        "marriage": 3,
        "wedding": 3,
        "business": 4,
        "personal": 5
    }
    score = priority_map.get(reason_lower, 5)

    plan_member = PlanMember(
        plan_id=plan_id,
        user_id=member.id,
        is_active=False,
        joined_date=datetime.now().date(),
        reason=reason_lower,
        priority_score=score
    )
    db.add(plan_member)
    db.commit()
    return {"message": f"Successfully requested to join plan with reason '{reason_lower}'. Waiting for admin approval."}


@router.get("/my")
def get_my_plans(
    db: Session = Depends(get_db),
    member: User = Depends(get_active_member)
):
    """List all chit plans joined by current user along with ticket numbers and monthly draw winner history."""
    my_memberships = db.query(PlanMember).filter(
        PlanMember.user_id == member.id
    ).all()

    plan_ids = list(set([m.plan_id for m in my_memberships]))
    plans = db.query(ChitPlan).filter(ChitPlan.id.in_(plan_ids)).all()

    results = []
    for plan in plans:
        user_tickets = [m for m in my_memberships if m.plan_id == plan.id]
        
        # Get winners history for this plan
        draws = db.query(MonthlyDraw).filter(
            MonthlyDraw.plan_id == plan.id,
            MonthlyDraw.status == DrawStatus.completed
        ).order_by(MonthlyDraw.month_number).all()

        # Build full Month-by-Month timeline from Month 1 to duration_months
        draws_dict = {d.month_number: d for d in draws}
        full_schedule = []

        start_dt = plan.start_date or datetime.now().date()
        for m_num in range(1, plan.duration_months + 1):
            if m_num in draws_dict:
                d = draws_dict[m_num]
                w_user = db.query(User).filter(User.id == d.winner_id).first() if d.winner_id else None
                w_ticket = db.query(PlanMember).filter(PlanMember.id == d.winning_ticket_id).first() if d.winning_ticket_id else None
                full_schedule.append({
                    "month_number": m_num,
                    "status": "completed",
                    "draw_date": str(d.draw_date),
                    "winner_name": w_user.name if w_user else "N/A",
                    "ticket_number": w_ticket.ticket_number if w_ticket else "N/A",
                    "prize_amount": d.prize_amount,
                    "reason": getattr(w_ticket, 'reason', 'personal') if w_ticket else "N/A"
                })
            else:
                # Estimate future month draw date
                future_month = (start_dt.month + m_num - 2) % 12 + 1
                future_year = start_dt.year + (start_dt.month + m_num - 2) // 12
                proj_date = f"{future_year}-{future_month:02d}-01"
                full_schedule.append({
                    "month_number": m_num,
                    "status": "upcoming",
                    "draw_date": proj_date,
                    "winner_name": "Scheduled Draw",
                    "ticket_number": "Pending",
                    "prize_amount": plan.net_prize_amount,
                    "reason": "Upcoming"
                })

        results.append({
            "plan_id": plan.id,
            "plan_name": plan.plan_name,
            "plan_type": plan.plan_type.value if hasattr(plan.plan_type, 'value') else str(plan.plan_type),
            "chit_type": plan.chit_type,
            "monthly_amount": plan.monthly_amount,
            "total_value": plan.total_value,
            "duration_months": plan.duration_months,
            "current_members": plan.current_members,
            "total_members": plan.total_members,
            "status": plan.status.value if hasattr(plan.status, 'value') else str(plan.status),
            "tickets": [{
                "ticket_id": t.id,
                "ticket_number": t.ticket_number,
                "has_won": t.has_won,
                "is_active": t.is_active,
                "reason": getattr(t, 'reason', 'personal')
            } for t in user_tickets],
            "winners": full_schedule
        })

    return results


@router.get("/{plan_id}/winners")
def get_plan_winners(
    plan_id: int,
    db: Session = Depends(get_db),
    member: User = Depends(get_active_member)
):
    """Get full month-by-month draw schedule and winners list for a specific plan."""
    plan = db.query(ChitPlan).filter(ChitPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    draws = db.query(MonthlyDraw).filter(
        MonthlyDraw.plan_id == plan_id,
        MonthlyDraw.status == DrawStatus.completed
    ).order_by(MonthlyDraw.month_number).all()

    draws_dict = {d.month_number: d for d in draws}
    full_schedule = []

    start_dt = plan.start_date or datetime.now().date()
    for m_num in range(1, plan.duration_months + 1):
        if m_num in draws_dict:
            d = draws_dict[m_num]
            w_user = db.query(User).filter(User.id == d.winner_id).first() if d.winner_id else None
            w_ticket = db.query(PlanMember).filter(PlanMember.id == d.winning_ticket_id).first() if d.winning_ticket_id else None
            full_schedule.append({
                "month_number": m_num,
                "status": "completed",
                "draw_date": str(d.draw_date),
                "winner_name": w_user.name if w_user else "N/A",
                "ticket_number": w_ticket.ticket_number if w_ticket else "N/A",
                "prize_amount": d.prize_amount,
                "reason": getattr(w_ticket, 'reason', 'personal') if w_ticket else "N/A"
            })
        else:
            future_month = (start_dt.month + m_num - 2) % 12 + 1
            future_year = start_dt.year + (start_dt.month + m_num - 2) // 12
            proj_date = f"{future_year}-{future_month:02d}-01"
            full_schedule.append({
                "month_number": m_num,
                "status": "upcoming",
                "draw_date": proj_date,
                "winner_name": "Scheduled Draw",
                "ticket_number": "Pending",
                "prize_amount": plan.net_prize_amount,
                "reason": "Upcoming"
            })

    return full_schedule



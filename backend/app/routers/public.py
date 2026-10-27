from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User, UserRole
from app.models.chit_plan import ChitPlan, PlanStatus
from app.schemas.plan import ChitPlanResponse

router = APIRouter(prefix="/api/v1/public", tags=["Public Data"])

@router.get("/stats")
def get_public_stats(db: Session = Depends(get_db)):
    total_members = db.query(User).filter(User.role == UserRole.member, User.is_deleted == False).count()
    total_plans = db.query(ChitPlan).filter(ChitPlan.is_deleted == False).count()
    
    return {
        "active_customers": total_members,
        "successful_plans": total_plans
    }

@router.get("/plans", response_model=List[ChitPlanResponse])
def get_public_plans(db: Session = Depends(get_db)):
    """List plans that are public/active and not deleted."""
    plans = db.query(ChitPlan).filter(
        ChitPlan.is_deleted == False,
        ChitPlan.status.in_([PlanStatus.draft, PlanStatus.active])
    ).all()
    return plans


@router.get("/winners")
def get_public_winners(db: Session = Depends(get_db)):
    """List recent completed monthly draw winners across all schemes."""
    from app.models.draw import MonthlyDraw, DrawStatus
    from app.models.plan_member import PlanMember

    draws = db.query(MonthlyDraw).filter(
        MonthlyDraw.status == DrawStatus.completed
    ).order_by(MonthlyDraw.created_at.desc()).limit(20).all()

    results = []
    for d in draws:
        plan = db.query(ChitPlan).filter(ChitPlan.id == d.plan_id).first()
        user = db.query(User).filter(User.id == d.winner_id).first()
        ticket = db.query(PlanMember).filter(PlanMember.id == d.winning_ticket_id).first()

        results.append({
            "id": d.id,
            "plan_name": plan.plan_name if plan else "Chit Plan",
            "month_number": d.month_number,
            "draw_date": str(d.draw_date),
            "winner_name": user.name if user else "Member",
            "ticket_number": ticket.ticket_number if ticket else "N/A",
            "prize_amount": d.prize_amount,
            "reason": getattr(ticket, 'reason', 'personal') if ticket else "personal"
        })

    return results


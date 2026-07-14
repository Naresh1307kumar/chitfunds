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

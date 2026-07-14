from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import Dict, Any, List

from app.database import get_db
from app.models.user import User, UserRole, UserStatus, KYCStatus
from app.models.chit_plan import ChitPlan, PlanStatus
from app.models.draw import MonthlyDraw
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/admin/dashboard", tags=["Admin Dashboard"])

def check_admin(user: User = Depends(get_current_user)):
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    # Total members (exclude soft-deleted)
    total_members = db.query(User).filter(User.role == UserRole.member, User.is_deleted == False).count()
    
    # Active plans
    active_plans = db.query(ChitPlan).filter(ChitPlan.status == PlanStatus.active, ChitPlan.is_deleted == False).count()
    
    # Expected monthly collection
    active_plans_list = db.query(ChitPlan).filter(ChitPlan.status == PlanStatus.active, ChitPlan.is_deleted == False).all()
    monthly_collection = sum([plan.monthly_amount * plan.total_members for plan in active_plans_list])
    
    # Pending Draws
    pending_draws = active_plans
    
    # Pending approvals (members with status 'pending', not deleted)
    pending_approvals = db.query(User).filter(
        User.role == UserRole.member, 
        User.status == UserStatus.pending,
        User.is_deleted == False
    ).count()

    return {
        "total_members": total_members,
        "active_plans": active_plans,
        "monthly_collection": monthly_collection,
        "pending_draws": pending_draws,
        "pending_approvals": pending_approvals
    }


@router.get("/pending-actions")
def get_pending_actions(
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    actions = []

    # 1. Pending KYC applications (not deleted)
    pending_kyc = db.query(User).filter(
        User.role == UserRole.member,
        User.kyc_status == KYCStatus.pending,
        User.is_deleted == False
    ).count()
    if pending_kyc > 0:
        actions.append({
            "id": "kyc",
            "text": f"Review {pending_kyc} pending KYC application{'s' if pending_kyc != 1 else ''}.",
            "type": "kyc",
            "count": pending_kyc,
            "priority": "High Priority"
        })

    # 2. Pending member approvals (not deleted)
    pending_members = db.query(User).filter(
        User.role == UserRole.member,
        User.status == UserStatus.pending,
        User.is_deleted == False
    ).count()
    if pending_members > 0:
        actions.append({
            "id": "approval",
            "text": f"Approve {pending_members} pending member registration{'s' if pending_members != 1 else ''}.",
            "type": "members",
            "count": pending_members,
            "priority": "High Priority"
        })

    # 3. Active plans needing draws
    active_plan_list = db.query(ChitPlan).filter(
        ChitPlan.status == PlanStatus.active,
        ChitPlan.is_deleted == False
    ).all()
    for plan in active_plan_list:
        actions.append({
            "id": f"draw_{plan.id}",
            "text": f"Conduct draw for plan \"{plan.plan_name}\".",
            "type": "draw",
            "count": 1,
            "priority": "High Priority"
        })

    # 4. Pending installment payments awaiting verification
    try:
        from app.models.installment import Installment, InstallmentStatus
        pending_payments = db.query(Installment).filter(
            Installment.status == InstallmentStatus.paid
        ).count()
        if pending_payments > 0:
            actions.append({
                "id": "payments",
                "text": f"Verify {pending_payments} pending installment payment{'s' if pending_payments != 1 else ''}.",
                "type": "payment",
                "count": pending_payments,
                "priority": "High Priority"
            })
    except Exception:
        pass

    return actions

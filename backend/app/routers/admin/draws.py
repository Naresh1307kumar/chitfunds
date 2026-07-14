from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func as sql_func
from typing import List
from datetime import datetime

from app.database import get_db
from app.models.user import User, UserRole
from app.models.chit_plan import ChitPlan, PlanStatus
from app.models.plan_member import PlanMember
from app.models.draw import MonthlyDraw, DrawStatus
from app.middleware.auth import get_current_user
from app.services.notification_service import send_winner_notifications

router = APIRouter(prefix="/api/v1/admin/draws", tags=["Admin Draws"])

def check_admin(user: User = Depends(get_current_user)):
    if user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


@router.post("/{plan_id}/conduct")
def conduct_monthly_draw(
    plan_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    plan = db.query(ChitPlan).filter(ChitPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
        
    if plan.status != PlanStatus.active:
        raise HTTPException(status_code=400, detail=f"Cannot conduct draw. Plan is {plan.status.value}")

    # Calculate current month number based on previous draws
    completed_draws = db.query(MonthlyDraw).filter(MonthlyDraw.plan_id == plan_id).order_by(MonthlyDraw.draw_date.desc()).all()
    if len(completed_draws) >= plan.duration_months:
        plan.status = PlanStatus.completed
        db.commit()
        raise HTTPException(status_code=400, detail="All draws for this plan are completed")
        
    if completed_draws:
        last_draw = completed_draws[0]
        now = datetime.utcnow()
        if last_draw.draw_date.month == now.month and last_draw.draw_date.year == now.year:
            raise HTTPException(status_code=400, detail="A draw has already been conducted this month for this plan.")
            
    month_number = len(completed_draws) + 1
    
    # Pick a random winner from active tickets that haven't won
    winning_ticket = db.query(PlanMember).filter(
        PlanMember.plan_id == plan_id,
        PlanMember.is_active == True,
        PlanMember.has_won == False
    ).order_by(sql_func.random()).first()

    if not winning_ticket:
        raise HTTPException(status_code=400, detail="No eligible tickets found for the draw")

    # Mark ticket as won
    winning_ticket.has_won = True
    
    # Calculate amounts
    total_pool = plan.total_value
    commission_amt = total_pool * (plan.commission_rate / 100)
    prize = total_pool - commission_amt

    # Create draw record
    draw = MonthlyDraw(
        plan_id=plan_id,
        month_number=month_number,
        draw_date=datetime.now().date(),
        total_chit_value=total_pool,
        admin_commission=commission_amt,
        prize_amount=prize,
        winning_ticket_id=winning_ticket.id,
        winner_id=winning_ticket.user_id,
        status=DrawStatus.completed,
        conducted_by=admin.id
    )
    db.add(draw)
    
    # If this was the last draw, complete the plan
    if month_number == plan.duration_months:
        plan.status = PlanStatus.completed
    else:
        # Generate next month's installments
        from app.models.installment import Installment, InstallmentStatus
        from datetime import timedelta
        base_amount = plan.total_value / plan.duration_months
        active_members = db.query(PlanMember).filter(
            PlanMember.plan_id == plan_id, 
            PlanMember.is_active == True
        ).all()
        for pm in active_members:
            ins = Installment(
                plan_member_id=pm.id,
                plan_id=plan.id,
                month_number=month_number + 1,
                due_date=datetime.now().date() + timedelta(days=5),
                base_amount=base_amount,
                total_amount=base_amount,
                status=InstallmentStatus.pending
            )
            db.add(ins)
            
    db.commit()
    
    # Fetch winner details for response
    winner_user = db.query(User).filter(User.id == winning_ticket.user_id).first()
    
    # Trigger notifications asynchronously
    background_tasks.add_task(
        send_winner_notifications,
        user_name=winner_user.name,
        user_email=winner_user.email,
        user_phone=winner_user.phone,
        plan_name=plan.plan_name,
        prize_amount=prize,
        ticket_number=winning_ticket.ticket_number,
        month=month_number
    )
    
    return {
        "message": "Draw conducted successfully",
        "month_number": month_number,
        "winner_name": winner_user.name,
        "ticket_number": winning_ticket.ticket_number,
        "prize_amount": prize
    }


@router.get("/{plan_id}")
def get_plan_draws(
    plan_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    draws = db.query(MonthlyDraw).filter(MonthlyDraw.plan_id == plan_id).order_by(MonthlyDraw.month_number).all()
    results = []
    for d in draws:
        ticket = db.query(PlanMember).filter(PlanMember.id == d.winning_ticket_id).first()
        user = db.query(User).filter(User.id == d.winner_id).first()
        results.append({
            "id": d.id,
            "month_number": d.month_number,
            "draw_date": d.draw_date,
            "prize_amount": d.prize_amount,
            "admin_commission": d.admin_commission,
            "ticket_number": ticket.ticket_number if ticket else None,
            "winner_name": user.name if user else None,
            "status": d.status.value
        })
    return results

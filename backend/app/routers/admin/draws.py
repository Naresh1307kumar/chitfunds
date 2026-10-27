from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func as sql_func
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

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

class ConductDrawRequest(BaseModel):
    winner_ticket_id: Optional[int] = None
    winning_bid_amount: Optional[float] = None

@router.post("/{plan_id}/conduct")
def conduct_monthly_draw(
    plan_id: int,
    background_tasks: BackgroundTasks,
    data: Optional[ConductDrawRequest] = None,
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
    
    # Pick winning ticket
    if getattr(plan, 'chit_type', 'lucky_draw') == 'auction':
        if not data or not data.winner_ticket_id:
            raise HTTPException(status_code=400, detail="Winner ticket is required for auction chits")
        
        winning_ticket = db.query(PlanMember).filter(
            PlanMember.id == data.winner_ticket_id,
            PlanMember.plan_id == plan_id,
            PlanMember.is_active == True,
            PlanMember.has_won == False
        ).first()
        
        if not winning_ticket:
            raise HTTPException(status_code=400, detail="Selected ticket is invalid or has already won")
            
        winning_bid = data.winning_bid_amount or 0.0
    else:
        # Pick a random winner from active tickets that haven't won
        winning_ticket = db.query(PlanMember).filter(
            PlanMember.plan_id == plan_id,
            PlanMember.is_active == True,
            PlanMember.has_won == False
        ).order_by(sql_func.random()).first()

        if not winning_ticket:
            raise HTTPException(status_code=400, detail="No eligible tickets found for the draw")
            
        winning_bid = 0.0

    # Mark ticket as won
    winning_ticket.has_won = True
    
    # Calculate amounts using real chit fund auction formula
    from app.services.chit_calculator import calculate_auction_draw, calculate_last_month_draw
    
    chit_pool_value = plan.chit_value or (plan.monthly_amount * plan.total_members)
    
    # If last month, full chit_value
    if month_number == plan.duration_months or winning_bid >= chit_pool_value:
        calc_result = calculate_last_month_draw(chit_pool_value, plan.monthly_amount)
    else:
        calc_result = calculate_auction_draw(
            chit_value=chit_pool_value,
            monthly_amount=plan.monthly_amount,
            total_members=plan.total_members,
            commission_rate=plan.commission_rate,
            winning_bid_amount=winning_bid
        )

    # Create draw record with full auction breakdown
    draw = MonthlyDraw(
        plan_id=plan_id,
        month_number=month_number,
        draw_date=datetime.now().date(),
        chit_value=calc_result["chit_value"],
        winning_bid_amount=calc_result["winning_bid_amount"],
        discount=calc_result["discount"],
        company_commission=calc_result["company_commission"],
        net_discount=calc_result["net_discount"],
        dividend_per_member=calc_result["dividend_per_member"],
        net_payable=calc_result["net_payable"],
        prize_amount=calc_result["winner_receives"],
        total_chit_value=calc_result["chit_value"],
        admin_commission=calc_result["company_commission"],
        winning_ticket_id=winning_ticket.id,
        winner_id=winning_ticket.user_id,
        status=DrawStatus.completed,
        conducted_by=admin.id,
        notes=f"Winning Bid: Rs.{calc_result['winning_bid_amount']} | Discount: Rs.{calc_result['discount']} | Dividend: Rs.{calc_result['dividend_per_member']}"
    )
    db.add(draw)

    # Auto-generate Promissory Note for the winning member conditionally
    try:
        from app.models.promissory_note import PromissoryNote, PronoteStatus
        from app.models.installment import Installment, InstallmentStatus
        from sqlalchemy.sql.expression import func
        from datetime import date, timedelta

        # Calculate how much the user has spent (paid) so far
        amount_spent = db.query(func.sum(Installment.total_amount)).filter(
            Installment.plan_member_id == winning_ticket.id,
            Installment.status.in_([InstallmentStatus.paid, InstallmentStatus.verified])
        ).scalar() or 0.0

        if calc_result["winner_receives"] > amount_spent:
            pronote_count = db.query(PromissoryNote).count()
            auto_prn_id = f"PRN-{datetime.now().year}-{(pronote_count + 1):04d}"

            winner_pronote = PromissoryNote(
                pronote_id=auto_prn_id,
                member_id=winning_ticket.user_id,
                chit_id=plan_id,
                loan_amount=calc_result["winner_receives"],
                issue_date=date.today(),
                due_date=date.today() + timedelta(days=365),
                interest_rate=0.0,
                repayment_amount=calc_result["winner_receives"],
                purpose=f"Security Undertaking for Month {month_number} Draw ({plan.plan_name})",
                status=PronoteStatus.pending_signature,
                signature=None
            )
            db.add(winner_pronote)
        else:
            print(f"Skipping pronote: winner received {calc_result['winner_receives']} <= spent amount {amount_spent}")
    except Exception as e:
        print("Failed to auto-generate winner pronote:", e)
    
    # If this was the last draw, complete the plan
    if month_number == plan.duration_months:
        plan.status = PlanStatus.completed
    else:
        # Generate next month's installments using calculated net_payable
        from app.models.installment import Installment, InstallmentStatus
        from datetime import timedelta
        base_amount = plan.monthly_amount
        total_amount = calc_result["net_payable"]
        
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
                total_amount=total_amount,
                status=InstallmentStatus.pending
            )
            db.add(ins)
            
    db.commit()
    
    # Fetch winner details for response
    winner_user = db.query(User).filter(User.id == winning_ticket.user_id).first()
    
    # Trigger notifications asynchronously
    from app.services.notification_service import send_winner_notifications, send_draw_announcement_to_all_members
    background_tasks.add_task(
        send_winner_notifications,
        user_name=winner_user.name,
        user_email=winner_user.email,
        user_phone=winner_user.phone,
        plan_name=plan.plan_name,
        prize_amount=calc_result["winner_receives"],
        ticket_number=winning_ticket.ticket_number,
        month=month_number
    )
    background_tasks.add_task(
        send_draw_announcement_to_all_members,
        plan_id=plan_id,
        plan_name=plan.plan_name,
        winner_name=winner_user.name,
        ticket_number=winning_ticket.ticket_number,
        prize_amount=calc_result["winner_receives"],
        month_number=month_number
    )
    
    return {
        "message": "Draw conducted successfully",
        "month_number": month_number,
        "winner_name": winner_user.name,
        "ticket_number": winning_ticket.ticket_number,
        "prize_amount": calc_result["winner_receives"],
        "chit_value": calc_result["chit_value"],
        "winning_bid_amount": calc_result["winning_bid_amount"],
        "discount": calc_result["discount"],
        "company_commission": calc_result["company_commission"],
        "dividend_per_member": calc_result["dividend_per_member"],
        "net_payable_next_month": calc_result["net_payable"]
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
            "status": d.status.value,
            "notes": d.notes
        })
    return results


@router.get("/{plan_id}/ai-recommend")
def get_ai_recommended_winner(
    plan_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """AI Engine endpoint to compute smart winner allocation based on emergency urgency and credit standing."""
    eligible_members = db.query(PlanMember).filter(
        PlanMember.plan_id == plan_id,
        PlanMember.has_won == False
    ).all()

    if not eligible_members:
        raise HTTPException(status_code=400, detail="No eligible members remaining for this plan")

    scored_candidates = []
    reason_weights = {
        "hospital": 100,
        "medical": 100,
        "education": 80,
        "studies": 80,
        "marriage": 60,
        "wedding": 60,
        "business": 40,
        "personal": 20
    }

    for m in eligible_members:
        user = db.query(User).filter(User.id == m.user_id).first()
        reason = getattr(m, 'reason', 'personal') or 'personal'
        prio_score = getattr(m, 'priority_score', 5) or 5
        
        base_urgency = reason_weights.get(reason.lower(), 20)
        rank_bonus = (6 - prio_score) * 15
        total_ai_score = base_urgency + rank_bonus + 20  # +20 active standing bonus

        explanation = f"AI Score {total_ai_score} pts • Selected due to high emergency urgency ({reason.upper()}) & rank #{prio_score}"

        scored_candidates.append({
            "ticket_id": m.id,
            "ticket_number": m.ticket_number,
            "user_name": user.name if user else "Member",
            "reason": reason,
            "priority_score": prio_score,
            "ai_score": total_ai_score,
            "ai_explanation": explanation
        })

    # Sort candidates by AI score descending
    scored_candidates.sort(key=lambda x: x["ai_score"], reverse=True)
    top_recommendation = scored_candidates[0]

    return {
        "recommended_winner": top_recommendation,
        "all_ranked_candidates": scored_candidates
    }


import sys
import os
from datetime import datetime, date, timedelta
from dotenv import load_dotenv

load_dotenv('c:/chit fund/backend/.env')

# Add backend directory to sys.path so app imports work
sys.path.insert(0, 'c:/chit fund/backend')

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.models.chit_plan import ChitPlan, PlanStatus
from app.models.plan_member import PlanMember
from app.models.draw import MonthlyDraw, DrawStatus
from app.models.promissory_note import PromissoryNote, PronoteStatus
from app.services.chit_calculator import calculate_auction_draw, calculate_last_month_draw

db = SessionLocal()

try:
    print("--- 1. Locating Ramesh & Plan 31 ---")
    ramesh = db.query(User).filter(User.id == 29).first()
    plan = db.query(ChitPlan).filter(ChitPlan.id == 31).first()
    ticket = db.query(PlanMember).filter(PlanMember.id == 44).first()

    print(f"User: {ramesh.name} (ID: {ramesh.id})")
    print(f"Plan: {plan.plan_name} (ID: {plan.id})")
    print(f"Ticket: {ticket.ticket_number} (ID: {ticket.id}, Has Won: {ticket.has_won})")

    # Ensure ticket belongs to Ramesh & Plan 31
    if ticket.user_id != ramesh.id or ticket.plan_id != plan.id:
        raise Exception("Ticket mismatch!")

    # Conduct draw
    completed_draws = db.query(MonthlyDraw).filter(MonthlyDraw.plan_id == plan.id).order_by(MonthlyDraw.draw_date.desc()).all()
    month_number = len(completed_draws) + 1
    winning_bid = 5000.0  # Sample winning bid for auction chit

    ticket.has_won = True
    chit_pool_value = plan.chit_value or (plan.monthly_amount * plan.total_members)

    calc_result = calculate_auction_draw(
        chit_value=chit_pool_value,
        monthly_amount=plan.monthly_amount,
        total_members=plan.total_members,
        commission_rate=plan.commission_rate or 5.0,
        winning_bid_amount=winning_bid
    )

    admin_user = db.query(User).filter(User.role == UserRole.admin).first()
    admin_id = admin_user.id if admin_user else ramesh.id

    draw = MonthlyDraw(
        plan_id=plan.id,
        month_number=month_number,
        draw_date=date.today(),
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
        winning_ticket_id=ticket.id,
        winner_id=ramesh.id,
        status=DrawStatus.completed,
        conducted_by=admin_id,
        notes=f"Winner: {ramesh.name} | Winning Bid: Rs.{calc_result['winning_bid_amount']} | Prize: Rs.{calc_result['winner_receives']}"
    )
    db.add(draw)
    db.flush()

    print(f"\n--- 2. Monthly Draw #{month_number} Created ---")
    print(f"Winner Prize Amount: Rs. {calc_result['winner_receives']}")

    # Promissory Note creation & signature submission
    pronote_count = db.query(PromissoryNote).count()
    auto_prn_id = f"PRN-{datetime.now().year}-{(pronote_count + 1):04d}"

    # Sample base64 signature string representing Ramesh's submitted signature
    sample_signature = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAPAAAABkCAYAAAC6mg3AAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAA_SURBVHhe7d0BjgM"

    pronote = PromissoryNote(
        pronote_id=auto_prn_id,
        member_id=ramesh.id,
        chit_id=plan.id,
        loan_amount=calc_result["winner_receives"],
        issue_date=date.today(),
        due_date=date.today() + timedelta(days=365),
        interest_rate=0.0,
        repayment_amount=calc_result["winner_receives"],
        purpose=f"Security Undertaking for Month {month_number} Draw ({plan.plan_name})",
        status=PronoteStatus.active,  # Signed & Active / Submitted
        signature=sample_signature
    )
    db.add(pronote)

    db.commit()
    print(f"\n--- 3. Promissory Note Created & Submitted ---")
    print(f"Pronote ID: {pronote.pronote_id}")
    print(f"Member Name: {ramesh.name}")
    print(f"Status: {pronote.status.value}")
    print(f"Loan/Prize Amount: Rs. {pronote.loan_amount}")
    print("SUCCESS!")

except Exception as e:
    db.rollback()
    print("ERROR:", e)
finally:
    db.close()

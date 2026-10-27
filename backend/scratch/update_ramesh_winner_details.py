import sys
import os
from datetime import datetime, date, timedelta
from dotenv import load_dotenv

load_dotenv('c:/chit fund/backend/.env')
sys.path.insert(0, 'c:/chit fund/backend')

from app.database import SessionLocal
from app.models.user import User
from app.models.chit_plan import ChitPlan
from app.models.plan_member import PlanMember
from app.models.draw import MonthlyDraw
from app.models.promissory_note import PromissoryNote, PronoteStatus
from app.services.chit_calculator import calculate_auction_draw

db = SessionLocal()

try:
    ramesh = db.query(User).filter(User.id == 29).first()
    plan = db.query(ChitPlan).filter(ChitPlan.id == 31).first()
    ticket = db.query(PlanMember).filter(PlanMember.id == 44).first()

    winning_bid = 36000.0  # Winning bid of ₹36,000 out of ₹40,000 chit value
    chit_pool_value = plan.chit_value or (plan.monthly_amount * plan.total_members)

    calc_result = calculate_auction_draw(
        chit_value=chit_pool_value,
        monthly_amount=plan.monthly_amount,
        total_members=plan.total_members,
        commission_rate=plan.commission_rate or 5.0,
        winning_bid_amount=winning_bid
    )

    draw = db.query(MonthlyDraw).filter(MonthlyDraw.plan_id == plan.id, MonthlyDraw.winner_id == ramesh.id).first()
    if draw:
        draw.chit_value = calc_result["chit_value"]
        draw.winning_bid_amount = calc_result["winning_bid_amount"]
        draw.discount = calc_result["discount"]
        draw.company_commission = calc_result["company_commission"]
        draw.net_discount = calc_result["net_discount"]
        draw.dividend_per_member = calc_result["dividend_per_member"]
        draw.net_payable = calc_result["net_payable"]
        draw.prize_amount = calc_result["winner_receives"]
        draw.total_chit_value = calc_result["chit_value"]
        draw.admin_commission = calc_result["company_commission"]
        draw.notes = f"Winning Bid: Rs.{calc_result['winning_bid_amount']} | Discount: Rs.{calc_result['discount']} | Dividend: Rs.{calc_result['dividend_per_member']}"

    pronote = db.query(PromissoryNote).filter(PromissoryNote.member_id == ramesh.id, PromissoryNote.chit_id == plan.id).first()
    if pronote:
        pronote.loan_amount = calc_result["winner_receives"]
        pronote.repayment_amount = calc_result["winner_receives"]

    db.commit()

    print("UPDATED SUCCESSFULLY!")
    print(f"Winner: {ramesh.name}")
    print(f"Chit Plan: {plan.plan_name}")
    print(f"Ticket: {ticket.ticket_number}")
    print(f"Prize Amount: ₹{calc_result['winner_receives']:,.2f}")
    print(f"Dividend / Member: ₹{calc_result['dividend_per_member']:,.2f}")
    print(f"Pronote ID: {pronote.pronote_id}")
    print(f"Pronote Status: {pronote.status.value}")

except Exception as e:
    db.rollback()
    print("ERROR:", e)
finally:
    db.close()

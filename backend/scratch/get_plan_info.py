import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from app.database import SessionLocal
from app.models.plan_member import PlanMember
from app.models.installment import Installment
from app.models.chit_plan import ChitPlan

db = SessionLocal()
plan = db.query(ChitPlan).filter(ChitPlan.id == 31).first()
print(f"Plan ID {plan.id}, total_members={plan.total_members}, current={plan.current_members}")

members = db.query(PlanMember).filter(PlanMember.plan_id == 31).all()
print(f"Members count: {len(members)}")
for m in members:
    insts = db.query(Installment).filter(Installment.plan_member_id == m.id).all()
    print(f"Member ID {m.user_id}, ticket={m.ticket_number}, installments={len(insts)}")

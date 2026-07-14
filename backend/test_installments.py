import sys, os, datetime
sys.path.append(os.path.abspath('.'))
from app.database import SessionLocal
from app.models.chit_plan import ChitPlan
from app.models.plan_member import PlanMember
from app.models.installment import Installment, InstallmentStatus

db = SessionLocal()
plan = db.query(ChitPlan).filter(ChitPlan.id == 7).first()
pms = db.query(PlanMember).filter(PlanMember.plan_id == 7).all()
base_amt = plan.total_value / plan.duration_months

for pm in pms:
    ins = Installment(
        plan_member_id=pm.id, 
        plan_id=7, 
        month_number=1, 
        due_date=datetime.date.today(), 
        base_amount=base_amt, 
        total_amount=base_amt, 
        status=InstallmentStatus.verified, 
        paid_date=datetime.date.today(), 
        payment_method='cash', 
        receipt_number=f'REC-7-{pm.id}-1', 
        verified_by=13, 
        verified_at=datetime.datetime.utcnow()
    )
    db.add(ins)
db.commit()
print('Success')

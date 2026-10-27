import sys
import os
from datetime import datetime, date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.models.chit_plan import ChitPlan
from app.models.plan_member import PlanMember
from app.models.installment import Installment, InstallmentStatus

def generate_active_dues():
    db = SessionLocal()
    try:
        # Get plan
        plan = db.query(ChitPlan).filter(ChitPlan.is_deleted == False).first()
        if not plan:
            print("[ERROR] No active chit plan found!")
            return

        users = db.query(User).filter(User.username.in_(["ramesh", "vikram2026"])).all()
        for idx, u in enumerate(users, 1):
            # Check if membership exists
            pm = db.query(PlanMember).filter(PlanMember.user_id == u.id, PlanMember.plan_id == plan.id).first()
            if not pm:
                pm = PlanMember(
                    plan_id=plan.id,
                    user_id=u.id,
                    is_active=True,
                    ticket_number=f"TCK-{plan.id}-{idx:02d}",
                    joined_date=date.today(),
                    reason="personal",
                    priority_score=5
                )
                db.add(pm)
                db.commit()
                db.refresh(pm)
                plan.current_members += 1
                db.commit()
            else:
                pm.is_active = True
                pm.ticket_number = f"TCK-{plan.id}-{idx:02d}"
                db.commit()

            # Check if Month 1 installment exists
            ins = db.query(Installment).filter(Installment.plan_member_id == pm.id, Installment.month_number == 1).first()
            if not ins:
                ins = Installment(
                    plan_member_id=pm.id,
                    plan_id=plan.id,
                    month_number=1,
                    due_date=date.today(),
                    base_amount=plan.monthly_amount,
                    total_amount=plan.monthly_amount,
                    status=InstallmentStatus.pending
                )
                db.add(ins)
                db.commit()
                print(f"[SUCCESS] Created Month 1 active due (Rs.{plan.monthly_amount}) for '{u.username}' in '{plan.plan_name}'!")
            else:
                ins.status = InstallmentStatus.pending
                ins.total_amount = plan.monthly_amount
                db.commit()
                print(f"[SUCCESS] Updated Month 1 due status to pending for '{u.username}'!")

        db.commit()
        print("[SUCCESS] All active dues generated successfully!")
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    generate_active_dues()

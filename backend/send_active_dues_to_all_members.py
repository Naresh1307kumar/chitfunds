import sys
import os
from datetime import date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.models.payment import Payment
from app.models.installment import Installment, InstallmentStatus
from app.models.plan_member import PlanMember
from app.models.chit_plan import ChitPlan

def send_dues_to_all():
    db = SessionLocal()
    try:
        print("=" * 60)
        print("SENDING MONTH 1 PENDING DUES TO ALL SYSTEM MEMBERS")
        print("=" * 60)

        # 1. Clear test payments
        deleted_count = db.query(Payment).delete(synchronize_session=False)
        db.commit()
        print(f"[CLEARED] Deleted {deleted_count} old payment records.")

        # 2. Get all plan members
        pms = db.query(PlanMember).filter(PlanMember.is_active == True).all()
        print(f"[FOUND] {len(pms)} Active Plan Member Enrollment(s)")

        for pm in pms:
            user = db.query(User).filter(User.id == pm.user_id).first()
            plan = db.query(ChitPlan).filter(ChitPlan.id == pm.plan_id).first()
            
            if not user or not plan:
                continue

            # Check existing Month 1 installment
            inst = db.query(Installment).filter(
                Installment.plan_member_id == pm.id,
                Installment.month_number == 1
            ).first()

            due_amt = plan.monthly_amount if plan.monthly_amount > 0 else 2000.0

            if inst:
                inst.status = InstallmentStatus.pending
                inst.base_amount = due_amt
                inst.total_amount = due_amt
                inst.paid_date = None
                inst.payment_method = None
                inst.transaction_id = None
                inst.receipt_number = None
                print(f"   - Updated Month 1 Due for Member '{user.name}' ({user.username}) | Plan: '{plan.plan_name}' -> Rs. {due_amt:,.0f} (PENDING)")
            else:
                inst = Installment(
                    plan_member_id=pm.id,
                    plan_id=plan.id,
                    month_number=1,
                    due_date=date.today(),
                    base_amount=due_amt,
                    total_amount=due_amt,
                    status=InstallmentStatus.pending
                )
                db.add(inst)
                print(f"   - Created New Month 1 Due for Member '{user.name}' ({user.username}) | Plan: '{plan.plan_name}' -> Rs. {due_amt:,.0f} (PENDING)")

        db.commit()
        print("\n" + "=" * 60)
        print("[SUCCESS] ALL MEMBERS NOW HAVE AN ACTIVE MONTH 1 PENDING DUE!")
        print("=" * 60)

    except Exception as e:
        print(f"[ERROR] Failed to send dues: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    send_dues_to_all()

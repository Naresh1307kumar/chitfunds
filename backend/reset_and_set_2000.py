import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.models.payment import Payment
from app.models.installment import Installment, InstallmentStatus
from app.models.plan_member import PlanMember

def reset_and_set_2000():
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.username.in_(["ramesh", "vikram2026"])).all()
        user_ids = [u.id for u in users]

        # 1. Delete all payment records for ramesh and vikram
        payments = db.query(Payment).filter(Payment.user_id.in_(user_ids)).all()
        for p in payments:
            db.delete(p)
        db.commit()

        # 2. Reset Month 1 installments to PENDING with total_amount = 2000
        pms = db.query(PlanMember).filter(PlanMember.user_id.in_(user_ids)).all()
        pm_ids = [pm.id for pm in pms]

        insts = db.query(Installment).filter(Installment.plan_member_id.in_(pm_ids)).all()
        for inst in insts:
            inst.status = InstallmentStatus.pending
            inst.base_amount = 2000.0
            inst.total_amount = 2000.0
            inst.paid_date = None
            inst.payment_method = None
            inst.transaction_id = None
            inst.receipt_number = None

        db.commit()
        print("[SUCCESS] Successfully deleted test payments and reset installments to PENDING with amount Rs.2,000!")

    except Exception as e:
        print(f"[ERROR] Failed to reset: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_and_set_2000()

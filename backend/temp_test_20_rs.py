import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.models.payment import Payment
from app.models.installment import Installment, InstallmentStatus
from app.models.plan_member import PlanMember

def set_temp_20_rs():
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.username.in_(["ramesh", "vikram2026"])).all()
        user_ids = [u.id for u in users]

        # 1. Delete all test payments for ramesh and vikram
        payments = db.query(Payment).filter(Payment.user_id.in_(user_ids)).all()
        for p in payments:
            db.delete(p)
        db.commit()
        print(f"[SUCCESS] Deleted {len(payments)} test payment records for Ramesh and Vikram!")

        # 2. Reset Month 1 installments to PENDING with total_amount = 20
        pms = db.query(PlanMember).filter(PlanMember.user_id.in_(user_ids)).all()
        pm_ids = [pm.id for pm in pms]

        insts = db.query(Installment).filter(Installment.plan_member_id.in_(pm_ids)).all()
        for inst in insts:
            inst.status = InstallmentStatus.pending
            inst.base_amount = 20.0
            inst.total_amount = 20.0
            inst.paid_date = None
            inst.payment_method = None
            inst.transaction_id = None
            inst.receipt_number = None

        db.commit()
        print(f"[SUCCESS] Reset {len(insts)} installment(s) back to PENDING with temporary test amount Rs.20!")

        print("\n============================================================")
        print("TEMPORARY TEST AMOUNT SET TO Rs.20 FOR RAMESH AND VIKRAM!")
        print("============================================================")

    except Exception as e:
        print(f"[ERROR] Failed to set temp Rs.20: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    set_temp_20_rs()

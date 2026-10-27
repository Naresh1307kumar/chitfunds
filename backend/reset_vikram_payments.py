import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.models.payment import Payment
from app.models.installment import Installment, InstallmentStatus
from app.models.plan_member import PlanMember

def reset_vikram():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username.in_(["vikram2026", "ramesh"])).all()
        for u in user:
            # Delete payments
            payments = db.query(Payment).filter(Payment.user_id == u.id).all()
            for p in payments:
                db.delete(p)
            db.commit()
            print(f"[SUCCESS] Deleted {len(payments)} test payment records for {u.username}!")

            # Reset Month 1 installment
            pms = db.query(PlanMember).filter(PlanMember.user_id == u.id).all()
            pm_ids = [pm.id for pm in pms]

            insts = db.query(Installment).filter(Installment.plan_member_id.in_(pm_ids)).all()
            for inst in insts:
                inst.status = InstallmentStatus.pending
                inst.paid_date = None
                inst.payment_method = None
                inst.transaction_id = None
                inst.receipt_number = None

            db.commit()
            print(f"[SUCCESS] Reset {len(insts)} installment(s) back to PENDING for {u.username}!")

    except Exception as e:
        print(f"[ERROR] Reset failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_vikram()

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.models.installment import Installment, InstallmentStatus

def reset_due():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "ramesh").first()
        inst = db.query(Installment).filter(Installment.id == 10).first()
        if inst:
            inst.status = InstallmentStatus.pending
            inst.paid_date = None
            inst.payment_method = None
            inst.transaction_id = None
            inst.receipt_number = None
            db.commit()
            print("[SUCCESS] Reset ramesh Month 1 due to PENDING for browser testing!")
    finally:
        db.close()

if __name__ == "__main__":
    reset_due()

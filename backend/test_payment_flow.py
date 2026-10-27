import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.models.installment import Installment, InstallmentStatus
from app.models.plan_member import PlanMember
from app.models.chit_plan import ChitPlan
from app.routers.member.payments import create_razorpay_order, verify_razorpay_payment

def test_payment():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "ramesh").first()
        inst = db.query(Installment).join(PlanMember).filter(
            PlanMember.user_id == user.id,
            Installment.status == InstallmentStatus.pending
        ).first()

        if not inst:
            print("[ERROR] No pending installment found for ramesh!")
            return

        print(f"Found pending installment ID {inst.id} for Rs.{inst.total_amount}")

        # 1. Create order test
        order_res = create_razorpay_order({"installment_id": inst.id}, db, user)
        print("Order Created:", order_res)

        # 2. Verify test
        verify_payload = {
            "installment_id": inst.id,
            "razorpay_payment_id": "pay_rzp_test_12345",
            "razorpay_order_id": order_res["order_id"],
            "razorpay_signature": "valid_sig",
            "payment_method": "Razorpay Instant UPI",
            "reason": "hospital"
        }
        verify_res = verify_razorpay_payment(verify_payload, db, user)
        print("Verification Result:", verify_res)

    except Exception as e:
        print(f"[TEST EXCEPTION ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_payment()

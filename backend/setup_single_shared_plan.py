import sys
import os
from datetime import date

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.models.chit_plan import ChitPlan
from app.models.plan_member import PlanMember
from app.models.installment import Installment, InstallmentStatus
from app.models.payment import Payment

def setup_single_shared_plan():
    db = SessionLocal()
    try:
        # Get Ramesh and Vikram users
        ramesh = db.query(User).filter(User.username == "ramesh").first()
        vikram = db.query(User).filter(User.username == "vikram2026").first()

        if not ramesh or not vikram:
            print("[ERROR] Users ramesh or vikram2026 not found!")
            return

        target_users = [ramesh, vikram]
        target_ids = [u.id for u in target_users]

        # 1. Clean existing payments, installments, and plan memberships for Ramesh and Vikram
        db.query(Payment).filter(Payment.user_id.in_(target_ids)).delete(synchronize_session=False)

        existing_pms = db.query(PlanMember).filter(PlanMember.user_id.in_(target_ids)).all()
        pm_ids = [pm.id for pm in existing_pms]
        if pm_ids:
            db.query(Installment).filter(Installment.plan_member_id.in_(pm_ids)).delete(synchronize_session=False)
            db.query(PlanMember).filter(PlanMember.id.in_(pm_ids)).delete(synchronize_session=False)

        db.commit()
        print("[SUCCESS] Cleared all old plans & installments for Ramesh and Vikram!")

        # 2. Select 1 single target plan (e.g., 'Silver Starter Scheme')
        plan = db.query(ChitPlan).filter(ChitPlan.plan_name == "Silver Starter Scheme", ChitPlan.is_deleted == False).first()
        if not plan:
            plan = db.query(ChitPlan).filter(ChitPlan.is_deleted == False).first()

        print(f"[TARGET PLAN] Registering both Ramesh and Vikram into '{plan.plan_name}' (Chit Value: Rs.{plan.total_value:,.0f})")

        # 3. Enroll both Ramesh and Vikram into the exact same plan
        for idx, user in enumerate(target_users, 1):
            ticket_no = f"TCK-{plan.id}-{idx:02d}"
            pm = PlanMember(
                plan_id=plan.id,
                user_id=user.id,
                is_active=True,
                ticket_number=ticket_no,
                joined_date=date.today(),
                reason="hospital" if idx == 1 else "education",
                priority_score=1 if idx == 1 else 2
            )
            db.add(pm)
            db.commit()
            db.refresh(pm)

            # Create Month 1 pending installment
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
            print(f"   - Enrolled '{user.username}' (Ticket: {ticket_no}) into '{plan.plan_name}'. Month 1 Due: Rs.{plan.monthly_amount:,.0f} (PENDING)")

        # Update current members count on target plan
        plan.current_members = 2
        db.commit()

        print("\n============================================================")
        print("[SUCCESS] Ramesh and Vikram are now enrolled in the EXACT SAME PLAN!")
        print(f"Plan Name: {plan.plan_name} | Monthly Installment: Rs.{plan.monthly_amount:,.0f}")
        print("============================================================")

    except Exception as e:
        print(f"[ERROR] Failed setup: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_single_shared_plan()

import sys, os
from datetime import datetime, date

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.database import SessionLocal
from app.models.user import User, UserRole, UserStatus, KYCStatus
from app.models.plan_member import PlanMember
from app.models.chit_plan import ChitPlan
from app.models.installment import Installment, InstallmentStatus
from app.utils.password import hash_password
import random

def main():
    db = SessionLocal()
    try:
        plan_id = 31
        plan = db.query(ChitPlan).filter(ChitPlan.id == plan_id).first()
        if not plan:
            print("Plan 31 not found.")
            return

        reasons = ["hospital", "education", "marriage", "business", "personal"]
        priority_map = {"hospital": 1, "education": 2, "marriage": 3, "business": 4, "personal": 5}
        
        # Add 18 users
        start_idx = plan.current_members + 1
        users_added = 0
        
        for i in range(18):
            username = f"user{start_idx + i}"
            plain_password = f"{username}123"
            hashed_pwd = hash_password(plain_password)
            
            # Create user
            new_user = User(
                username=username,
                name=f"Test User {start_idx + i}",
                email=f"{username}@example.com",
                phone=f"9876543{i:03d}",
                password_hash=hashed_pwd,
                role=UserRole.member,
                status=UserStatus.active,
                kyc_status=KYCStatus.verified
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # Add to plan
            ticket_number = f"TCK-{plan_id}-{start_idx + i:02d}"
            reason = random.choice(reasons)
            score = priority_map[reason]
            
            plan_member = PlanMember(
                plan_id=plan_id,
                user_id=new_user.id,
                is_active=True,
                joined_date=date.today(),
                reason=reason,
                priority_score=score,
                ticket_number=ticket_number
            )
            db.add(plan_member)
            db.commit()
            db.refresh(plan_member)
            
            # Generate Installment 1
            installment = Installment(
                plan_member_id=plan_member.id,
                plan_id=plan_id,
                month_number=1,
                due_date=date.today(),
                base_amount=plan.monthly_amount,
                total_amount=plan.monthly_amount,
                status=InstallmentStatus.paid,
                paid_date=date.today(),
                payment_method="System Generated",
                transaction_id=f"TXN-{plan_id}-{plan_member.id}-1",
                receipt_number=f"REC-{plan_member.id}-001"
            )
            db.add(installment)
            
            plan.current_members += 1
            users_added += 1

        db.commit()
        print(f"Added {users_added} users and joined them to plan {plan_id}.")
        
        # Now make sure all existing members also have different priorities and paid installments
        all_members = db.query(PlanMember).filter(PlanMember.plan_id == plan_id).all()
        for i, pm in enumerate(all_members):
            reason = reasons[i % len(reasons)]
            pm.reason = reason
            pm.priority_score = priority_map[reason]
            
            # Pay their installment if pending
            inst = db.query(Installment).filter(
                Installment.plan_member_id == pm.id,
                Installment.month_number == 1
            ).first()
            if inst:
                inst.status = InstallmentStatus.paid
                inst.paid_date = date.today()
                inst.payment_method = "System Generated"
                if not inst.transaction_id:
                    inst.transaction_id = f"TXN-SYSTEM-{pm.id}"
                if not inst.receipt_number:
                    inst.receipt_number = f"REC-SYS-{pm.id}-1"
            db.add(pm)
            
        db.commit()
        print("Updated priorities and installments for all 20 members.")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

import sys
import os
from datetime import datetime, date

from app.database import SessionLocal
from app.models.user import User, UserRole, UserStatus, KYCStatus
from app.models.chit_plan import ChitPlan, PlanStatus
from app.models.plan_member import PlanMember
from app.utils.password import hash_password

def seed_auction():
    db = SessionLocal()
    try:
        print("Seeding 10 Members and enrolling them into an Auction Chit Plan...")

        # 1. Create 10 demo members
        member_data = [
            ("Dr. Rajesh Kumar", "rajesh101", "rajesh@gmail.com", "9876543210", "hospital", 1),
            ("Priya Sharma", "priya102", "priya@gmail.com", "9876543211", "hospital", 1),
            ("Anand V", "anand103", "anand@gmail.com", "9876543212", "education", 2),
            ("Kavitha M", "kavitha104", "kavitha@gmail.com", "9876543213", "education", 2),
            ("Suresh Babu", "suresh105", "suresh@gmail.com", "9876543214", "marriage", 3),
            ("Meena K", "meena106", "meena@gmail.com", "9876543215", "marriage", 3),
            ("Venkatesh R", "venkat107", "venkat@gmail.com", "9876543216", "business", 4),
            ("Divya S", "divya108", "divya@gmail.com", "9876543217", "business", 4),
            ("Karthik N", "karthik109", "karthik@gmail.com", "9876543218", "personal", 5),
            ("Shanthi L", "shanthi110", "shanthi@gmail.com", "9876543219", "personal", 5),
        ]

        created_users = []
        for name, username, email, phone, reason, prio in member_data:
            existing = db.query(User).filter(User.username == username).first()
            if not existing:
                u = User(
                    name=name,
                    username=username,
                    email=email,
                    phone=phone,
                    password_hash=hash_password("Password@123"),
                    role=UserRole.member,
                    status=UserStatus.active,
                    kyc_status=KYCStatus.verified
                )
                db.add(u)
                db.commit()
                db.refresh(u)
                created_users.append((u, reason, prio))
            else:
                existing.status = UserStatus.active
                existing.kyc_status = KYCStatus.verified
                db.commit()
                created_users.append((existing, reason, prio))

        print(f"[OK] {len(created_users)} Active & Verified Members ready.")

        # 2. Get or create Auction Chit Plan
        plan = db.query(ChitPlan).filter(
            ChitPlan.chit_type == "auction",
            ChitPlan.is_deleted == False
        ).first()

        if not plan:
            admin_user = db.query(User).filter(User.role == UserRole.admin).first()
            admin_id = admin_user.id if admin_user else 1
            plan = ChitPlan(
                plan_name="Gold Emergency Auction Scheme",
                plan_type="gold",
                chit_type="auction",
                monthly_amount=5000.0,
                total_members=10,
                current_members=10,
                duration_months=10,
                total_value=50000.0,
                commission_rate=5.0,
                net_prize_amount=47500.0,
                start_date=date.today(),
                end_date=date.today(),
                status=PlanStatus.active,
                created_by=admin_id
            )
            db.add(plan)
            db.commit()
            db.refresh(plan)
            print(f"[SUCCESS] Created new Auction Plan: '{plan.plan_name}' (ID: {plan.id})")
        else:
            plan.status = PlanStatus.active
            plan.current_members = len(created_users)
            db.commit()
            print(f"[SUCCESS] Using existing Auction Plan: '{plan.plan_name}' (ID: {plan.id})")

        # 3. Enroll members into the auction plan
        enrolled_count = 0
        for idx, (user_obj, reason, prio) in enumerate(created_users, start=101):
            ticket_num = f"TCK-{plan.id}-{idx}"
            existing_mem = db.query(PlanMember).filter(
                PlanMember.plan_id == plan.id,
                PlanMember.user_id == user_obj.id
            ).first()

            if not existing_mem:
                pm = PlanMember(
                    user_id=user_obj.id,
                    plan_id=plan.id,
                    joined_date=date.today(),
                    has_won=False,
                    is_active=True,
                    reason=reason,
                    priority_score=prio,
                    ticket_number=ticket_num
                )
                db.add(pm)
                enrolled_count += 1
            else:
                existing_mem.is_active = True
                existing_mem.reason = reason
                existing_mem.priority_score = prio
                existing_mem.ticket_number = ticket_num

        db.commit()
        print(f"[SUCCESS] Successfully enrolled 10 members with priority ranks & ticket IDs into Plan ID #{plan.id}!")
        print("   Users created with Password: Password@123")

    except Exception as e:
        print(f"[ERROR] Error seeding auction members: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_auction()

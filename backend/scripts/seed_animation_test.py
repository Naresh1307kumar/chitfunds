import sys
import os
from datetime import datetime, date

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.user import User, UserRole, UserStatus, KYCStatus
from app.models.chit_plan import ChitPlan, PlanStatus, PlanType
from app.models.plan_member import PlanMember
from app.utils.password import hash_password

def seed_data():
    db = SessionLocal()
    
    try:
        print("Seeding test data for Animation...")
        
        # 1. Create 10 Users
        users = []
        for i in range(1, 11):
            username = f"testuser{i}"
            # Check if user already exists
            user = db.query(User).filter(User.username == username).first()
            if not user:
                user = User(
                    username=username,
                    name=f"Test Member {i}",
                    email=f"test{i}@example.com",
                    phone=f"98765432{i:02d}",
                    password_hash=hash_password("Pass@123"),
                    role=UserRole.member,
                    status=UserStatus.active,
                    kyc_status=KYCStatus.verified,
                    aadhar_number=f"1234567890{i:02d}",
                    pan_number=f"ABCDE123{i}F"
                )
                db.add(user)
                users.append(user)
            else:
                users.append(user)
                
        db.commit()
        for u in users:
            db.refresh(u)
            
        print("10 Verified Users created successfully!")
        
        # 2. Get Admin ID
        admin = db.query(User).filter(User.role == UserRole.admin).first()
        if not admin:
            print("Admin user not found. Please create an admin first.")
            return

        # 3. Create a Test Plan
        plan = ChitPlan(
            plan_name="Notification Test Scheme",
            plan_type=PlanType.gold,
            monthly_amount=5000,
            total_members=10,
            current_members=10,
            duration_months=10,
            total_value=50000,
            commission_rate=5.0,
            net_prize_amount=47500,
            start_date=date.today(),
            end_date=date.today(),  # Simplified for test
            status=PlanStatus.active,
            created_by=admin.id
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        print(f"Active Plan '{plan.plan_name}' created!")

        # 4. Add 10 Users to the Plan
        for i, user in enumerate(users):
            pm = PlanMember(
                user_id=user.id,
                plan_id=plan.id,
                joined_date=date.today(),
                is_active=True,
                has_won=False,
                ticket_number=f"TCK-{plan.id}-{i+1:02d}"
            )
            db.add(pm)
            
        db.commit()
        print("All 10 members added to the plan!")
        print("Setup Complete! You can now login as Admin and test the Draw Animation.")

    except Exception as e:
        print(f"Error: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()

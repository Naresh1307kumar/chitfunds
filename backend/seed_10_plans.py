import sys
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models.chit_plan import ChitPlan, PlanType, PlanStatus
from app.models.user import User, UserRole

def seed_exact_10_plans():
    db = SessionLocal()
    try:
        # Fetch admin user
        admin = db.query(User).filter(User.role == UserRole.admin).first()
        admin_id = admin.id if admin else 1

        # Delete / soft-delete existing old plans
        db.query(ChitPlan).update({"is_deleted": True, "status": PlanStatus.cancelled})
        db.commit()
        print("[INFO] Existing old plans marked as deleted.")

        # Define 10 realistic auction plans
        ten_plans = [
            {"name": "Bronze Express Savings", "type": PlanType.bronze, "monthly": 2000, "members": 10, "duration": 10},
            {"name": "Silver Starter Scheme", "type": PlanType.silver, "monthly": 2000, "members": 20, "duration": 20},
            {"name": "Bronze Flexi Savings", "type": PlanType.bronze, "monthly": 5000, "members": 10, "duration": 10},
            {"name": "Gold Growth Fund", "type": PlanType.gold, "monthly": 5000, "members": 20, "duration": 20},
            {"name": "Silver Prosperity Chit", "type": PlanType.silver, "monthly": 10000, "members": 15, "duration": 15},
            {"name": "Gold Fortune Wealth", "type": PlanType.gold, "monthly": 10000, "members": 20, "duration": 20},
            {"name": "Silver Super Saver", "type": PlanType.silver, "monthly": 15000, "members": 20, "duration": 20},
            {"name": "Gold Business Capital", "type": PlanType.gold, "monthly": 25000, "members": 20, "duration": 20},
            {"name": "Gold Enterprise Fund", "type": PlanType.gold, "monthly": 40000, "members": 20, "duration": 20},
            {"name": "Gold Sovereign Wealth", "type": PlanType.gold, "monthly": 50000, "members": 20, "duration": 20},
        ]

        start_d = date.today()

        for idx, p in enumerate(ten_plans, 1):
            chit_val = p["monthly"] * p["members"]
            end_d = start_d + relativedelta(months=p["duration"])
            net_prize = chit_val * 0.95

            new_plan = ChitPlan(
                plan_name=p["name"],
                plan_type=p["type"],
                chit_type="auction",
                monthly_amount=float(p["monthly"]),
                total_members=p["members"],
                current_members=0,
                duration_months=p["duration"],
                total_value=float(chit_val),
                chit_value=float(chit_val),
                commission_rate=5.0,
                net_prize_amount=float(net_prize),
                start_date=start_d,
                end_date=end_d,
                status=PlanStatus.active,
                is_deleted=False,
                created_by=admin_id
            )
            db.add(new_plan)

        db.commit()
        print(f"[SUCCESS] Exactly {len(ten_plans)} active auction plans created successfully!")

    except Exception as e:
        print(f"[ERROR] Failed to seed 10 plans: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_exact_10_plans()

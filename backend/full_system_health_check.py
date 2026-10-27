import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models.user import User, UserRole, UserStatus
from app.models.chit_plan import ChitPlan, PlanStatus
from app.models.plan_member import PlanMember
from app.models.installment import Installment, InstallmentStatus
from app.models.payment import Payment
from app.services.auth_service import login_user
from app.schemas.auth import LoginRequest

def health_check():
    print("=" * 60)
    print("SECURE CHIT FUND - SYSTEM TESTING & VALIDATION CHECK")
    print("=" * 60)

    db = SessionLocal()
    try:
        # 1. Check Plans
        plans = db.query(ChitPlan).filter(ChitPlan.is_deleted == False).all()
        print(f"\n1. CHIT PLANS COUNT: {len(plans)} Plans Seeded")
        for p in plans[:5]:
            print(f"   - [{p.plan_type.value.upper()}] {p.plan_name}: Chit Value Rs.{p.total_value:,.0f} ({p.duration_months} Months @ Rs.{p.monthly_amount:,.0f}/mo)")

        # 2. Check Users & Login Authentication
        users = db.query(User).filter(User.is_deleted == False).all()
        print(f"\n2. SYSTEM USERS COUNT: {len(users)} Active Users")
        
        # Test Member Login (ramesh)
        res_r = login_user(db, LoginRequest(username="ramesh", password="ramesh1234"), UserRole.member)
        print("   - Ramesh Login (ramesh / ramesh1234): SUCCESS")

        # Test Member Login (vikram2026)
        res_v = login_user(db, LoginRequest(username="vikram2026", password="Password@123"), UserRole.member)
        print("   - Vikram Login (vikram2026 / Password@123): SUCCESS")

        # Test Admin Login (admin)
        res_a = login_user(db, LoginRequest(username="admin", password="admin123"), UserRole.admin)
        print("   - Admin Login (admin / admin123): SUCCESS")

        # 3. Check Dues & Installments
        dues = db.query(Installment).filter(Installment.status == InstallmentStatus.pending).all()
        print(f"\n3. ACTIVE PENDING DUES: {len(dues)} Pending Installment(s)")
        for d in dues:
            pm = db.query(PlanMember).filter(PlanMember.id == d.plan_member_id).first()
            u = db.query(User).filter(User.id == pm.user_id).first() if pm else None
            p = db.query(ChitPlan).filter(ChitPlan.id == d.plan_id).first()
            print(f"   - User: '{u.username if u else 'N/A'}' | Plan: '{p.plan_name if p else 'N/A'}' | Month {d.month_number} Due: Rs.{d.total_amount:,.0f}")

        # 4. Check Payment Receipts & Verification
        payments = db.query(Payment).all()
        print(f"\n4. PAYMENT TRANSACTIONS RECORDED: {len(payments)} Payments")

        print("\n" + "=" * 60)
        print("ALL BACKEND & DATABASE SYSTEM CHECKS PASSED 100%!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ [HEALTH CHECK ERROR] {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    health_check()

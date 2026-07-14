"""
Run this script to create the first admin account.
Usage: python seeds/admin_seed.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.user import User, UserRole, UserStatus, KYCStatus
from app.utils.password import hash_password
from datetime import datetime


def create_admin():
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing = db.query(User).filter(User.email == "admin@securechit.com").first()
        if existing:
            print("✅ Admin already exists: admin@securechit.com")
            return

        admin = User(
            name="SecureChit Admin",
            email="admin@securechit.com",
            phone="9999999999",
            password_hash=hash_password("Admin@123"),
            role=UserRole.admin,
            status=UserStatus.active,
            kyc_status=KYCStatus.verified,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print("✅ Admin created successfully!")
        print("   Email   : admin@securechit.com")
        print("   Password: Admin@123")
        print("   ⚠️  Please change the password after first login!")
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()

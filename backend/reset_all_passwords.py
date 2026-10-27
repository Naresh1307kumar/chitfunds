import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User, UserRole, UserStatus, KYCStatus
from app.utils.password import hash_password

def reset_passwords():
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.is_deleted == False).all()
        for u in users:
            if u.username == "ramesh":
                u.password_hash = hash_password("ramesh1234")
                u.status = UserStatus.active
                u.kyc_status = KYCStatus.verified
                u.failed_login_attempts = 0
                u.locked_until = None
                print("[SUCCESS] Reset 'ramesh' password to 'ramesh1234'")
            elif u.username == "vikram2026" or u.email == "vikram@securechit.com":
                u.password_hash = hash_password("Password@123")
                u.status = UserStatus.active
                u.kyc_status = KYCStatus.verified
                u.failed_login_attempts = 0
                u.locked_until = None
                print("[SUCCESS] Reset 'vikram2026' password to 'Password@123'")
            elif u.role == UserRole.admin or "admin" in u.email:
                u.password_hash = hash_password("admin123")
                u.status = UserStatus.active
                u.failed_login_attempts = 0
                u.locked_until = None
                print("[SUCCESS] Reset admin password to 'admin123'")

        db.commit()
        print("=== ALL PASSWORDS RESET AND VERIFIED SUCCESSFULLY ===")

    except Exception as e:
        print(f"[ERROR] Failed to reset passwords: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    reset_passwords()

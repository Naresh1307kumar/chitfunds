import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User, UserRole, UserStatus, KYCStatus
from app.utils.password import hash_password

def create_ramesh_user():
    db = SessionLocal()
    try:
        username = "ramesh"
        plain_password = "ramesh1234"
        hashed_pwd = hash_password(plain_password)

        existing = db.query(User).filter(User.username == username).first()
        if existing:
            existing.password_hash = hashed_pwd
            existing.status = UserStatus.active
            existing.kyc_status = KYCStatus.verified
            existing.is_deleted = False
            db.commit()
            print(f"[SUCCESS] Updated password for existing user '{username}'.")
        else:
            new_user = User(
                username=username,
                name="Ramesh Kumar",
                email="ramesh@securechit.com",
                phone="9876543210",
                password_hash=hashed_pwd,
                role=UserRole.member,
                status=UserStatus.active,
                kyc_status=KYCStatus.verified
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            print(f"[SUCCESS] Created new user '{username}' (ID: {new_user.id}).")

        print("----------------------------------------")
        print(f"Username : {username}")
        print(f"Password : {plain_password}")
        print("Status   : Active & KYC Verified")
        print("----------------------------------------")

    except Exception as e:
        print(f"[ERROR] Failed to create user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_ramesh_user()

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User, UserRole, UserStatus
from app.utils.password import hash_password, verify_password

def verify_admin():
    db = SessionLocal()
    try:
        admins = db.query(User).filter(User.role == UserRole.admin).all()
        print(f"Found {len(admins)} Admin user(s) in DB:")
        for a in admins:
            print(f"ID: {a.id} | Username: '{a.username}' | Email: '{a.email}' | Status: {a.status} | Failed Attempts: {a.failed_login_attempts}")
            a.username = "admin"
            a.email = "admin@securechit.com"
            a.password_hash = hash_password("admin123")
            a.status = UserStatus.active
            a.failed_login_attempts = 0
            db.commit()
            print(f"[VERIFIED & UPDATED] Admin username='admin', email='admin@securechit.com', password='admin123'")
            
            # Verify password check
            print(f"Testing password 'admin123': {verify_password('admin123', a.password_hash)}")

    finally:
        db.close()

if __name__ == "__main__":
    verify_admin()

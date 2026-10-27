import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User, UserRole, UserStatus, KYCStatus
from app.utils.password import hash_password

def verify_and_print_users():
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.is_deleted == False).all()
        print("=== ACTIVE SYSTEM USER CREDENTIALS ===")
        for u in users:
            print(f"Role: {u.role.value.upper()} | Name: {u.name} | Username: {u.username} | Email: {u.email} | Status: {u.status.value}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_and_print_users()

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.services.auth_service import login_user
from app.schemas.auth import LoginRequest
from app.models.user import UserRole

def test_login():
    db = SessionLocal()
    try:
        # Test 1: Username 'admin' + password 'admin123'
        res1 = login_user(db, LoginRequest(username="admin", password="admin123"), UserRole.admin)
        print("[SUCCESS] Login with username 'admin' passed! Access Token generated.")

        # Test 2: Email 'admin@securechit.com' + password 'admin123'
        res2 = login_user(db, LoginRequest(username="admin@securechit.com", password="admin123"), UserRole.admin)
        print("[SUCCESS] Login with email 'admin@securechit.com' passed! Access Token generated.")

    except Exception as e:
        print(f"[LOGIN ERROR] {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_login()

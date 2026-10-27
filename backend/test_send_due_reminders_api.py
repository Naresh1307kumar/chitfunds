import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.services.auth_service import login_user
from app.schemas.auth import LoginRequest
from app.models.user import UserRole

def test_due_reminders():
    db = SessionLocal()
    try:
        # Admin login
        admin_res = login_user(db, LoginRequest(username="admin", password="admin123"), UserRole.admin)
        print("[SUCCESS] Admin login passed!")

        # Import notification service function
        from app.services.notification_service import send_10th_due_reminder_notifications
        count = send_10th_due_reminder_notifications()
        print(f"\n============================================================")
        print(f"[SUCCESS] Due reminder emails sent to {count} unpaid members!")
        print("============================================================")

    except Exception as e:
        print(f"[ERROR] Failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_due_reminders()

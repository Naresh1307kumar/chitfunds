import sys
import os
from datetime import datetime, date

from app.database import SessionLocal
from app.models import (
    User, UserRole, UserStatus, KYCStatus,
    PlanMember, MonthlyDraw, KYCDocument, Guarantor,
    Installment, Payment, Notification, Certificate,
    Report, PasswordReset, ChitPlan
)
from app.utils.password import hash_password

def setup_fresh_user():
    db = SessionLocal()
    try:
        print("Cleaning up old member data and creating a fresh user...")

        # 1. Delete dependent transactional records
        db.query(Payment).delete()
        db.query(Installment).delete()
        db.query(MonthlyDraw).delete()
        db.query(PlanMember).delete()
        db.query(KYCDocument).delete()
        db.query(Guarantor).delete()
        db.query(Certificate).delete()
        db.query(Report).delete()
        db.query(PasswordReset).delete()
        db.query(Notification).delete()

        # 2. Reset plan current_members to 0
        db.query(ChitPlan).update({"current_members": 0})

        # 3. Delete all non-admin users
        deleted_count = db.query(User).filter(User.role != UserRole.admin).delete()

        # 4. Create fresh primary member account
        fresh_user = User(
            name="Vikramaditya S",
            username="vikram2026",
            email="vikram@securechit.com",
            phone="9876501234",
            password_hash=hash_password("Vikram@2026"),
            role=UserRole.member,
            status=UserStatus.active,
            kyc_status=KYCStatus.verified
        )
        db.add(fresh_user)
        db.commit()
        db.refresh(fresh_user)

        print("\n==============================================")
        print("FRESH USER CREATION COMPLETED SUCCESSFULLY!")
        print("==============================================")
        print(f"• Deleted Old Member Accounts : {deleted_count}")
        print(f"• Fresh Member Name          : {fresh_user.name}")
        print(f"• Member ID                  : PM-{fresh_user.id}")
        print(f"• Username                   : {fresh_user.username}")
        print(f"• Password                   : Vikram@2026")
        print(f"• Email                      : {fresh_user.email}")
        print(f"• Status                     : ACTIVE & KYC VERIFIED")
        print("==============================================")

    except Exception as e:
        print(f"[ERROR] Failed to create fresh user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_fresh_user()

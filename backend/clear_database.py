import sys
import os

from app.database import SessionLocal
from app.models import (
    User, UserRole, ChitPlan, PlanMember, MonthlyDraw,
    KYCDocument, Guarantor, Installment, Payment,
    Notification, Certificate, Report, AuditLog,
    PasswordReset
)

def clear_all_plans_and_members():
    db = SessionLocal()
    try:
        print("Wiping all existing plans, member accounts, draws, and ledgers...")

        # 1. Delete dependent transactional records
        num_payments = db.query(Payment).delete()
        num_installments = db.query(Installment).delete()
        num_draws = db.query(MonthlyDraw).delete()
        num_plan_members = db.query(PlanMember).delete()
        
        # 2. Delete chit plans
        num_plans = db.query(ChitPlan).delete()

        # 3. Delete member KYC, guarantors, certificates, reports, password resets & notifications
        num_kyc = db.query(KYCDocument).delete()
        num_guarantors = db.query(Guarantor).delete()
        num_certs = db.query(Certificate).delete()
        num_reports = db.query(Report).delete()
        num_resets = db.query(PasswordReset).delete()
        num_notifs = db.query(Notification).delete()
        num_audit = db.query(AuditLog).delete()

        # 4. Delete all user accounts EXCEPT System Admin
        non_admin_users = db.query(User).filter(User.role != UserRole.admin).delete()

        db.commit()

        print("\n==============================================")
        print("DATABASE CLEANUP COMPLETED SUCCESSFULLY!")
        print("==============================================")
        print(f"• Deleted Chit Plans        : {num_plans}")
        print(f"• Deleted Enrolled Tickets  : {num_plan_members}")
        print(f"• Deleted Monthly Draws     : {num_draws}")
        print(f"• Deleted Installments      : {num_installments}")
        print(f"• Deleted Payments          : {num_payments}")
        print(f"• Deleted Member Accounts   : {non_admin_users}")
        print("• Preserved System Admin    : admin (admin@securechit.com)")
        print("==============================================")

    except Exception as e:
        print(f"[ERROR] Failed to clear database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_all_plans_and_members()

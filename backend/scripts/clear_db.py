import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.user import User, UserRole
from app.models.chit_plan import ChitPlan
from app.models.plan_member import PlanMember
from app.models.draw import MonthlyDraw
from app.models.kyc import KYCDocument
from app.models.password_reset import PasswordReset

def clear_db():
    db: Session = SessionLocal()
    try:
        print("Clearing test data...")
        
        # Delete dependent tables first
        db.query(MonthlyDraw).delete()
        db.query(PlanMember).delete()
        db.query(ChitPlan).delete()
        db.query(KYCDocument).delete()
        db.query(PasswordReset).delete()
        
        # Delete all members (keep admin)
        members_deleted = db.query(User).filter(User.role == UserRole.member).delete()
        
        db.commit()
        print(f"Successfully cleared test data. Deleted {members_deleted} members.")
        
    except Exception as e:
        print(f"Error clearing db: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_db()

import sys
import os
from dotenv import load_dotenv

load_dotenv('c:/chit fund/backend/.env')
sys.path.insert(0, 'c:/chit fund/backend')

from app.database import SessionLocal
from app.models.user import User
from app.models.promissory_note import PromissoryNote
from app.models.draw import MonthlyDraw
from app.models.plan_member import PlanMember
from app.models.installment import Installment

db = SessionLocal()

try:
    print("--- Cleaning Promissory Notes & Monthly Draws ---")
    
    # 1. Delete all promissory notes
    pronotes_count = db.query(PromissoryNote).delete()
    print(f"Deleted {pronotes_count} Promissory Note(s)")

    # 2. Delete all monthly draws
    draws_count = db.query(MonthlyDraw).delete()
    print(f"Deleted {draws_count} Monthly Draw(s)")

    # 3. Reset has_won = False for all tickets in Plan 31 (and all plans)
    members = db.query(PlanMember).all()
    for m in members:
        m.has_won = False
        m.is_active = True
    print(f"Reset {len(members)} ticket(s) to has_won = False")

    # 4. Remove generated installments for month > 1
    installments_count = db.query(Installment).filter(Installment.month_number > 1).delete()
    print(f"Cleaned {installments_count} future installment(s)")

    db.commit()
    print("\n--- RESET COMPLETED SUCCESSFULLY! ---")

    # Verify state
    ramesh = db.query(User).filter(User.name.ilike('%ramesh%')).first()
    vikram = db.query(User).filter(User.name.ilike('%vikram%')).first()

    print(f"\nRamesh (ID: {ramesh.id}): Eligible to win & get Pronote")
    print(f"Vikram (ID: {vikram.id}): Eligible to win & get Pronote")

except Exception as e:
    db.rollback()
    print("ERROR:", e)
finally:
    db.close()

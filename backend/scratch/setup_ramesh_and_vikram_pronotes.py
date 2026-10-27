import sys
import os
from datetime import date, timedelta, datetime
from dotenv import load_dotenv

load_dotenv('c:/chit fund/backend/.env')
sys.path.insert(0, 'c:/chit fund/backend')

from app.database import SessionLocal
from app.models.user import User
from app.models.chit_plan import ChitPlan
from app.models.promissory_note import PromissoryNote, PronoteStatus

db = SessionLocal()

try:
    ramesh = db.query(User).filter(User.id == 29).first()
    vikram = db.query(User).filter(User.id == 28).first()
    plan = db.query(ChitPlan).filter(ChitPlan.id == 31).first()

    print(f"Ramesh: {ramesh.name} (ID: {ramesh.id})")
    print(f"Vikram: {vikram.name} (ID: {vikram.id})")
    print(f"Plan: {plan.plan_name} (ID: {plan.id})")

    # Clean existing pronotes first to be 100% clean
    db.query(PromissoryNote).delete()
    db.commit()

    year = datetime.now().year

    # 1. Create Pronote for Ramesh Kumar
    pronote_ramesh = PromissoryNote(
        pronote_id=f"PRN-{year}-0001",
        member_id=ramesh.id,
        chit_id=plan.id,
        loan_amount=36000.0,
        issue_date=date.today(),
        due_date=date.today() + timedelta(days=365),
        interest_rate=0.0,
        repayment_amount=36000.0,
        purpose=f"Security Undertaking for Month 1 Draw ({plan.plan_name})",
        status=PronoteStatus.pending_signature,
        signature=None
    )
    db.add(pronote_ramesh)

    # 2. Create Pronote for Vikramaditya S
    pronote_vikram = PromissoryNote(
        pronote_id=f"PRN-{year}-0002",
        member_id=vikram.id,
        chit_id=plan.id,
        loan_amount=36000.0,
        issue_date=date.today(),
        due_date=date.today() + timedelta(days=365),
        interest_rate=0.0,
        repayment_amount=36000.0,
        purpose=f"Security Undertaking for Month 1 Draw ({plan.plan_name})",
        status=PronoteStatus.pending_signature,
        signature=None
    )
    db.add(pronote_vikram)

    db.commit()

    print("\n--- PROMISORY NOTES CREATED SUCCESSFULLY! ---")
    print(f"1. Ramesh Kumar -> Pronote ID: PRN-{year}-0001 | Status: pending_signature")
    print(f"2. Vikramaditya S -> Pronote ID: PRN-{year}-0002 | Status: pending_signature")

except Exception as e:
    db.rollback()
    print("ERROR:", e)
finally:
    db.close()

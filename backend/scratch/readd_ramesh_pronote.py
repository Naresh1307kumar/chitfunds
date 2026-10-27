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
    plan = db.query(ChitPlan).filter(ChitPlan.id == 31).first()

    existing = db.query(PromissoryNote).filter(PromissoryNote.member_id == ramesh.id).first()
    if existing:
        print(f"Ramesh already has pronote ID {existing.pronote_id}, updating to pending_signature...")
        existing.status = PronoteStatus.pending_signature
        existing.signature = None
    else:
        print("Creating fresh Promissory Note for Ramesh...")
        year = datetime.now().year
        
        # Find next available PRN-2026-XXXX ID
        all_notes = db.query(PromissoryNote).all()
        used_numbers = []
        for n in all_notes:
            if n.pronote_id and n.pronote_id.startswith(f"PRN-{year}-"):
                try:
                    num = int(n.pronote_id.split("-")[-1])
                    used_numbers.append(num)
                except:
                    pass
        next_num = max(used_numbers) + 1 if used_numbers else 1
        auto_id = f"PRN-{year}-{next_num:04d}"

        pronote_ramesh = PromissoryNote(
            pronote_id=auto_id,
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

    db.commit()

    notes = db.query(PromissoryNote).all()
    print("\n--- ALL PROMISSORY NOTES IN DB ---")
    for n in notes:
        m = db.query(User).filter(User.id == n.member_id).first()
        print(f"DB ID: {n.id} | Code: {n.pronote_id} | Member: {m.name if m else n.member_id} | Amount: ₹{n.loan_amount} | Status: {n.status.value}")

except Exception as e:
    db.rollback()
    print("ERROR:", e)
finally:
    db.close()

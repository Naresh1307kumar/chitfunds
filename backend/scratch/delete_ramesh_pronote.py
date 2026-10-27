import sys
import os
from dotenv import load_dotenv

load_dotenv('c:/chit fund/backend/.env')
sys.path.insert(0, 'c:/chit fund/backend')

from app.database import SessionLocal
from app.models.promissory_note import PromissoryNote
from app.models.user import User

db = SessionLocal()

try:
    ramesh = db.query(User).filter(User.id == 29).first()
    notes = db.query(PromissoryNote).filter(PromissoryNote.member_id == 29).all()
    
    print(f"Found {len(notes)} pronote(s) for {ramesh.name if ramesh else 'Ramesh'}:")
    for n in notes:
        print(f"Deleting Pronote DB ID: {n.id}, Pronote ID: {n.pronote_id}, Amount: {n.loan_amount}, Status: {n.status.value}")
        db.delete(n)
        
    db.commit()
    print("SUCCESS: Deleted all existing pronotes for Ramesh. Ready to issue fresh note from scratch!")

except Exception as e:
    db.rollback()
    print("ERROR:", e)
finally:
    db.close()

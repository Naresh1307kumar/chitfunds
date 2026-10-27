import sys
import os
from dotenv import load_dotenv

load_dotenv('c:/chit fund/backend/.env')
sys.path.insert(0, 'c:/chit fund/backend')

from app.database import SessionLocal
from app.models.promissory_note import PromissoryNote, PronoteStatus

db = SessionLocal()

try:
    pronote = db.query(PromissoryNote).filter(PromissoryNote.member_id == 29).first()
    if pronote:
        pronote.status = PronoteStatus.pending_signature
        pronote.signature = None
        db.commit()
        print("Pronote status reset to 'pending_signature' for testing user interactive signing!")
    else:
        print("No pronote found for member_id 29")

except Exception as e:
    db.rollback()
    print("ERROR:", e)
finally:
    db.close()

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

db = SessionLocal()

try:
    ramesh = db.query(User).filter(User.name.ilike('%ramesh%')).first()
    vikram = db.query(User).filter(User.name.ilike('%vikram%')).first()

    print("Users found:")
    print("Ramesh:", (ramesh.id, ramesh.name, ramesh.email) if ramesh else "Not found")
    print("Vikram:", (vikram.id, vikram.name, vikram.email) if vikram else "Not found")

    print("\nPromissory Notes in DB:")
    notes = db.query(PromissoryNote).all()
    for n in notes:
        print(f"Pronote ID: {n.id}, Code: {n.pronote_id}, Member ID: {n.member_id}, Status: {n.status.value}")

    print("\nMonthly Draws in DB:")
    draws = db.query(MonthlyDraw).all()
    for d in draws:
        print(f"Draw ID: {d.id}, Plan ID: {d.plan_id}, Month: {d.month_number}, Winner ID: {d.winner_id}")

    print("\nPlan Memberships:")
    members = db.query(PlanMember).all()
    for m in members:
        print(f"Member Ticket ID: {m.id}, Plan ID: {m.plan_id}, User ID: {m.user_id}, Ticket: {m.ticket_number}, Has Won: {m.has_won}")

except Exception as e:
    print("ERROR:", e)
finally:
    db.close()

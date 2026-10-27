import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from app.database import SessionLocal
from app.models.user import User
from app.models.plan_member import PlanMember

db = SessionLocal()
ramesh = db.query(User).filter(User.username == 'ramesh').first()
vikram = db.query(User).filter(User.username.like('%vik%')).first() 

print(f"Ramesh: {ramesh.id if ramesh else 'Not found'}")
if vikram:
    print(f"Vikram: {vikram.id} (username: {vikram.username})")
else:
    print("Vikram: Not found")

if ramesh:
    pm = db.query(PlanMember).filter(PlanMember.user_id == ramesh.id).first()
    print(f"Ramesh PlanMember: plan_id={pm.plan_id if pm else 'None'}, priority_score={pm.priority_score if pm else 'None'}")
    
if vikram:
    pm2 = db.query(PlanMember).filter(PlanMember.user_id == vikram.id).first()
    print(f"Vikram PlanMember: plan_id={pm2.plan_id if pm2 else 'None'}")

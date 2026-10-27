import sys
import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv('c:/chit fund/backend/.env')
sys.path.insert(0, 'c:/chit fund/backend')

from app.database import SessionLocal
from app.models.user import User, UserRole
from app.utils.jwt import create_access_token

db = SessionLocal()
admin = db.query(User).filter(User.role == UserRole.admin).first()

if not admin:
    print("No admin user found!")
    sys.exit(1)

print(f"Admin found: {admin.email} (ID: {admin.id})")
db.close()

token = create_access_token(data={"sub": str(admin.id), "role": admin.role.value})

endpoints = [
    "/api/v1/admin/users/",
    "/api/v1/admin/plans/",
    "/api/v1/admin/pronotes/"
]

for ep in endpoints:
    url = f"http://localhost:8000{ep}"
    try:
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"GET {ep} -> Status {resp.status}, Items count: {len(data)}")
    except Exception as e:
        print(f"GET {ep} -> ERROR: {e}")

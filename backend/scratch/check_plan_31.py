import os
from dotenv import load_dotenv
load_dotenv('c:/chit fund/backend/.env')
import psycopg2

db_url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("""
    SELECT cp.id, cp.plan_name, cp.status, cp.monthly_amount, cp.total_members, cp.duration_months, cp.chit_value, cp.chit_type
    FROM chit_plans cp
    WHERE cp.id = 31
""")
plan = cur.fetchone()
print("Plan 31 details:", plan)

cur.execute("""
    SELECT pm.id, pm.ticket_number, pm.user_id, u.name, u.email, pm.has_won, pm.is_active
    FROM plan_members pm
    JOIN users u ON pm.user_id = u.id
    WHERE pm.plan_id = 31
""")
members = cur.fetchall()
print("\nPlan 31 members:")
for m in members:
    print(m)

conn.close()

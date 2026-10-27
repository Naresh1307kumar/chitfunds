import os
from dotenv import load_dotenv
load_dotenv('c:/chit fund/backend/.env')
import psycopg2

db_url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("""
    SELECT pm.id, pm.plan_id, cp.plan_name, pm.user_id, u.name, pm.ticket_number, pm.has_won, pm.is_active
    FROM plan_members pm
    JOIN chit_plans cp ON pm.plan_id = cp.id
    JOIN users u ON pm.user_id = u.id
    WHERE u.id = 29 OR u.name ILIKE '%ramesh%'
""")
memberships = cur.fetchall()
print("Ramesh memberships:")
for m in memberships:
    print(m)

conn.close()

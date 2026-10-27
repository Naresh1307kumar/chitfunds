import sys
import os
from dotenv import load_dotenv
load_dotenv('c:/chit fund/backend/.env')

import psycopg2

db_url = os.getenv("DATABASE_URL")
print("Connecting to:", db_url)

try:
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = cur.fetchall()
    print("Tables:", [t[0] for t in tables])
    
    cur.execute("SELECT id, name, email, role FROM users WHERE name ILIKE '%ramesh%' OR email ILIKE '%ramesh%'")
    print("\nRamesh Users:", cur.fetchall())
    
    cur.execute("SELECT id, plan_name, status, chit_type FROM chit_plans")
    print("\nPlans:", cur.fetchall())

    cur.execute("SELECT id, plan_id, user_id, ticket_number, has_won, is_active FROM plan_members")
    print("\nPlan Members:", cur.fetchall())
    
    cur.execute("SELECT id, pronote_id, member_id, chit_id, loan_amount, status FROM promissory_notes")
    print("\nPronotes:", cur.fetchall())
    
    conn.close()
except Exception as e:
    print("Error:", e)

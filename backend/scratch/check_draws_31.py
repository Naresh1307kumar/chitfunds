import os
from dotenv import load_dotenv
load_dotenv('c:/chit fund/backend/.env')
import psycopg2

db_url = os.getenv("DATABASE_URL")
conn = psycopg2.connect(db_url)
cur = conn.cursor()

cur.execute("SELECT * FROM monthly_draws WHERE plan_id = 31")
draws = cur.fetchall()
print("Draws for plan 31:", draws)

conn.close()

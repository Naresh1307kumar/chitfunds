import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:naresh@localhost:5433/Secure')
engine = create_engine(db_url)

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE plan_members ADD COLUMN reason VARCHAR(50) DEFAULT 'personal';"))
        conn.execute(text("ALTER TABLE plan_members ADD COLUMN priority_score INTEGER DEFAULT 5;"))
        conn.commit()
        print("SUCCESS: Columns added to plan_members!")
    except Exception as e:
        print("INFO/ERROR (it may already exist):", str(e))

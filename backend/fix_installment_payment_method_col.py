import sys
import os
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine

def fix_column():
    print("Fixing installments.payment_method column type in PostgreSQL...")
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE installments ALTER COLUMN payment_method TYPE VARCHAR(100) USING payment_method::text;"))
            conn.commit()
            print("[SUCCESS] installments.payment_method column converted to VARCHAR(100) successfully!")
        except Exception as e:
            print(f"[NOTE/ERROR] {e}")

if __name__ == "__main__":
    fix_column()

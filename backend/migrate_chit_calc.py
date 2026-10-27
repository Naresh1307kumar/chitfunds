import sys
import os
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.database import engine

def migrate_database():
    print("Migrating Chit Fund calculation schema...")
    with engine.connect() as conn:
        # Add chit_value to chit_plans if not exists
        try:
            conn.execute(text("ALTER TABLE chit_plans ADD COLUMN IF NOT EXISTS chit_value FLOAT;"))
            conn.execute(text("UPDATE chit_plans SET chit_value = monthly_amount * total_members WHERE chit_value IS NULL;"))
            print("[SUCCESS] Updated chit_plans table with chit_value.")
        except Exception as e:
            print(f"Note on chit_plans: {e}")

        # Add new columns to monthly_draws if not exists
        draw_cols = [
            ("chit_value", "FLOAT DEFAULT 0.0"),
            ("winning_bid_amount", "FLOAT DEFAULT 0.0"),
            ("discount", "FLOAT DEFAULT 0.0"),
            ("company_commission", "FLOAT DEFAULT 0.0"),
            ("net_discount", "FLOAT DEFAULT 0.0"),
            ("dividend_per_member", "FLOAT DEFAULT 0.0"),
            ("net_payable", "FLOAT DEFAULT 0.0"),
        ]

        for col, col_type in draw_cols:
            try:
                conn.execute(text(f"ALTER TABLE monthly_draws ADD COLUMN IF NOT EXISTS {col} {col_type};"))
            except Exception as e:
                print(f"Note on monthly_draws column {col}: {e}")

        conn.commit()
        print("[SUCCESS] Database migration completed successfully!")

if __name__ == "__main__":
    migrate_database()

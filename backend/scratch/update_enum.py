from app.database import engine
from sqlalchemy import text

def update_enum():
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TYPE pronotestatus ADD VALUE IF NOT EXISTS 'pending_signature'"))
            conn.commit()
            print("PostgreSQL ENUM successfully updated!")
        except Exception as e:
            print("Enum alter note:", e)

if __name__ == "__main__":
    update_enum()

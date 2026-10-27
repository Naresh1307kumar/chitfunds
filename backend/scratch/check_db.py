import sqlite3
import json

conn = sqlite3.connect('securechit.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]
print("Tables:", tables)

print("\n--- Users ---")
try:
    cursor.execute("SELECT id, name, email, role FROM users WHERE name LIKE '%ramesh%' OR email LIKE '%ramesh%'")
    print("Ramesh users:", cursor.fetchall())
except Exception as e:
    print("Error querying users:", e)

print("\n--- All Users ---")
try:
    cursor.execute("SELECT id, name, email, role FROM users")
    print(cursor.fetchall())
except Exception as e:
    print("Error querying users:", e)

print("\n--- Plans / Draws / Pronotes sample ---")
for t in ['plans', 'draws', 'pronotes', 'chit_draws', 'auction_winners', 'memberships', 'user_plans']:
    if t in tables:
        try:
            cursor.execute(f"SELECT * FROM {t} LIMIT 5")
            print(f"\nTable {t}:", cursor.fetchall())
        except Exception as e:
            print(f"Error reading {t}:", e)

conn.close()

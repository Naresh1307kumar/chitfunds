import urllib.request
import base64
import json
import shutil
import os

lvl0_td = """flowchart TD
    User["USER / SUBSCRIBER<br/>(Chit Member)"]
    Admin["ADMIN / CHIT FOREMAN<br/>(Chit Manager)"]
    
    Sys(("0.0<br/>SECURE CHIT<br/>MANAGEMENT SYSTEM"))

    Payment["PAYMENT GATEWAY<br/>(Online / UPI)"]
    EmailSMS["FAST2SMS & SMTP GATEWAY<br/>(Alert Services)"]

    %% Flow from Top to Center
    User -->|"Chit Application, Bids, Receipts"| Sys
    Sys -->|"Dynamic Dues, Dividend Statements, Receipts"| User

    Admin -->|"Scheme Specs, Member Approvals, Verifications"| Sys
    Sys -->|"Pending Requests, Auction Summary, Reports"| Admin

    %% Flow from Center to Bottom
    Sys -->|"Payment Authorization Request"| Payment
    Payment -->|"Payment Confirmation Token"| Sys

    Sys -->|"OTP, Due Reminders & Winner Alerts"| EmailSMS
"""

payload = json.dumps({'code': lvl0_td, 'mermaid': {'theme': 'default'}})
encoded = base64.urlsafe_b64encode(payload.encode('utf-8')).decode('ascii')
url = f'https://mermaid.ink/img/{encoded}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

with urllib.request.urlopen(req) as resp:
    data = resp.read()

out_file = os.path.abspath("DFD_Level_0.png")
try:
    with open(out_file, "wb") as f:
        f.write(data)
    print("Saved DFD_Level_0.png successfully!")
except Exception as e:
    print(f"Direct write error: {e}")
    alt_file = os.path.abspath("DFD_Level_0_v2.png")
    with open(alt_file, "wb") as f:
        f.write(data)
    print(f"Saved as {alt_file}")

# Copy to artifacts
artifact_dir = r"C:\Users\nares\.gemini\antigravity\brain\454c2f6d-d632-4132-98eb-c6e47ea84a85"
with open(os.path.join(artifact_dir, "DFD_Level_0.png"), "wb") as f:
    f.write(data)

with open("level0_dfd.mmd", "w", encoding="utf-8") as f:
    f.write(lvl0_td)

print("Done updating Top-Down Level 0!")

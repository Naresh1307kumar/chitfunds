import urllib.request
import base64
import json
import shutil
import os

lvl0_code = """flowchart LR
    User["USER / SUBSCRIBER<br/>(Chit Member)"]
    Admin["ADMIN / CHIT FOREMAN<br/>(Chit Manager)"]
    Payment["PAYMENT GATEWAY<br/>(Online / UPI)"]
    EmailSMS["FAST2SMS & SMTP GATEWAY<br/>(Alert Services)"]
    Sys(("0.0<br/>SECURE CHIT<br/>MANAGEMENT SYSTEM"))

    User -->|"Chit Application, Bids, Receipts"| Sys
    Sys -->|"Dynamic Dues, Dividend Statements, Receipts"| User

    Admin -->|"Scheme Specs, Member Approvals, Verifications"| Sys
    Sys -->|"Pending Requests, Auction Summary, Reports"| Admin

    Sys -->|"Payment Authorization Request"| Payment
    Payment -->|"Payment Confirmation Token"| Sys

    Sys -->|"OTP, Due Reminders & Winner Alerts"| EmailSMS
"""

payload = json.dumps({'code': lvl0_code, 'mermaid': {'theme': 'default'}})
encoded = base64.urlsafe_b64encode(payload.encode('utf-8')).decode('ascii')
url = f'https://mermaid.ink/img/{encoded}'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

with urllib.request.urlopen(req) as resp, open('DFD_Level_0.png', 'wb') as f:
    f.write(resp.read())

print("Successfully saved DFD_Level_0.png!")

# Copy to artifacts directory as well
artifact_dir = r'C:\Users\nares\.gemini\antigravity\brain\454c2f6d-d632-4132-98eb-c6e47ea84a85'
shutil.copy('DFD_Level_0.png', os.path.join(artifact_dir, 'DFD_Level_0.png'))
print("Copied to artifacts directory!")

with open("level0_dfd.mmd", "w", encoding="utf-8") as f:
    f.write(lvl0_code)
print("Updated level0_dfd.mmd!")

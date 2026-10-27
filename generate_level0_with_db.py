import urllib.request
import base64
import json
import shutil
import os

bw_theme = {
    "theme": "base",
    "themeVariables": {
        "primaryColor": "#ffffff",
        "primaryTextColor": "#000000",
        "primaryBorderColor": "#000000",
        "lineColor": "#000000",
        "secondaryColor": "#ffffff",
        "tertiaryColor": "#ffffff",
        "mainBkg": "#ffffff",
        "nodeBorder": "#000000",
        "clusterBkg": "#ffffff",
        "clusterBorder": "#000000",
        "edgeLabelBackground": "#ffffff",
        "nodeTextColor": "#000000"
    }
}

lvl0_code = """flowchart TD
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    linkStyle default stroke:#000000,stroke-width:1.5px;

    User["USER / SUBSCRIBER<br/>(Chit Member)"]
    Admin["ADMIN / CHIT FOREMAN<br/>(Chit Manager)"]
    
    Sys(("0.0<br/>SECURE CHIT<br/>MANAGEMENT SYSTEM"))

    DB[("POSTGRESQL DATABASE<br/>(Central Relational Store)")]
    Payment["PAYMENT GATEWAY<br/>(Online / UPI)"]
    EmailSMS["FAST2SMS and SMTP GATEWAY<br/>(Alert Services)"]

    %% User & Admin Flows
    User -->|"Chit Application, Bids, Receipts"| Sys
    Sys -->|"Dynamic Dues, Dividend Statements, Receipts"| User

    Admin -->|"Scheme Specs, Member Approvals, Verifications"| Sys
    Sys -->|"Pending Requests, Auction Summary, Reports"| Admin

    %% Database Flows
    Sys -->|"Save / Update Records"| DB
    DB -->|"Fetch Stored Data and Queries"| Sys

    %% External Services Flows
    Sys -->|"Payment Authorization Request"| Payment
    Payment -->|"Payment Confirmation Token"| Sys

    Sys -->|"OTP, Due Reminders and Winner Alerts"| EmailSMS
"""

payload = json.dumps({'code': lvl0_code, 'mermaid': bw_theme})
encoded = base64.urlsafe_b64encode(payload.encode('utf-8')).decode('ascii')
url = f"https://mermaid.ink/img/{encoded}"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

with urllib.request.urlopen(req) as resp:
    data = resp.read()

output_file = "DFD_Level_0.png"
if os.path.exists(output_file):
    try:
        os.remove(output_file)
    except Exception:
        pass

with open(output_file, "wb") as f:
    f.write(data)

# Copy to artifacts directory
artifact_dir = r"C:\Users\nares\.gemini\antigravity\brain\454c2f6d-d632-4132-98eb-c6e47ea84a85"
try:
    with open(os.path.join(artifact_dir, "DFD_Level_0.png"), "wb") as f:
        f.write(data)
except Exception:
    pass

with open("level0_dfd.mmd", "w", encoding="utf-8") as f:
    f.write(lvl0_code)

print("Generated DFD_Level_0.png with PostgreSQL Database successfully!")

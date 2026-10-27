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

def render_bw_mermaid(code, output_file):
    payload = json.dumps({'code': code, 'mermaid': bw_theme})
    encoded = base64.urlsafe_b64encode(payload.encode('utf-8')).decode('ascii')
    url = f"https://mermaid.ink/img/{encoded}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
    if os.path.exists(output_file):
        try:
            os.remove(output_file)
        except Exception:
            pass
    with open(output_file, "wb") as f:
        f.write(data)
    print(f"Generated {output_file} in Black & White!")

# LEVEL 0 (Top-Down, Pure B&W)
lvl0_bw = """flowchart TD
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    linkStyle default stroke:#000000,stroke-width:1.5px;

    User["USER / SUBSCRIBER<br/>(Chit Member)"]
    Admin["ADMIN / CHIT FOREMAN<br/>(Chit Manager)"]
    
    Sys(("0.0<br/>SECURE CHIT<br/>MANAGEMENT SYSTEM"))

    Payment["PAYMENT GATEWAY<br/>(Online / UPI)"]
    EmailSMS["FAST2SMS and SMTP GATEWAY<br/>(Alert Services)"]

    %% Flow from Top to Center
    User -->|"Chit Application, Bids, Receipts"| Sys
    Sys -->|"Dynamic Dues, Dividend Statements, Receipts"| User

    Admin -->|"Scheme Specs, Member Approvals, Verifications"| Sys
    Sys -->|"Pending Requests, Auction Summary, Reports"| Admin

    %% Flow from Center to Bottom
    Sys -->|"Payment Authorization Request"| Payment
    Payment -->|"Payment Confirmation Token"| Sys

    Sys -->|"OTP, Due Reminders and Winner Alerts"| EmailSMS
"""

# LEVEL 1 (Pure B&W)
lvl1_bw = """flowchart TD
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    linkStyle default stroke:#000000,stroke-width:1.5px;

    Subscriber["USER / SUBSCRIBER"]
    Admin["ADMIN / CHIT FOREMAN"]
    SMSGateway["FAST2SMS / EMAIL GATEWAY"]

    P1(("1.0<br/>User Auth and<br/>Role Control"))
    P2(("2.0<br/>Chit Scheme<br/>Management"))
    P3(("3.0<br/>Reverse Auction and<br/>Dividend Engine"))
    P4(("4.0<br/>Installment Payment<br/>and Verification"))
    P5(("5.0<br/>Automated Due and<br/>Reminder Scheduler"))

    D1[("D1: USERS STORE")]
    D2[("D2: CHIT SCHEMES STORE")]
    D3[("D3: BIDS STORE")]
    D4[("D4: PAYMENTS STORE")]
    D5[("D5: NOTIFICATIONS STORE")]

    Subscriber -->|"Login Info"| P1
    P1 -->|"Save Profile"| D1

    Admin -->|"Create Scheme Specs"| P2
    P2 -->|"Save Config"| D2

    Subscriber -->|"Submit Auction Bid"| P3
    D2 -->|"Fetch Pool Specs"| P3
    P3 -->|"Save Winning Bid"| D3

    Subscriber -->|"Upload Receipt Ref"| P4
    Admin -->|"Approve Receipt"| P4
    P4 -->|"Update Status to PAID"| D4

    P5 -->|"Scan Dues Near Expiry"| D4
    P5 -->|"Fetch Member Contacts"| D1
    P5 -->|"Trigger SMS and Emails"| SMSGateway
    P5 -->|"Log Dispatch Status"| D5
"""

# LEVEL 2 (Pure B&W)
lvl2_bw = """flowchart TD
    classDef default fill:#ffffff,stroke:#000000,stroke-width:1.5px,color:#000000;
    linkStyle default stroke:#000000,stroke-width:1.5px;

    Subscriber["USER / SUBSCRIBER"]
    Admin["ADMIN / CHIT FOREMAN"]
    D2[("D2: CHIT SCHEMES STORE")]
    D3[("D3: BIDS STORE")]
    D4[("D4: PAYMENTS STORE")]

    P3_1(("3.1<br/>Validate and Entry<br/>Auction Bid"))
    P3_2(("3.2<br/>Compute Foreman Fee<br/>and Dividend Pool"))
    P3_3(("3.3<br/>Calculate Member Share<br/>and Net Payable"))
    
    P4_1(("4.1<br/>Submit Payment<br/>Ref / Receipt"))
    P4_2(("4.2<br/>Admin Verification and<br/>Ledger Status Update"))

    InBid[/"Discount Bid Amount"/]
    OutDividend[/"Member Dividend and Net Due"/]
    InReceipt[/"Bank / UPI Txn Ref"/]

    Subscriber --> InBid
    InBid --> P3_1
    D2 -->|"Max Cap Check"| P3_1
    P3_1 -->|"Store Valid Bid"| D3
    P3_1 --> P3_2

    P3_2 -->|"Net Dividend = Discount - 5% Fee"| P3_3
    P3_3 --> OutDividend
    OutDividend -->|"Save Monthly Payable"| D4

    Subscriber --> InReceipt
    InReceipt --> P4_1
    P4_1 -->|"Set Status: SUBMITTED"| D4
    Admin -->|"Inspect Reference and Confirm"| P4_2
    P4_2 -->|"Set Status: PAID"| D4
"""

if __name__ == "__main__":
    render_bw_mermaid(lvl0_bw, "DFD_Level_0.png")
    render_bw_mermaid(lvl1_bw, "DFD_Level_1.png")
    render_bw_mermaid(lvl2_bw, "DFD_Level_2.png")

    artifact_dir = r"C:\Users\nares\.gemini\antigravity\brain\454c2f6d-d632-4132-98eb-c6e47ea84a85"
    for img in ["DFD_Level_0.png", "DFD_Level_1.png", "DFD_Level_2.png"]:
        shutil.copy(img, os.path.join(artifact_dir, img))

    with open("level0_dfd.mmd", "w", encoding="utf-8") as f:
        f.write(lvl0_bw)
    with open("level1_dfd.mmd", "w", encoding="utf-8") as f:
        f.write(lvl1_bw)
    with open("level2_dfd.mmd", "w", encoding="utf-8") as f:
        f.write(lvl2_bw)

    print("All diagrams regenerated in Black & White successfully!")

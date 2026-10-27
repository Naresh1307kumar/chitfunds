import re

with open(r'C:\chit fund\SecureChit_Full_Project_Report.md', 'r', encoding='utf-8') as f:
    content = f.read()

level0 = """
```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'lineColor': '#000000', 'textColor': '#000000', 'primaryBorderColor': '#000000', 'primaryColor': '#ffffff', 'fontFamily': 'arial'}}}%%
flowchart TD
    classDef default fill:#fff,stroke:#000,stroke-width:2px,color:#000,font-weight:bold;
    
    User["USER"]
    Admin["ADMIN"]
    DB[("POSTGRESQL DATABASE\\n(Central Relational Store)")]
    PG["PAYMENT GATEWAY\\n(Online / UPI)"]
    SMS["FAST2SMS and SMTP\\nGATEWAY\\n(Alert Services)"]
    
    System(("0.0\\nSECURE CHIT\\nMANAGEMENT SYSTEM"))

    User -- "Chit Application, Bids,\\nReceipts" --> System
    System -- "Dynamic Dues, Dividend\\nStatements, Receipts" --> User

    Admin -- "Pending Requests, Auction\\nSummary, Reports" --> System
    System -- "Alerts, Member\\nVerification" --> Admin

    System -- "Save / Update Record" --> DB
    DB -- "Fetch Stored Data and\\nQueries" --> System

    System -- "Payment Auth\\nRequest" --> PG
    PG -- "Payment Confirmation\\nToken" --> System

    System -- "OTP, Due Reminders and\\nWinner Alerts" --> SMS
```
"""

level1 = """
```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'lineColor': '#000000', 'textColor': '#000000', 'primaryBorderColor': '#000000', 'primaryColor': '#ffffff', 'fontFamily': 'arial'}}}%%
flowchart TD
    classDef default fill:#fff,stroke:#000,stroke-width:2px,color:#000,font-weight:bold;

    Admin["ADMIN"]
    User["USER"]
    SMS["FAST2SMS / EMAIL\\nGATEWAY"]

    P2(("2.0\\nChit Scheme\\nManagement"))
    P3(("3.0\\nReverse Auction and\\nDividend Engine"))
    P4(("4.0\\nInstallment Payment\\nand Verification"))
    P1(("1.0\\nUser Auth and\\nRole Control"))
    P5(("5.0\\nAutomated Due and\\nReminder Scheduler"))

    D2[("D2: CHIT SCHEMES\\nSTORE")]
    D3[("D3: BIDS STORE")]
    D4[("D4: PAYMENTS STORE")]
    D1[("D1: USERS STORE")]
    D6[("D5: NOTIFICATIONS\\nSTORE")]

    Admin -- "Create Scheme Specs" --> P2
    P2 -- "Save Config" --> D2

    User -- "Submit Auction Bid" --> P3
    D2 -- "Fetch Pool Specs" --> P3
    P3 -- "Save Winning Bid" --> D3

    User -- "Upload Receipt Ref" --> P4
    Admin -- "Approve Receipt" --> P4
    P4 -- "Update Status to PAID" --> D4

    User -- "Login Info" --> P1
    P1 -- "Save Profile" --> D1

    P5 -- "Scan Dues Near Expiry" --> D4
    P5 -- "Fetch Member Contacts" --> D1
    P5 -- "Trigger SMS and Emails" --> SMS
    P5 -- "Log Dispatch Status" --> D6
```
"""

level2 = """
```mermaid
%%{init: {'theme': 'base', 'themeVariables': {'lineColor': '#000000', 'textColor': '#000000', 'primaryBorderColor': '#000000', 'primaryColor': '#ffffff', 'fontFamily': 'arial'}}}%%
flowchart TD
    classDef default fill:#fff,stroke:#000,stroke-width:2px,color:#000,font-weight:bold;

    User["USER"]
    Admin["ADMIN"]

    BidInput[/"Discount Bid Amount"/]
    TxnInput[/"Bank / UPI Txn Ref"/]
    Output[/"Member Dividend and Net Due"/]

    D2[("D2: CHIT SCHEMES\\nSTORE")]
    D3[("D3: BIDS STORE")]
    D4[("D4: PAYMENTS STORE")]

    P31(("3.1\\nValidate and Entry\\nAuction Bid"))
    P32(("3.2\\nCompute Foreman Fee\\nand Dividend Pool"))
    P33(("3.3\\nCalculate Member Share\\nand Net Payable"))
    P41(("4.1\\nSubmit Payment\\nRef / Receipt"))
    P42(("4.2\\nAdmin Verification and\\nLedger Status Update"))

    User --> BidInput
    BidInput --> P31
    D2 -- "Max Cap Check" --> P31
    P31 -- "Store Valid Bid" --> D3
    P31 --> P32
    P32 -- "Net Dividend = Discount -\\n5% Fee" --> P33
    P33 --> Output

    User --> TxnInput
    TxnInput --> P41
    P41 -- "Set Status: SUBMITTED" --> D4

    Admin -- "Inspect Reference and\\nConfirm" --> P42
    P42 -- "Set Status: PAID" --> D4
```
"""

content = content.replace("![Level 0 DFD](dfd_level_0.png)", level0)
content = content.replace("![Level 1 DFD](dfd_level_1.png)", level1)
content = content.replace("![Level 2 DFD](dfd_level_2.png)", level2)

with open(r'C:\chit fund\SecureChit_Report_v10.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Created SecureChit_Report_v10.md successfully!")

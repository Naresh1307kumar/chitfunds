import os

level0_mmd = """flowchart LR
    %% External Entities (Rectangles)
    Subscriber["USER / SUBSCRIBER"]
    Admin["ADMIN / CHIT FOREMAN"]
    SMSGateway["FAST2SMS API GATEWAY"]
    EmailGateway["SMTP EMAIL GATEWAY"]

    %% Central Process (Circle)
    CentralProcess(("0.0<br/>SECURE CHIT<br/>MANAGEMENT SYSTEM"))

    %% Data Flows
    Subscriber -->|"Join Request, Bids, Receipts"| CentralProcess
    CentralProcess -->|"Dynamic Dues, Dividend Statements"| Subscriber

    Admin -->|"Scheme Specs, Approvals"| CentralProcess
    CentralProcess -->|"Pending Requests, Risk Stats"| Admin

    CentralProcess -->|"SMS Alerts"| SMSGateway
    CentralProcess -->|"Email Alerts"| EmailGateway
"""

level1_mmd = """flowchart TD
    %% External Entities (Rectangles)
    Subscriber["USER / SUBSCRIBER"]
    Admin["ADMIN / CHIT FOREMAN"]
    SMSGateway["FAST2SMS / EMAIL GATEWAY"]

    %% Main Functional Processes (Circles)
    P1(("1.0<br/>User Auth &<br/>Role Control"))
    P2(("2.0<br/>Chit Scheme<br/>Management"))
    P3(("3.0<br/>Reverse Auction &<br/>Dividend Engine"))
    P4(("4.0<br/>Installment Payment<br/>& Verification"))
    P5(("5.0<br/>Automated Due &<br/>Reminder Scheduler"))

    %% Data Stores (Cylinders)
    D1[( "D1: USERS STORE" )]
    D2[( "D2: CHIT SCHEMES STORE" )]
    D3[( "D3: BIDS STORE" )]
    D4[( "D4: PAYMENTS STORE" )]
    D5[( "D5: NOTIFICATIONS STORE" )]

    %% Data Flows
    Subscriber -->|"Login Info"| P1
    P1 -->|"Save Profile"| D1

    Admin -->|"Create Scheme Specs"| P2
    P2 -->|"Save Config"| D2

    Subscriber -->|"Submit Auction Bid"| P3
    D2 -->|"Fetch Pool Specs"| P3
    P3 -->|"Save Winning Bid"| D3

    Subscriber -->|"Upload Receipt Ref"| P4
    Admin -->|"Approve Receipt"| P4
    P4 -->|"Update Status ('PAID')"| D4

    P5 -->|"Scan Dues (24h)"| D4
    P5 -->|"Fetch Member Contacts"| D1
    P5 -->|"Trigger SMS & Emails"| SMSGateway
    P5 -->|"Log Dispatch Status"| D5
"""

level2_mmd = """flowchart TD
    %% External Entities & Stores
    Subscriber["USER / SUBSCRIBER"]
    Admin["ADMIN / CHIT FOREMAN"]
    D2[( "D2: CHIT SCHEMES STORE" )]
    D3[( "D3: BIDS STORE" )]
    D4[( "D4: PAYMENTS STORE" )]

    %% Sub-Processes (Circles)
    P3_1(("3.1<br/>Validate & Entry<br/>Auction Bid"))
    P3_2(("3.2<br/>Compute Foreman Fee<br/>& Dividend Pool"))
    P3_3(("3.3<br/>Calculate Member Share<br/>& Net Payable"))
    
    P4_1(("4.1<br/>Submit Payment<br/>Ref / Receipt"))
    P4_2(("4.2<br/>Admin Verification &<br/>Ledger Status Update"))

    %% Inputs / Outputs (Parallelograms)
    InBid[/ "Discount Bid Amount" /]
    OutDividend[/ "Member Dividend & Net Due" /]
    InReceipt[/ "Bank / UPI Txn Ref" /]

    %% Workflows
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
    Admin -->|"Inspect Reference & Confirm"| P4_2
    P4_2 -->|"Set Status: PAID"| D4
"""

with open("level0_dfd.mmd", "w", encoding="utf-8") as f:
    f.write(level0_mmd)

with open("level1_dfd.mmd", "w", encoding="utf-8") as f:
    f.write(level1_mmd)

with open("level2_dfd.mmd", "w", encoding="utf-8") as f:
    f.write(level2_mmd)

print("Exported level0_dfd.mmd, level1_dfd.mmd, level2_dfd.mmd successfully!")

import os

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SecureChit - Data Flow Diagrams (DFD)</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'neutral',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }
        });
    </script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8fafc;
            color: #0f172a;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        h1 {
            color: #103c58;
            text-align: center;
            margin-bottom: 10px;
        }
        h2 {
            color: #03739e;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 8px;
            margin-top: 30px;
        }
        .diagram-box {
            background: #f1f5f9;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 20px;
            margin-top: 15px;
            display: flex;
            justify-content: center;
            overflow-x: auto;
        }
        .info-card {
            background: #f0f9ff;
            border-left: 4px solid #03739e;
            padding: 12px 16px;
            margin-bottom: 20px;
            border-radius: 4px;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>SECURE CHIT: DATA FLOW DIAGRAMS (DFD)</h1>
        <p style="text-align: center; color: #64748b;">Automated Level 0, Level 1 & Level 2 Diagrams</p>

        <div class="info-card">
            <strong>DFD Symbol Key:</strong>
            Rectangles = External Entities | Circles = Processes | Cylinders = Data Stores | Parallelograms = Inputs/Outputs
        </div>

        <!-- LEVEL 0 DFD -->
        <h2>Level 0 DFD (Context Diagram)</h2>
        <div class="diagram-box">
            <pre class="mermaid">
flowchart LR
    Subscriber["USER / SUBSCRIBER"]
    Admin["ADMIN / CHIT FOREMAN"]
    SMSGateway["FAST2SMS API GATEWAY"]
    EmailGateway["SMTP EMAIL GATEWAY"]

    CentralProcess(("0.0<br/>SECURE CHIT<br/>MANAGEMENT SYSTEM"))

    Subscriber -->|"Join Request, Bids, Receipts"| CentralProcess
    CentralProcess -->|"Dynamic Dues, Dividend Statements"| Subscriber

    Admin -->|"Scheme Specs, Approvals"| CentralProcess
    CentralProcess -->|"Pending Requests, Risk Stats"| Admin

    CentralProcess -->|"SMS Alerts"| SMSGateway
    CentralProcess -->|"Email Alerts"| EmailGateway
            </pre>
        </div>

        <!-- LEVEL 1 DFD -->
        <h2>Level 1 DFD (System Modules & Data Stores)</h2>
        <div class="diagram-box">
            <pre class="mermaid">
flowchart TD
    Subscriber["USER / SUBSCRIBER"]
    Admin["ADMIN / CHIT FOREMAN"]
    SMSGateway["FAST2SMS / EMAIL GATEWAY"]

    P1(("1.0<br/>User Auth &<br/>Role Control"))
    P2(("2.0<br/>Chit Scheme<br/>Management"))
    P3(("3.0<br/>Reverse Auction &<br/>Dividend Engine"))
    P4(("4.0<br/>Installment Payment<br/>& Verification"))
    P5(("5.0<br/>Automated Due &<br/>Reminder Scheduler"))

    D1[( "D1: USERS STORE" )]
    D2[( "D2: CHIT SCHEMES STORE" )]
    D3[( "D3: BIDS STORE" )]
    D4[( "D4: PAYMENTS STORE" )]
    D5[( "D5: NOTIFICATIONS STORE" )]

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
            </pre>
        </div>

        <!-- LEVEL 2 DFD -->
        <h2>Level 2 DFD (Reverse Auction & Payment Verification)</h2>
        <div class="diagram-box">
            <pre class="mermaid">
flowchart TD
    Subscriber["USER / SUBSCRIBER"]
    Admin["ADMIN / CHIT FOREMAN"]
    D2[( "D2: CHIT SCHEMES STORE" )]
    D3[( "D3: BIDS STORE" )]
    D4[( "D4: PAYMENTS STORE" )]

    P3_1(("3.1<br/>Validate & Entry<br/>Auction Bid"))
    P3_2(("3.2<br/>Compute Foreman Fee<br/>& Dividend Pool"))
    P3_3(("3.3<br/>Calculate Member Share<br/>& Net Payable"))
    
    P4_1(("4.1<br/>Submit Payment<br/>Ref / Receipt"))
    P4_2(("4.2<br/>Admin Verification &<br/>Ledger Status Update"))

    InBid[/ "Discount Bid Amount" /]
    OutDividend[/ "Member Dividend & Net Due" /]
    InReceipt[/ "Bank / UPI Txn Ref" /]

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
            </pre>
        </div>
    </div>
</body>
</html>
"""

with open("all_dfd_diagrams.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("Generated all_dfd_diagrams.html successfully!")

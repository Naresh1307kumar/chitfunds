import base64
import requests
from pptx import Presentation
from pptx.util import Inches, Pt
import os

user_mermaid = """flowchart LR
    USER(("👤 USER (Member)")) 
    A[Registration on Web Portal]
    B[Submit KYC Documents]
    C{Admin KYC Approval?}
    D[Browse & Join Chit Plan]
    E[Pay First Installment via Razorpay]
    F[Participate in Monthly Live Reverse Auction]
    G{Bid & AI Emergency Priority}
    H[Declared as Auction Winner]
    I[Wait for Next Month]
    J[System Auto-Generates Promissory Note]
    K[Draw Digital Signature via HTML5 Canvas]
    L{Admin Verifies Signature?}
    M([Receive Prize Money Disbursal])
    N[Pay Subsequent Dues with Automated Dividends]

    USER ==> A
    A --> B --> C
    C -- Rejected --> B
    C -- Approved --> D
    D --> E --> F
    F --> G
    G -- Wins --> H
    G -- Loses --> I
    I -.->|Next Month| F
    H --> J --> K --> L
    L -- Invalid --> K
    L -- Valid --> M
    M --> N
    N -.->|Monthly Loop| N
    
    style USER fill:#ff9800,stroke:#e65100,stroke-width:4px,color:#fff,font-size:20px,font-weight:bold
"""

admin_mermaid = """flowchart LR
    ADMIN(("👨‍💼 ADMIN (Foreman)")) 
    A[Review New Member Registrations]
    B{Verify KYC Aadhaar/PAN}
    C[Create Chit Groups & Set Schedules]
    D[Allocate Slots to Approved Members]
    E[Monitor Monthly Live Reverse Auction]
    F[Review AI Emergency Priority Requests]
    G[Declare Auction Winner]
    H[System Calculates 5% Commission & Dividends]
    I[Winner Signs Digital Promissory Note]
    J{Verify Promissory Note Signature?}
    K[Initiate Prize Money Disbursal]
    L[Track Monthly Installments & UPI Payments]
    M[Maintain Database Audit Logs & Reports]

    ADMIN ==> A
    A --> B
    B -- Reject --> A
    B -- Approve --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    I --> J
    J -- Invalid --> I
    J -- Valid --> K
    K --> L
    L --> M
    M -.->|Next Month Loop| E
    
    style ADMIN fill:#1565c0,stroke:#0d47a1,stroke-width:4px,color:#fff,font-size:20px,font-weight:bold
"""

integrated_mermaid = """flowchart LR
    classDef user fill:#e8f5e9,stroke:#4caf50,stroke-width:2px;
    classDef admin fill:#e3f2fd,stroke:#2196f3,stroke-width:2px;
    classDef system fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;

    subgraph USER ["👤 USER (Member)"]
        direction LR
        U1[Submit KYC Documents]
        U2[Join Chit Plan & Pay]
        U3[Participate in Live Auction / Bid]
        U4[Sign Digital Promissory Note]
        U5[Receive Prize Amount]
        U6[Pay Subsequent Monthly Dues]
    end

    subgraph SYSTEM ["💻 SECURECHIT SYSTEM"]
        direction LR
        S1[AI Evaluates Priority & Declares Winner]
        S2[Auto-Generate Promissory Note]
        S3[Calculate 5% Commission & Dividends]
    end

    subgraph ADMIN ["👨‍💼 ADMIN (Foreman)"]
        direction LR
        A1[Verify & Approve KYC]
        A2[Create Chit Groups]
        A3[Monitor Live Auction]
        A4[Verify Digital Signature]
        A5[Disburse Prize Money]
        A6[Track Payments & Audit Ledger]
    end

    class U1,U2,U3,U4,U5,U6 user;
    class S1,S2,S3 system;
    class A1,A2,A3,A4,A5,A6 admin;

    U1 -->|Requires Approval| A1
    A1 -->|Approval Status| U2
    A2 -.->|Available Plans| U2
    
    U2 --> U3
    U3 -->|Submit Bid| S1
    S1 -->|Notify Status| A3
    
    S1 --> S2
    S2 -->|Require Signature| U4
    U4 -->|Submit Signature| A4
    
    A4 -->|If Signature Valid| A5
    A5 -->|Transfer Funds| U5
    
    A5 --> S3
    S3 -->|Apply Discount| U6
    U6 -->|Online Payment| A6
    A6 -.->|Start Next Month Auction| U3
"""

def download_mermaid(code, filename):
    encoded = base64.b64encode(code.encode('utf-8')).decode('utf-8')
    url = f"https://mermaid.ink/img/{encoded}?type=png"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    else:
        print(f"Error downloading {filename}: {response.status_code} {response.text}")
        return False

def main():
    prs = Presentation()
    
    diagrams = [
        ("User (Member) Detailed Workflow", user_mermaid, "user_flow_lr.png"),
        ("Admin (Foreman) Detailed Workflow", admin_mermaid, "admin_flow_lr.png"),
        ("Integrated System Workflow", integrated_mermaid, "integrated_flow_lr.png")
    ]
    
    for title, code, img_file in diagrams:
        print(f"Downloading {img_file}...")
        if download_mermaid(code, img_file):
            slide_layout = prs.slide_layouts[5] # Blank / Title only
            slide = prs.slides.add_slide(slide_layout)
            
            try:
                title_shape = slide.shapes.title
                title_shape.text = title
            except:
                pass
                
            try:
                # Add picture horizontally. Since it's horizontal, width is the constraint
                # Width 9.5 out of 10 leaves 0.25 on each side
                pic = slide.shapes.add_picture(img_file, Inches(0.25), Inches(1.5), width=Inches(9.5))
            except Exception as e:
                print(f"Error adding picture {img_file}: {e}")
                
    out_path = r"C:\chit fund\SecureChit_Workflow_Diagrams_v4.pptx"
    prs.save(out_path)
    print(f"SUCCESS: {out_path}")

if __name__ == "__main__":
    main()

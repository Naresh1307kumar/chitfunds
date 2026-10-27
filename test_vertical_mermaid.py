import urllib.request
import base64
import json
import os

bw_theme = {
    "theme": "base",
    "themeVariables": {
        "primaryColor": "#ffffff",
        "primaryTextColor": "#0f172a",
        "primaryBorderColor": "#0f172a",
        "lineColor": "#0f172a",
        "secondaryColor": "#ffffff",
        "tertiaryColor": "#ffffff",
        "mainBkg": "#ffffff",
        "nodeBorder": "#0f172a",
        "clusterBkg": "#ffffff",
        "clusterBorder": "#ffffff",
        "edgeLabelBackground": "#ffffff",
        "nodeTextColor": "#0f172a",
        "fontFamily": "arial",
        "fontSize": "14px"
    }
}

lvl0_vertical = """flowchart TD
    classDef default fill:#ffffff,stroke:#0f172a,stroke-width:2px,color:#0f172a;
    linkStyle default stroke:#0f172a,stroke-width:2px;

    subgraph TopActors [" "]
        User["<b>USER / SUBSCRIBER</b><br/>(Chit Member)<br/><i>[External Entity]</i>"]
        Admin["<b>ADMIN / FOREMAN</b><br/>(Chit Manager)<br/><i>[External Entity]</i>"]
    end

    Sys(("<b>0.0</b><br/><b>SECURE CHIT</b><br/><b>MANAGEMENT SYSTEM</b>"))
    DB[("<b>D1: POSTGRESQL DATABASE</b><br/>(Central Relational Store)")]

    User -->|"Chit Application, Bids, UPI UTR"| Sys
    Sys -->|"Due Alerts, Dividend Statements"| User

    Admin -->|"Scheme Specs, KYC Approvals"| Sys
    Sys -->|"Reports, Signed Pronotes"| Admin

    Sys -->|"Save / Update Records"| DB
    DB -->|"Fetch Stored Data"| Sys

    style TopActors fill:#ffffff,stroke:none;
"""

payload = json.dumps({'code': lvl0_vertical, 'mermaid': bw_theme})
encoded = base64.urlsafe_b64encode(payload.encode('utf-8')).decode('ascii')
url = f"https://mermaid.ink/img/{encoded}?scale=2"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
    with open("DFD_Level_0_Mermaid_Vertical.png", "wb") as f:
        f.write(data)
    print("Saved DFD_Level_0_Mermaid_Vertical.png")
except Exception as e:
    print("Error:", e)

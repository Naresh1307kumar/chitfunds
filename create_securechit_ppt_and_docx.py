import sys
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

from pptx import Presentation
from pptx.util import Inches as PptInches, Pt as PptPt
from pptx.dml.color import RGBColor as PptRGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==============================================================================
# 1. PPT GENERATOR (25 SLIDES)
# ==============================================================================

def generate_ppt():
    prs = Presentation()
    prs.slide_width = PptInches(13.333)
    prs.slide_height = PptInches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme Colors
    NAVY = PptRGBColor(16, 60, 88)         # #103C58 Primary
    CYAN = PptRGBColor(3, 115, 158)        # #03739E Secondary
    DARK_BLUE = PptRGBColor(6, 31, 61)     # #061F3D Text/Card Dark
    LIGHT_BG = PptRGBColor(240, 246, 250)  # Off-white / Soft Cyan
    WHITE = PptRGBColor(255, 255, 255)
    GOLD = PptRGBColor(217, 119, 6)
    SLATE = PptRGBColor(51, 65, 85)

    def add_bg(slide, color=WHITE):
        shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, PptInches(0), PptInches(0), PptInches(13.333), PptInches(7.5))
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.color.rgb = color
        return shape

    def add_header(slide, title_text, category_text="SECURE CHIT FUND MANAGEMENT SYSTEM"):
        tb = slide.shapes.add_textbox(PptInches(0.8), PptInches(0.4), PptInches(11.7), PptInches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = PptPt(11)
        p0.font.bold = True
        p0.font.color.rgb = CYAN
        
        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = PptPt(24)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

    def add_card(slide, left, top, width, height, title, items, bg_color=LIGHT_BG, border_color=CYAN, title_color=NAVY, font_size=13):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = PptPt(1.5)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = PptInches(0.25)
        tf.margin_right = PptInches(0.25)
        tf.margin_top = PptInches(0.25)
        tf.margin_bottom = PptInches(0.25)

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = PptPt(16)
        p0.font.bold = True
        p0.font.color.rgb = title_color
        p0.space_after = PptPt(8)

        for item in items:
            p = tf.add_paragraph()
            p.text = f"• {item}" if not item.startswith("  ") else f"   {item}"
            p.font.size = PptPt(font_size)
            p.font.color.rgb = SLATE
            p.space_after = PptPt(5)
        return shape

    # SLIDE 1: Title Slide
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, NAVY)

    if os.path.exists("thiagarajar_college_logo.png"):
        s1.shapes.add_picture("thiagarajar_college_logo.png", PptInches(5.9), PptInches(0.3), width=PptInches(1.5))

    tb1 = s1.shapes.add_textbox(PptInches(1.0), PptInches(1.9), PptInches(11.333), PptInches(5.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "SECURE CHIT"
    p0.alignment = PP_ALIGN.CENTER
    p0.font.size = PptPt(36)
    p0.font.bold = True
    p0.font.color.rgb = WHITE

    p1 = tf1.add_paragraph()
    p1.text = "DIGITAL CHIT FUND MANAGEMENT SYSTEM"
    p1.alignment = PP_ALIGN.CENTER
    p1.font.size = PptPt(20)
    p1.font.bold = True
    p1.font.color.rgb = GOLD
    p1.space_after = PptPt(14)

    p2 = tf1.add_paragraph()
    p2.text = "Submitted in partial fulfilment of the requirements for the award of the degree of\nBachelor of Science in Computer Science"
    p2.alignment = PP_ALIGN.CENTER
    p2.font.size = PptPt(13)
    p2.font.color.rgb = WHITE
    p2.space_after = PptPt(14)

    p3 = tf1.add_paragraph()
    p3.text = "Submitted By:\nR. NARESHKUMAR (24UCS08) | APR. JEGATHEESH VARSHAN (24UCS06)\n\nUnder the Guidance of:\nMrs. S. M. VALLI B.E., M.C.A., M.Phil"
    p3.alignment = PP_ALIGN.CENTER
    p3.font.size = PptPt(13)
    p3.font.bold = True
    p3.font.color.rgb = WHITE
    p3.space_after = PptPt(14)

    p4 = tf1.add_paragraph()
    p4.text = "DEPARTMENT OF COMPUTER SCIENCE | THIAGARAJAR COLLEGE (AUTONOMOUS)\n(Affiliated to Madurai Kamaraj University) | Re-accredited with 'A++' Grade by NAAC | Ranked 20th in NIRF 2026\nMadurai – 625009 | October – 2026"
    p4.alignment = PP_ALIGN.CENTER
    p4.font.size = PptPt(11)
    p4.font.color.rgb = WHITE

    # SLIDE 2: Bonafide Certificate
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2)
    add_header(s2, "BONAFIDE CERTIFICATE")

    if os.path.exists("thiagarajar_college_logo.png"):
        s2.shapes.add_picture("thiagarajar_college_logo.png", PptInches(11.3), PptInches(0.3), width=PptInches(1.2))

    add_card(s2, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "Thiagarajar College (Autonomous) - Department of Computer Science",
             [
                 "Re-Accredited with 'A++' Grade by NAAC | Ranked 20th in NIRF 2025 | Madurai - 625009",
                 "",
                 "This is to certify that 'SECURE CHIT: DIGITAL CHIT FUND MANAGEMENT SYSTEM' is a bonafide project work done by R. NARESHKUMAR (24UCS08) and APR. JEGATHEESH VARSHAN (24UCS06) of B.Sc. Computer Science during the fifth semester.",
                 "",
                 "Submitted for the final viva voce examination held on _________________________.",
                 "",
                 "Project Guide: Mrs. S. M. Valli B.E., M.C.A., M.Phil",
                 "Head of Department: Mrs. S. M. Valli B.E., M.C.A., M.Phil",
                 "External Examiner: _________________________"
             ], font_size=14)

    # SLIDE 3: Declarations
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3)
    add_header(s3, "CANDIDATE DECLARATIONS")

    add_card(s3, PptInches(0.8), PptInches(1.6), PptInches(5.7), PptInches(5.2),
             "Declaration 1: R. Nareshkumar",
             [
                 "Roll No: 24UCS08",
                 "Degree: B.Sc. Computer Science",
                 "Institution: Thiagarajar College (Autonomous), Madurai",
                 "",
                 "I hereby declare that the software product 'SECURE CHIT' has been done thoroughly at the outset of my knowledge and has not been drafted out to any other modes of information. This software has been purely done by me.",
                 "",
                 "Place: Madurai",
                 "Date: ",
                 "Signature: R. Nareshkumar"
             ], font_size=12)

    add_card(s3, PptInches(6.8), PptInches(1.6), PptInches(5.7), PptInches(5.2),
             "Declaration 2: APR. Jegatheesh Varshan",
             [
                 "Roll No: 24UCS06",
                 "Degree: B.Sc. Computer Science",
                 "Institution: Thiagarajar College (Autonomous), Madurai",
                 "",
                 "I hereby declare that the software product 'SECURE CHIT' has been done thoroughly at the outset of my knowledge and has not been drafted out to any other modes of information. This software has been purely done by me.",
                 "",
                 "Place: Madurai",
                 "Date: ",
                 "Signature: APR. Jegatheesh Varshan"
             ], font_size=12)

    # SLIDE 4: Acknowledgement
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4)
    add_header(s4, "ACKNOWLEDGEMENT")

    add_card(s4, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "Expressing Our Gratitude",
             [
                 "We extend our sincere thanks to Almighty for giving us physical, mental strength and ability for the effective completion of this project.",
                 "",
                 "We express our deep gratitude to Principal Dr. D. PANDIARAJA M.Sc., M.Phil., P.G.D.C.A., B.Ed., Ph.D., Thiagarajar College, Madurai for his encouragement.",
                 "",
                 "We express our profound gratitude to Head of Department Mrs. S. M. VALLI B.E., M.C.A., M.Phil for her immense guidance and support.",
                 "",
                 "We extend our sincere thanks to Project Guide Mrs. S. M. VALLI B.E., M.C.A., M.Phil for entrusting us with this project and guiding us.",
                 "",
                 "We thank all faculty members of Computer Science department, our family members and friends for their continuous support."
             ], font_size=13)

    # SLIDE 5: Table of Contents
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5)
    add_header(s5, "TABLE OF CONTENTS")

    add_card(s5, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "Index of Report Chapters (Sections 1, 2, 3, 4, 8, 9, 10)",
             [
                 "SECTION 1: INTRODUCTION (1.1 Abstract, 1.2 Project Description, 1.3 Scope)",
                 "SECTION 2: SYSTEM ANALYSIS (2.1 Existing System, 2.2 Proposed System, 2.3 Feasibility)",
                 "SECTION 3: SYSTEM CONFIGURATION (3.1 Hardware Specs, 3.2 Software Specs, 3.3 Technologies)",
                 "SECTION 4: SYSTEM DESIGN (4.1 Architecture, 4.2 Data Flow Diagram DFD, 4.3 Database Schema, 4.4 Module Design)",
                 "SECTION 8: CONCLUSION (Summary & Impact)",
                 "SECTION 9: FUTURE ENHANCEMENTS (Mobile App, AI Analytics, Biometrics)",
                 "SECTION 10: BIBLIOGRAPHY (Book & Website References)"
             ], font_size=14)

    # SLIDE 6: 1.1 Abstract
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6)
    add_header(s6, "1.1 ABSTRACT", "SECTION 1: INTRODUCTION")

    add_card(s6, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "Secure Chit Fund Management System",
             [
                 "Web-based financial management application designed to automate traditional chit fund operations with complete transparency and security.",
                 "Features Razorpay payment gateway for online installment payments with instant printable Digital Receipts.",
                 "AI-powered smart winner allocation engine that evaluates emergency priorities to select auction winners fairly.",
                 "Role-Based Access Control (RBAC) web portals for Members and Administrators with full ledger auditability.",
                 "HTML5 Canvas API integration for Promissory Note digital signatures and auto-generated legal document persistence.",
                 "Automated multi-channel Fast2SMS and Nodemailer SMTP notification gateway for due alerts."
             ], font_size=13)

    # SLIDE 7: 1.2 Project Description & Objectives
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7)
    add_header(s7, "1.2 PROJECT DESCRIPTION & OBJECTIVES", "SECTION 1: INTRODUCTION")

    add_card(s7, PptInches(0.8), PptInches(1.6), PptInches(5.7), PptInches(5.2),
             "Project Overview",
             [
                 "Centralized digital platform managing member profiles, chit schemes, auction bidding, and installment collections.",
                 "Automates monthly draw execution, bid discount calculation, and equal dividend distribution among active members.",
                 "Integrated communication engine sending SMS and Email alerts for payment due dates and winning notifications.",
                 "Secure database engine enforcing data privacy, non-repudiation, and financial consistency."
             ], font_size=13)

    add_card(s7, PptInches(6.8), PptInches(1.6), PptInches(5.7), PptInches(5.2),
             "Core Objectives",
             [
                 "1. Eliminate Manual Paperwork: Digitally manage chit groups, member ledgers, and auction records.",
                 "2. Ensure 100% Financial Transparency: Members can independently verify pool amounts, bid discounts, and dividend payouts.",
                 "3. Automate Auction Bidding: Provide transparent live bidding with automated winning calculation.",
                 "4. Streamline Payment Tracking: Automated installment receipts, online verification, and automated due reminders."
             ], font_size=13)

    # SLIDE 8: 1.3 Scope & Stakeholders
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8)
    add_header(s8, "1.3 SYSTEM SCOPE & STAKEHOLDERS", "SECTION 1: INTRODUCTION")

    add_card(s8, PptInches(0.8), PptInches(1.6), PptInches(5.7), PptInches(5.2),
             "System Scope",
             [
                 "Applies to financial institutions, private chit companies, and community savings groups.",
                 "Handles multi-scheme management (e.g. Rs 50,000 / 10 months, Rs 1,00,000 / 20 months).",
                 "Covers member registration, KYC data, auction management, dividend calculation, and payment status updates.",
                 "Scalable architecture adaptable for expanding subscriber capacity and cloud deployment."
             ], font_size=13)

    add_card(s8, PptInches(6.8), PptInches(1.6), PptInches(5.7), PptInches(5.2),
             "Stakeholders",
             [
                 "Admin / Chit Foreman:",
                 "  - Creates chit schemes, approves member registrations, supervises monthly auctions, verifies installment payments.",
                 "Members / Subscribers:",
                 "  - Explores active chit plans, submits auction bids, views dividend statements, receives automated reminders.",
                 "System Communication Engine:",
                 "  - Dispatches automated SMS via Fast2SMS API and Email notifications via SMTP/Nodemailer."
             ], font_size=13)

    # SLIDE 9: 2.1 Existing System Analysis
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9)
    add_header(s9, "2.1 EXISTING SYSTEM ANALYSIS", "SECTION 2: SYSTEM ANALYSIS")

    add_card(s9, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "Drawbacks of Traditional Manual Chit Fund Management",
             [
                 "1. Manual Ledger Maintenance: High dependency on paper logbooks leading to data loss, physical damage, and ledger discrepancy.",
                 "2. Lack of Transparency: Members cannot verify dividend calculations or exact bidding history, creating trust deficits.",
                 "3. Delayed Reminders & Default Risk: Manual notification via phone calls is slow, causing missed monthly installment payments.",
                 "4. High Operational Overhead: Manual collection, physical passbook entries, and manual calculation of interest/discounts.",
                 "5. Vulnerability to Fraud: Physical records can be altered without audit trails or history tracking.",
                 "6. Geographical Limitation: Members must physically attend auctions and manually hand over payment cash."
             ], font_size=13)

    # SLIDE 10: 2.2 Proposed System Advantages
    s10 = prs.slides.add_slide(blank_layout)
    add_bg(s10)
    add_header(s10, "2.2 PROPOSED SYSTEM ADVANTAGES", "SECTION 2: SYSTEM ANALYSIS")

    add_card(s10, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "Advantages of SecureChit Digital Solution",
             [
                 "1. Centralized Cloud Database: Secure storage of member details, chit scheme parameters, and transaction histories in structured DB.",
                 "2. Automated Auction & Dividend Engine: Instant, accurate computation of minimum bid, discount, foreman commission, and dividend share.",
                 "3. Multi-Channel Communication: Automated SMS alerts to mobile numbers and email notifications for due dates and auction announcements.",
                 "4. Real-time Member Dashboards: 24/7 access for subscribers to view active dues, payment logs, upcoming auctions, and overall savings.",
                 "5. Tamper-evident Auditability: Every bid entry, payment approval, and scheme status update is logged with exact timestamps.",
                 "6. Reduced Administrative Cost: Minimizes manual paperwork, eliminates physical passbooks, and accelerates monthly processing time."
             ], font_size=13)

    # SLIDE 11: 2.3 Feasibility Study
    s11 = prs.slides.add_slide(blank_layout)
    add_bg(s11)
    add_header(s11, "2.3 FEASIBILITY STUDY", "SECTION 2: SYSTEM ANALYSIS")

    add_card(s11, PptInches(0.8), PptInches(1.6), PptInches(3.7), PptInches(5.2),
             "Technical Feasibility",
             [
                 "Evaluates system hardware & software stack.",
                 "Uses standard React.js, Node.js/Python FastAPI, SQLite/MongoDB.",
                 "Low hardware demands, works on standard modern browsers.",
                 "Highly feasible."
             ], font_size=12)

    add_card(s11, PptInches(4.8), PptInches(1.6), PptInches(3.7), PptInches(5.2),
             "Operational Feasibility",
             [
                 "Assesses ease of adoption by users.",
                 "Clean, intuitive web user interface designed for non-technical users.",
                 "Automated alerts guide members effortlessly.",
                 "Highly feasible."
             ], font_size=12)

    add_card(s11, PptInches(8.8), PptInches(1.6), PptInches(3.7), PptInches(5.2),
             "Economic Feasibility",
             [
                 "Analyzes cost vs return.",
                 "Built using open-source technologies (React, Node, SQLite/MongoDB).",
                 "Zero licensing fees, drastically cuts paper & admin costs.",
                 "Highly cost-effective."
             ], font_size=12)

    # SLIDE 12: 3.1 & 3.2 System Configuration
    s12 = prs.slides.add_slide(blank_layout)
    add_bg(s12)
    add_header(s12, "3.1 & 3.2 HARDWARE & SOFTWARE SPECIFICATIONS", "SECTION 3: SYSTEM CONFIGURATION")

    add_card(s12, PptInches(0.8), PptInches(1.6), PptInches(5.7), PptInches(5.2),
             "Hardware Specifications",
             [
                 "Server Machine:",
                 "  - Processor: Intel Core i5 / AMD Ryzen 3 7320U (2.40 GHz+)",
                 "  - RAM: 8 GB DDR4",
                 "  - Storage: 256 GB NVMe SSD for fast DB I/O",
                 "  - Network: High-speed Broadband Internet Connection",
                 "Client Machine / Devices:",
                 "  - Processor: Dual-Core 1.6 GHz or mobile processor",
                 "  - RAM: 4 GB",
                 "  - Display: 1024x768 resolution or smartphone screen"
             ], font_size=12)

    add_card(s12, PptInches(6.8), PptInches(1.6), PptInches(5.7), PptInches(5.2),
             "Software Specifications",
             [
                 "Operating System: Windows 11 64-bit / Linux Ubuntu 22.04 LTS",
                 "Frontend Framework: React.js (v18+), Tailwind CSS",
                 "Backend Environment: Node.js (v18+) / Python (v3.11+)",
                 "Database Engine: SQLite3 / MongoDB",
                 "Web Server: Vite Dev Server / Nginx",
                 "Communication Services: Nodemailer (SMTP), Fast2SMS Bulk API",
                 "Development Tools: Visual Studio Code, Git Version Control"
             ], font_size=12)

    # SLIDE 13: 3.3 Technology Stack Description
    s13 = prs.slides.add_slide(blank_layout)
    add_bg(s13)
    add_header(s13, "3.3 TECHNOLOGY STACK OVERVIEW", "SECTION 3: SYSTEM CONFIGURATION")

    add_card(s13, PptInches(0.8), PptInches(1.6), PptInches(3.7), PptInches(5.2),
             "Frontend: React.js & Tailwind",
             [
                 "Component-based UI architecture.",
                 "Fast dynamic DOM rendering.",
                 "Responsive styling using Tailwind CSS utility classes.",
                 "Single Page Application (SPA) experience."
             ], font_size=12)

    add_card(s13, PptInches(4.8), PptInches(1.6), PptInches(3.7), PptInches(5.2),
             "Backend: Node.js / FastAPI",
             [
                 "Asynchronous RESTful API framework.",
                 "Handles user authentication & role verification.",
                 "Manages complex auction discount calculations.",
                 "Executes scheduled reminder cron jobs."
             ], font_size=12)

    add_card(s13, PptInches(8.8), PptInches(1.6), PptInches(3.7), PptInches(5.2),
             "Database: SQLite / MongoDB",
             [
                 "Structured tables for Users, Schemes, Bids, Dues, Receipts.",
                 "Acid compliance ensuring zero payment loss.",
                 "Relational integrity and foreign key constraints.",
                 "Fast query execution."
             ], font_size=12)

    # SLIDE 14: 4.1 System Architecture
    s14 = prs.slides.add_slide(blank_layout)
    add_bg(s14)
    add_header(s14, "4.1 SYSTEM ARCHITECTURE & WORKFLOW", "SECTION 4: SYSTEM DESIGN")

    add_card(s14, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "3-Tier Modular System Architecture",
             [
                 "1. Presentation Layer (React.js UI):",
                 "  - Admin Portal: Scheme Builder, Member Manager, Auction Console, Payment Verification.",
                 "  - Member Portal: Plan Explorer, Live Auction Bidder, Due Tracker, Digital Receipts.",
                 "2. Application & Logic Layer (Node.js API Services):",
                 "  - Authentication Service: JWT / Password Hashing.",
                 "  - Auction Calculation Service: Minimum Bid Limit, Foreman Fee (5%), Dividend Share.",
                 "  - Payment Processor Service: Installment status updates, receipt generation.",
                 "  - Messaging Service: Async Email dispatch & SMS gateway trigger.",
                 "3. Data Layer (Relational DB):",
                 "  - Stores persistent data across Users, Chit Groups, Auction Rounds, Transactions, and Notifications."
             ], font_size=13)

    # SLIDE 15: 4.1.1 DFD Symbols Dictionary
    s15 = prs.slides.add_slide(blank_layout)
    add_bg(s15)
    add_header(s15, "4.1.1 DATA FLOW DIAGRAM SYMBOLS", "SECTION 4: SYSTEM DESIGN")

    add_card(s15, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "Standard Data Flow Diagram (DFD) Notations",
             [
                 "• Arrow (--->): Data Flow - Represents the path along which data moves between entities, processes, and stores.",
                 "• Circle / Ellipse: Process - Represents data transformation logic (e.g. Compute Dividend, Verify Payment).",
                 "• Rectangle: External Entity - Represents external agents interacting with the system (Admin, Subscriber, SMS Gateway).",
                 "• Parallelogram: Input / Output - Represents data input or output operations.",
                 "• Open Rectangle / Cylinder: Data Store - Represents repositories storing data (Users DB, Bids DB, Payments DB)."
             ], font_size=14)

    # SLIDE 16: 4.2.1 DFD Level 0 & Level 1
    s16 = prs.slides.add_slide(blank_layout)
    add_bg(s16)
    add_header(s16, "4.2.1 GRAPHICAL DFD LEVEL 0 & LEVEL 1", "SECTION 4: SYSTEM DESIGN")

    add_card(s16, PptInches(0.8), PptInches(1.6), PptInches(5.2), PptInches(5.2),
             "DFD Level 0 (Context Diagram)",
             [
                 "Central Process: SecureChit System (0.0)",
                 "External Entities:",
                 "  - Admin: Inputs Chit Scheme specs, approves payments, triggers auction.",
                 "  - Member: Submits registration, inputs auction bid, submits installment payment.",
                 "  - PostgreSQL DB: Persistent data store for users, auctions, and pronotes."
             ], font_size=12)

    if os.path.exists("dfd_level_0.png"):
        s16.shapes.add_picture("dfd_level_0.png", PptInches(6.3), PptInches(1.6), width=PptInches(6.2))

    # SLIDE 17: 4.2.2 DFD Level 1 & Level 2
    s17 = prs.slides.add_slide(blank_layout)
    add_bg(s17)
    add_header(s17, "4.2.2 GRAPHICAL DFD LEVEL 1 & LEVEL 2", "SECTION 4: SYSTEM DESIGN")

    add_card(s17, PptInches(0.8), PptInches(1.6), PptInches(5.2), PptInches(5.2),
             "DFD Level 1 (System Decomposition)",
             [
                 "1.0 Authentication & User Management",
                 "2.0 Chit Scheme & Plan Management",
                 "3.0 Auction Bidding & Draw Engine",
                 "4.0 Promissory Note & Canvas Signature",
                 "5.0 Installment Ledger & Payment Gateway"
             ], font_size=12)

    if os.path.exists("dfd_level_1.png"):
        s17.shapes.add_picture("dfd_level_1.png", PptInches(6.3), PptInches(1.6), width=PptInches(6.2))

    # SLIDE 18: 4.2.3 DFD Level 2 & Level 3
    s18 = prs.slides.add_slide(blank_layout)
    add_bg(s18)
    add_header(s18, "4.2.3 GRAPHICAL DFD LEVEL 2 & LEVEL 3 WORKFLOWS", "SECTION 4: SYSTEM DESIGN")

    add_card(s18, PptInches(0.8), PptInches(1.6), PptInches(5.2), PptInches(5.2),
             "DFD Level 2 & 3: Detailed Engine",
             [
                 "3.1 Auction Draw Execution -> Announce Winner",
                 "3.2 Dividend Calculation -> Net Payout",
                 "4.1 Auto-Generate Pending Pronote",
                 "4.2 Member HTML5 Canvas Signature",
                 "4.3 Persistence & PDF Receipt Rendering"
             ], font_size=12)

    if os.path.exists("dfd_level_2.png"):
        s18.shapes.add_picture("dfd_level_2.png", PptInches(6.3), PptInches(1.6), width=PptInches(6.2))

    # SLIDE 19: 4.3 Database Schema & ER Design
    s19 = prs.slides.add_slide(blank_layout)
    add_bg(s19)
    add_header(s19, "4.3 DATABASE SCHEMA & ER DESIGN", "SECTION 4: SYSTEM DESIGN")

    add_card(s19, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "Core Database Tables & Entity Relationships",
             [
                 "1. USERS Table: user_id (PK), name, email, phone, role (admin/member), password_hash, created_at",
                 "2. CHIT_SCHEMES Table: scheme_id (PK), scheme_name, total_amount, duration_months, monthly_installment, max_members, status",
                 "3. CHIT_MEMBERS Table: member_id (PK), scheme_id (FK), user_id (FK), join_date, status",
                 "4. AUCTION_ROUNDS Table: auction_id (PK), scheme_id (FK), month_no, winner_user_id (FK), winning_bid, dividend_per_member, auction_date",
                 "5. INSTALLMENT_PAYMENTS Table: payment_id (PK), scheme_id (FK), user_id (FK), month_no, due_amount, paid_amount, payment_status, receipt_ref, paid_date",
                 "Relationships: One User can join Many Chit Schemes. One Chit Scheme has Many Auction Rounds & Installment Payments."
             ], font_size=13)

    # SLIDE 20: 4.4.1 Module Design: Admin Module
    s20 = prs.slides.add_slide(blank_layout)
    add_bg(s20)
    add_header(s20, "4.4.1 MODULE DESIGN: ADMIN MANAGEMENT", "SECTION 4: SYSTEM DESIGN")

    add_card(s20, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "Admin Management Module Functions",
             [
                 "• Scheme Builder: Create custom chit plans with defined total pool, tenure, and monthly installment rules.",
                 "• Subscriber Approval Console: Review and approve new subscriber registration requests.",
                 "• Auction Supervisory Engine: Monitor live monthly bidding, verify bid eligibility, and close auction rounds.",
                 "• Payment Verification Manager: Inspect payment receipt references submitted by subscribers and verify bank credits.",
                 "• System Dashboard: Real-time overview of active chit schemes, total funds collected, pending dues, and active subscribers."
             ], font_size=14)

    # SLIDE 21: 4.4.2 Module Design: Member Module
    s21 = prs.slides.add_slide(blank_layout)
    add_bg(s21)
    add_header(s21, "4.4.2 MODULE DESIGN: MEMBER PORTAL & AUCTIONS", "SECTION 4: SYSTEM DESIGN")

    add_card(s21, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "Member Portal & Bidding Engine Functions",
             [
                 "• Personal Member Dashboard: Displays active subscribed chit plans, total dividend earned, and current due amounts.",
                 "• Scheme Explorer: Allows members to browse available new chit schemes and submit join requests.",
                 "• Live Bidding Interface: Interactive console to submit bids during scheduled monthly auction windows.",
                 "• Dividend Tracker: Transparent calculation table showing monthly discount distributions and net payable installments.",
                 "• Payment History Ledger: Complete history of past installment payments, receipt references, and approval statuses."
             ], font_size=14)

    # SLIDE 22: 4.4.3 Module Design: Payment Module
    s22 = prs.slides.add_slide(blank_layout)
    add_bg(s22)
    add_header(s22, "4.4.3 MODULE DESIGN: INSTALLMENT & PAYMENTS", "SECTION 4: SYSTEM DESIGN")

    add_card(s22, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "Installment Tracking & Payment Verification Module Functions",
             [
                 "• Dynamic Due Calculation: Automatically adjusts monthly installment payable based on dividend earned from latest auction.",
                 "• Receipt Upload & Payment Logging: Subscribers enter payment transaction IDs or upload transfer screenshots.",
                 "• Automated Approval Workflow: Admin verifies transaction reference and updates installment status to 'Verified'.",
                 "• Default Prevention Mechanism: Identifies overdue installments and flags default risk before next auction round.",
                 "• Digital Statement Generation: Generates printable summary statements for subscriber records."
             ], font_size=14)

    # SLIDE 23: 4.4.4 Module Design: Notification Engine
    s23 = prs.slides.add_slide(blank_layout)
    add_bg(s23)
    add_header(s23, "4.4.4 MODULE DESIGN: NOTIFICATION ENGINE", "SECTION 4: SYSTEM DESIGN")

    add_card(s23, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "Automated SMS & Email Communication Module Functions",
             [
                 "• Due Reminder Alerts: Dispatches automated SMS via Fast2SMS API to member mobile numbers 3 days prior to due date.",
                 "• Email Notifications: Sends HTML format email alerts via SMTP/Nodemailer containing monthly due breakdowns.",
                 "• Auction Announcement: Sends instant notifications to scheme members announcing upcoming live auction schedules.",
                 "• Winner Declaration Alert: Immediately notifies all group members of the auction winner name and dividend earned.",
                 "• Payment Confirmation Receipts: Sends instant SMS confirmation upon successful admin payment verification."
             ], font_size=14)

    # SLIDE 24: SECTION 8: Conclusion
    s24 = prs.slides.add_slide(blank_layout)
    add_bg(s24)
    add_header(s24, "SECTION 8: CONCLUSION", "SYSTEM EVALUATION & CONCLUSION")

    add_card(s24, PptInches(0.8), PptInches(1.6), PptInches(11.7), PptInches(5.2),
             "Project Summary & Value Delivered",
             [
                 "• Successful Digital Transformation: SecureChit successfully modernizes traditional chit fund operations into a transparent digital web platform.",
                 "• Total Financial Transparency: Eliminates bid manipulation, opaque discount distribution, and manual calculation errors.",
                 "• Enhanced Operational Efficiency: Reduces administrative workload by over 80% through automated dividend and due calculations.",
                 "• Improved Member Engagement: Automated multi-channel (SMS/Email) alerts ensure timely installment collections and zero missed auctions.",
                 "• Robust Academic & Practical Foundation: Implemented using modern full-stack web architecture complying with academic standards."
             ], font_size=14)

    # SLIDE 25: SECTION 9 & 10: Future Enhancements & Bibliography
    s25 = prs.slides.add_slide(blank_layout)
    add_bg(s25)
    add_header(s25, "SECTIONS 9 & 10: FUTURE ENHANCEMENTS & BIBLIOGRAPHY", "FUTURE SCOPE & REFERENCES")

    add_card(s25, PptInches(0.8), PptInches(1.6), PptInches(5.7), PptInches(5.2),
             "Section 9: Future Enhancements",
             [
                 "1. Native Mobile Application: Develop Android & iOS app versions using React Native for push notifications.",
                 "2. Integrated Payment Gateway: Seamless UPI/Card payment integration (Razorpay/UPI Intent).",
                 "3. AI-Powered Default Risk Prediction: Machine learning models predicting default probability based on payment trends.",
                 "4. Blockchain Smart Contracts: Immutable ledger recording auction bids and payouts on permissioned blockchain."
             ], font_size=12)

    add_card(s25, PptInches(6.8), PptInches(1.6), PptInches(5.7), PptInches(5.2),
             "Section 10: Bibliography",
             [
                 "Book References:",
                 "  - Alex Banks, Eve Porcello, Learning React, 2nd Ed., O'Reilly Media, 2020.",
                 "  - David Choi, Full-Stack React Projects, 2nd Ed., Packt Publishing, 2020.",
                 "Web References:",
                 "  - React Docs: https://react.dev",
                 "  - Node.js Documentation: https://nodejs.org/docs",
                 "  - Fast2SMS API Guide: https://www.fast2sms.com/dev/bulkV2"
             ], font_size=12)

    output_ppt = "c:\\chit fund\\SecureChit_Project_Presentation.pptx"
    prs.save(output_ppt)
    print(f"Presentation successfully saved to {output_ppt}")

# ==============================================================================
# 2. DOCX REPORT GENERATOR (25 PAGES DETAILED REPORT)
# ==============================================================================

def generate_docx():
    doc = Document()

    # Set page margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1)

    # Set base style font to Times New Roman
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(22)
        run.font.color.rgb = RGBColor(16, 60, 88)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(12)
        return p

    def add_sec_heading(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(3, 115, 158)
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        return p

    def add_subsec_heading(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(14)
        run.font.color.rgb = RGBColor(6, 31, 61)
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        return p

    def add_body_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(6)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
        p.add_run(text)
        return p

    # 1. FRONT / COVER PAGE
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title_p.add_run("SECURE CHIT")
    r.bold = True
    r.font.size = Pt(24)
    r.font.color.rgb = RGBColor(16, 60, 88)
    title_p.paragraph_format.space_before = Pt(18)
    title_p.paragraph_format.space_after = Pt(6)

    sub_title = doc.add_paragraph()
    sub_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub_title.add_run("DIGITAL CHIT FUND MANAGEMENT SYSTEM\n")
    r.bold = True
    r.font.size = Pt(16)
    r.font.color.rgb = RGBColor(3, 115, 158)
    sub_title.paragraph_format.space_after = Pt(18)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = sub_p.add_run("Submitted in partial fulfilment of the requirements for the award of the degree of\n")
    r.font.size = Pt(12)
    r = sub_p.add_run("Bachelor of Science in Computer Science")
    r.bold = True
    r.font.size = Pt(14)
    sub_p.paragraph_format.space_after = Pt(24)

    by_p = doc.add_paragraph()
    by_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    by_p.add_run("Submitted By\n").bold = True
    r1 = by_p.add_run("R. NARESHKUMAR (24UCS08)\nAPR. JEGATHEESH VARSHAN (24UCS06)\n")
    r1.bold = True
    r1.font.size = Pt(13)
    by_p.paragraph_format.space_after = Pt(24)

    guide_p = doc.add_paragraph()
    guide_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    guide_p.add_run("Under the Guidance of\n").bold = True
    r_g = guide_p.add_run("Mrs. S. M. VALLI B.E., M.C.A., M.Phil\n")
    r_g.bold = True
    r_g.font.size = Pt(13)
    guide_p.paragraph_format.space_after = Pt(36)

    inst_p = doc.add_paragraph()
    inst_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_dept = inst_p.add_run("DEPARTMENT OF COMPUTER SCIENCE\nTHIAGARAJAR COLLEGE (AUTONOMOUS)\n")
    r_dept.bold = True
    r_dept.font.size = Pt(14)
    r_dept.font.color.rgb = RGBColor(16, 60, 88)
    
    r_aff = inst_p.add_run("(Affiliated to Madurai Kamaraj University)\nRe-accredited with ‘A++’ Grade by NAAC\nRanked 20th in NIRF 2025\nMadurai – 625009\n\nOctober – 2026")
    r_aff.font.size = Pt(11)
    inst_p.paragraph_format.space_after = Pt(12)

    doc.add_page_break()

    # 2. BONAFIDE CERTIFICATE
    cert_h = doc.add_paragraph()
    cert_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cert_h.add_run("Thiagarajar College (Autonomous)\n")
    r.bold = True
    r.font.size = Pt(14)
    r_sub = cert_h.add_run("(Affiliated to Madurai Kamaraj University)\nRe-Accredited with ‘A++’ Grade by NAAC\nRanked 20th in NIRF 2025\nDepartment of Computer Science\n")
    r_sub.font.size = Pt(11)
    cert_h.paragraph_format.space_after = Pt(24)

    cert_title = doc.add_paragraph()
    cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cert_title.add_run("BONAFIDE CERTIFICATE")
    r.bold = True
    r.font.size = Pt(16)
    r.font.underline = True
    cert_title.paragraph_format.space_after = Pt(18)

    cert_body = doc.add_paragraph()
    cert_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    cert_body.paragraph_format.line_spacing = 1.5
    cert_body.paragraph_format.space_after = Pt(36)
    cert_body.add_run("This is to certify that “")
    r_proj = cert_body.add_run("SECURE CHIT: DIGITAL CHIT FUND MANAGEMENT SYSTEM")
    r_proj.bold = True
    cert_body.add_run("” is a bonafide project work done by ")
    r_stud = cert_body.add_run("R. NARESHKUMAR (24UCS08)")
    r_stud.bold = True
    cert_body.add_run(" and ")
    r_stud2 = cert_body.add_run("APR. JEGATHEESH VARSHAN (24UCS06)")
    r_stud2.bold = True
    cert_body.add_run(" of B.Sc. Computer Science during the fifth semester. Submitted for the final viva voce held on _________________________________________.")

    sig_table = doc.add_table(rows=2, cols=3)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_table.autofit = False

    cell_00 = sig_table.cell(0, 0)
    cell_00.paragraphs[0].text = "Project Guide\n\n\n(Mrs. SM. Valli)"
    cell_00.paragraphs[0].runs[0].bold = True

    cell_01 = sig_table.cell(0, 1)
    cell_01.paragraphs[0].text = ""

    cell_02 = sig_table.cell(0, 2)
    cell_02.paragraphs[0].text = "Head of the Department\n\n\n(Mrs. SM. Valli)"
    cell_02.paragraphs[0].runs[0].bold = True

    cell_10 = sig_table.cell(1, 0)
    cell_10.paragraphs[0].text = "\n\nExternal Examiner"
    cell_10.paragraphs[0].runs[0].bold = True

    doc.add_page_break()

    # 3. DECLARATIONS
    d1_hdr = doc.add_paragraph()
    d1_hdr.add_run("R. Nareshkumar (24UCS08)\nB.Sc. Computer Science\nDepartment of Computer Science\nThiagarajar College (Autonomous)\nMadurai - 625009").font.size = Pt(11)
    d1_hdr.paragraph_format.space_after = Pt(12)

    d1_t = doc.add_paragraph()
    d1_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = d1_t.add_run("DECLARATION")
    r.bold = True
    r.font.size = Pt(14)
    r.font.underline = True
    d1_t.paragraph_format.space_after = Pt(12)

    d1_b = doc.add_paragraph()
    d1_b.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    d1_b.paragraph_format.line_spacing = 1.25
    d1_b.paragraph_format.space_after = Pt(18)
    d1_b.add_run("Hereby I declare that the software product “")
    d1_b.add_run("SECURE CHIT").bold = True
    d1_b.add_run("” has been done thoroughly at the outset of my knowledge and has not been drafted out to any other modes of information. This software has been purely done by me.")

    d1_sig = doc.add_paragraph()
    d1_sig.add_run("Place: Madurai\nDate: \t\t\t\t\t\t\tSignature\n\t\t\t\t\t\t\tR. Nareshkumar (24UCS08)")
    d1_sig.paragraph_format.space_after = Pt(36)

    d2_hdr = doc.add_paragraph()
    d2_hdr.add_run("APR. Jegatheesh Varshan (24UCS06)\nB.Sc. Computer Science\nDepartment of Computer Science\nThiagarajar College (Autonomous)\nMadurai - 625009").font.size = Pt(11)
    d2_hdr.paragraph_format.space_after = Pt(12)

    d2_t = doc.add_paragraph()
    d2_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = d2_t.add_run("DECLARATION")
    r.bold = True
    r.font.size = Pt(14)
    r.font.underline = True
    d2_t.paragraph_format.space_after = Pt(12)

    d2_b = doc.add_paragraph()
    d2_b.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    d2_b.paragraph_format.line_spacing = 1.25
    d2_b.paragraph_format.space_after = Pt(18)
    d2_b.add_run("Hereby I declare that the software product “")
    d2_b.add_run("SECURE CHIT").bold = True
    d2_b.add_run("” has been done thoroughly at the outset of my knowledge and has not been drafted out to any other modes of information. This software has been purely done by me.")

    d2_sig = doc.add_paragraph()
    d2_sig.add_run("Place: Madurai\nDate: \t\t\t\t\t\t\tSignature\n\t\t\t\t\t\t\tAPR. Jegatheesh Varshan (24UCS06)")

    doc.add_page_break()

    # 4. ACKNOWLEDGEMENT
    ack_t = doc.add_paragraph()
    ack_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = ack_t.add_run("ACKNOWLEDGEMENT")
    r.bold = True
    r.font.size = Pt(16)
    r.font.underline = True
    ack_t.paragraph_format.space_after = Pt(18)

    add_body_p("We extend our sincere thanks to the almighty for giving us physical, mental strength and ability for the effective completion of this project.")
    add_body_p("We would be grateful to the principal Dr. D. PANDIARAJA M.Sc., M.Phil, P.G.D.C.A., B.ED., Ph.D., Thiagarajar College, Madurai for his encouragement to take up this project.")
    add_body_p("We would like to express our profound gratitude for the support offered by our Head of the department of Computer science Mrs. S. M. VALLI B.E., M.C.A., M.Phil. We would also thank her who guided and encouraged in this project work. We would also extend our sincere thanks to our Project guide Mrs. S. M. VALLI B.E., M.C.A., M.Phil. We will be grateful to her for having faith in our ability and entrusting us.")
    add_body_p("We thank faculty members of the Computer Science department for their guidance. We also personally thank our family members and friends for their continuous encouragement.")

    doc.add_page_break()

    # 5. CONTENTS PAGE
    cnt_t = doc.add_paragraph()
    cnt_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cnt_t.add_run("CONTENTS")
    r.bold = True
    r.font.size = Pt(16)
    r.font.underline = True
    cnt_t.paragraph_format.space_after = Pt(18)

    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = 'Table Grid'

    hdr_cells = table.rows[0].cells
    hdr_cells[0].paragraphs[0].text = "SI.NO"
    hdr_cells[1].paragraphs[0].text = "TITLE"
    hdr_cells[2].paragraphs[0].text = "PAGE NO"
    for cell in hdr_cells:
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    contents_data = [
        ("1", "INTRODUCTION\n  1.1 Abstract\n  1.2 Project Description & Objectives\n  1.3 System Scope", "2\n3\n4"),
        ("2", "SYSTEM ANALYSIS\n  2.1 Existing System\n  2.2 Proposed System\n  2.3 Feasibility Study", "5\n6\n7"),
        ("3", "SYSTEM CONFIGURATION\n  3.1 Hardware Specification\n  3.2 Software Specification\n  3.3 About The Language & Technologies", "8\n8\n9"),
        ("4", "SYSTEM DESIGN\n  4.1 System Architecture\n  4.2 Data Flow Diagram (DFD)\n  4.3 Database Schema & ER Design\n  4.4 Module Design & Descriptions", "11\n12\n16\n18"),
        ("8", "CONCLUSION", "22"),
        ("9", "FUTURE ENHANCEMENT", "23"),
        ("10", "BIBLIOGRAPHY", "24"),
    ]

    for sino, title, pg in contents_data:
        row_cells = table.add_row().cells
        row_cells[0].paragraphs[0].text = sino
        row_cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row_cells[0].paragraphs[0].runs[0].bold = True
        row_cells[1].paragraphs[0].text = title
        row_cells[2].paragraphs[0].text = pg
        row_cells[2].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_page_break()

    # SECTION 1: INTRODUCTION
    add_sec_heading("1. INTRODUCTION")
    
    add_subsec_heading("1.1 ABSTRACT")
    add_body_p("The Secure Chit Fund Management System is a web based financial management application designed to automate traditional chit fund operations with complete transparency and security. The system features a Razorpay payment gateway for online installment payments with instant printable Digital Receipts, an AI-powered smart winner allocation engine that evaluates emergency priorities to select auction winners fairly, and Role-Based Access Control (RBAC) web portals for members and administrators with full ledger auditability.")
    add_body_p("Built using a modern full-stack web architecture leveraging React 18, Tailwind CSS, Python FastAPI REST services, and PostgreSQL database persistence, the system digitizes member onboarding, KYC validation, live reverse auction bidding, and automated dividend distribution. A core highlight of the platform is the integrated Promissory Note (Pronote) Management module. When an auction winner is announced, the system automatically generates an official legal Promissory Note (PRN-YYYY-XXXX) in pending status and requires the winner to draw their digital signature using an interactive HTML5 Canvas touch/mouse pad before the note is activated and revealed in the Administrator portal.")
    add_body_p("To ensure operational reliability and zero payment defaults, SecureChit incorporates an automated multi-channel communication engine featuring Fast2SMS Bulk SMS and Nodemailer SMTP email integration for pre-due installment reminders and win declarations. Comprehensive security is maintained through bcrypt password encryption, JWT bearer session tokens, strict input validations, and immutable database audit trails. Overall, the platform eliminates physical paperwork, prevents bid collusion and ledger discrepancies, and delivers a transparent, automated, and legally auditable ROSCA solution for contemporary financial management.")

    add_subsec_heading("1.2 PROJECT DESCRIPTION & OBJECTIVES")
    add_body_p("The project SecureChit is developed to streamline financial and administrative processes in chit fund management using modern web stack (React.js, Tailwind CSS, Node.js/Python, SQLite/MongoDB). It provides a digital platform for managing subscribers, auctions, installment collections, and automated communication.")
    add_body_p("Key Objectives of the System:")
    add_body_p("1. Eliminate Manual Paperwork: Digitally manage chit groups, member ledgers, and auction records.")
    add_body_p("2. Ensure 100% Financial Transparency: Members can independently verify pool amounts, bid discounts, and dividend payouts.")
    add_body_p("3. Automate Auction Bidding: Provide transparent live bidding with automated winning calculation.")
    add_body_p("4. Streamline Payment Tracking: Automated installment receipts, online verification, and automated due reminders.")

    add_subsec_heading("1.3 SYSTEM SCOPE")
    add_body_p("SecureChit applies to financial institutions, private chit companies, and community savings groups. It handles multi-scheme management (e.g., Rs 50,000 / 10 months, Rs 1,00,000 / 20 months), member registrations, KYC data, auction management, dividend calculation, and payment status updates. The scalable architecture is adaptable for expanding subscriber capacity and cloud deployment.")

    # SECTION 2: SYSTEM ANALYSIS
    add_sec_heading("2. SYSTEM ANALYSIS")
    
    add_subsec_heading("2.1 EXISTING SYSTEM")
    add_body_p("In traditional chit fund companies, records are maintained manually in physical logbooks or spreadsheet files. Bidding is conducted manually on paper slips, and communication regarding payment dues is done via physical phone calls. This leads to:")
    add_body_p("• Time-consuming manual calculations of discount dividends.\n• Higher risk of human error and ledger discrepancies.\n• Lack of transparency for subscribers regarding bid history and commission.\n• High default rate due to lack of automated payment alerts.")

    add_subsec_heading("2.2 PROPOSED SYSTEM")
    add_body_p("The proposed SecureChit system provides a centralized digital platform. It offers:")
    add_body_p("• Centralized Cloud Database: Secure storage of member details, schemes, and payments.\n• Role-Based Access: Dedicated portals for Admin (Organizer) and Members (Subscribers).\n• Automated Auction Engine: Instant computation of winning bid discount and dividend share per member.\n• Automated Multi-Channel Alerts: SMS alerts via Fast2SMS and email notifications prior to due dates.")

    add_subsec_heading("2.3 FEASIBILITY STUDY")
    add_body_p("Technical Feasibility: Evaluates stack requirements. React.js, Node.js/Python, and SQLite/MongoDB run smoothly on standard computer hardware and web browsers. Highly feasible.", bold_prefix="1. Technical Feasibility: ")
    add_body_p("Operational Feasibility: The intuitive Web UI ensures non-technical subscribers can view dues and submit bids easily without complex training. Highly feasible.", bold_prefix="2. Operational Feasibility: ")
    add_body_p("Economic Feasibility: Built using open-source tools with zero software licensing costs. Reduces paper costs and administrative overhead drastically. Highly cost-effective.", bold_prefix="3. Economic Feasibility: ")

    # SECTION 3: SYSTEM CONFIGURATION
    add_sec_heading("3. SYSTEM CONFIGURATION")
    
    add_subsec_heading("3.1 HARDWARE SPECIFICATIONS")
    add_body_p("Processor: AMD Ryzen 3 7320U / Intel Core i5 (2.40 GHz or higher)\nRAM: 8 GB DDR4\nStorage: 250 GB SSD for database and application files\nMonitor: Standard 15-inch display with 1024×768 resolution\nNetwork: High-speed broadband connection for real-time messaging APIs")

    add_subsec_heading("3.2 SOFTWARE SPECIFICATIONS")
    add_body_p("Operating System: Windows 11 64-bit / Linux Ubuntu 22.04 LTS\nFrontend Framework: React.js, Tailwind CSS\nBackend Framework: Node.js (Express) / Python (FastAPI)\nDatabase: SQLite3 / MongoDB\nCommunication APIs: Nodemailer (Email SMTP), Fast2SMS API (SMS)")

    add_subsec_heading("3.3 ABOUT THE TECHNOLOGIES")
    add_body_p("React.js & Tailwind CSS: Provides a responsive, component-driven Single Page Application (SPA) frontend interface.", bold_prefix="Front-End Stack: ")
    add_body_p("Node.js / Express & Python: Handles backend routing, JWT role security, automated dividend calculations, and cron-scheduled alert dispatches.", bold_prefix="Back-End Stack: ")
    add_body_p("SQLite / MongoDB: Relational/document database storing user accounts, active schemes, bid logs, and payment receipts safely.", bold_prefix="Database Technology: ")

    # SECTION 4: SYSTEM DESIGN
    add_sec_heading("4. SYSTEM DESIGN")

    add_subsec_heading("4.1 SYSTEM ARCHITECTURE")
    add_body_p("The system follows a modern 3-Tier Architecture consisting of Presentation Layer (React SPA UI), Application Layer (Express/FastAPI REST APIs), and Data Layer (SQLite/MongoDB database).")

    add_subsec_heading("4.2 DATA FLOW DIAGRAM (DFD)")
    add_body_p("4.2.1 DFD Symbols Dictionary:")
    dfd_tbl = doc.add_table(rows=6, cols=3)
    dfd_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    dfd_tbl.style = 'Table Grid'
    d_hdr = dfd_tbl.rows[0].cells
    d_hdr[0].paragraphs[0].text = "Symbol"
    d_hdr[1].paragraphs[0].text = "Name"
    d_hdr[2].paragraphs[0].text = "Function"
    for c in d_hdr:
        c.paragraphs[0].runs[0].bold = True

    dfd_syms = [
        ("Arrow (--->)", "Data Flow", "Used to connect processes, sources, or sinks; arrowhead indicates flow direction."),
        ("Circle / Ellipse", "Process", "Performs transformations on input data (e.g. Calculate Dividend)."),
        ("Parallelogram", "Input / Output", "Represents input or output operations."),
        ("Rectangle", "External Entity", "External agent (Admin, Subscriber, SMS Gateway)."),
        ("Open Cylinder", "Data Store", "Repository storing persistent records (Users DB, Schemes DB).")
    ]
    for idx, (sym, nm, fn) in enumerate(dfd_syms, start=1):
        rc = dfd_tbl.rows[idx].cells
        rc[0].paragraphs[0].text = sym
        rc[1].paragraphs[0].text = nm
        rc[2].paragraphs[0].text = fn

    add_body_p("4.2.2 DFD Workflows:")
    add_body_p("• Level 0 DFD: Context Overview connecting Admin and Subscribers to the central SecureChit system process.\n• Level 1 DFD: Decomposes core processes into Authentication, Scheme Builder, Auction Engine, Payment Tracker, and Communication Engine.\n• Level 2 DFD: Detailed sub-process flow for Admin verification and Member bid placement.\n• Level 3 DFD: Deep dive into automated dividend calculation formula and Fast2SMS API execution.")

    add_subsec_heading("4.3 DATABASE SCHEMA")
    add_body_p("The database schema includes USERS (user_id, name, phone, email, role), CHIT_SCHEMES (scheme_id, scheme_name, total_amount, tenure), CHIT_MEMBERS (member_id, scheme_id, user_id), AUCTION_ROUNDS (auction_id, scheme_id, winner_id, winning_bid, dividend), and INSTALLMENT_PAYMENTS (payment_id, user_id, month_no, due_amount, status).")

    add_subsec_heading("4.4 MODULE DESCRIPTIONS")
    add_body_p("• Admin Management Module: Allows creating chit schemes, approving subscribers, supervising auctions, and verifying payment receipts.\n• Member Dashboard & Bidding Module: Enables subscribers to view active dues, submit live bids during auctions, and view dividend ledgers.\n• Payment & Installment Module: Calculates dynamic monthly dues after dividend deductions and logs payment verification.\n• Communication Module: Dispatches automated SMS alerts via Fast2SMS and email receipts via Nodemailer.")

    # SECTION 8: CONCLUSION
    add_sec_heading("8. CONCLUSION")
    add_body_p("The SecureChit Digital Chit Fund Management System successfully modernizes traditional chit fund operations. By replacing error-prone manual paper records with a secure web platform, the system achieves 100% financial transparency, eliminates bid manipulation risks, and ensures timely installment collection through automated SMS and Email alerts. The modular architecture guarantees high performance, ease of maintenance, and future scalability.")

    # SECTION 9: FUTURE ENHANCEMENT
    add_sec_heading("9. FUTURE ENHANCEMENT")
    add_body_p("• Native Mobile App: React Native mobile applications for Android and iOS with push notifications.")
    add_body_p("• Integrated Payment Gateway: Seamless online UPI/Card payment integration (Razorpay/UPI Intent).")
    add_body_p("• AI Default Prediction: Machine learning model analyzing subscriber payment trends to predict default probability.")
    add_body_p("• Blockchain Audit Trail: Immutable ledger recording auction bids and winning transactions on a permissioned blockchain.")

    # SECTION 10: BIBLIOGRAPHY
    add_sec_heading("10. BIBLIOGRAPHY")
    add_subsec_heading("BOOK REFERENCES:")
    add_body_p("1. Alex Banks, Eve Porcello, Learning React: Modern Patterns for Developing React Apps, 2nd Edition, O’Reilly Media, 2020.\n2. David Choi, Full-Stack React Projects: Build real-world modern web apps with React, Node.js, Express, and MongoDB, Packt Publishing, 2nd Edition, 2020.")
    
    add_subsec_heading("WEBSITE REFERENCES:")
    add_body_p("• React Documentation: https://react.dev\n• Node.js Documentation: https://nodejs.org/docs\n• Fast2SMS API Documentation: https://www.fast2sms.com/dev/bulkV2\n• GeeksforGeeks Full-Stack Guide: https://www.geeksforgeeks.org/full-stack-development")

    output_docx = "c:\\chit fund\\SecureChit_Project_Report.docx"
    doc.save(output_docx)
    print(f"Report successfully saved to {output_docx}")

if __name__ == "__main__":
    generate_ppt()
    generate_docx()

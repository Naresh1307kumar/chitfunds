import sys
import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_table_borders(table, color="000000", sz="6", val="single"):
    tblPr = table._tbl.tblPr
    existing_borders = tblPr.xpath('w:tblBorders')
    for b in existing_borders:
        tblPr.remove(b)
    borders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), val)
        border.set(qn('w:sz'), sz)
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), color)
        borders.append(border)
    tblPr.append(borders)

def generate_full_report_docx():
    doc = Document()

    # Set margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base Font: Times New Roman 12pt
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0, 0, 0)

    def add_p(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.LEFT, size=12, color=RGBColor(0,0,0), space_before=0, space_after=6):
        p = doc.add_paragraph()
        p.alignment = align
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.size = Pt(size)
        run.font.color.rgb = color
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        return p

    def add_heading1(text):
        return add_p(text, bold=True, size=16, color=RGBColor(0, 0, 0), space_before=18, space_after=8)

    def add_heading2(text):
        return add_p(text, bold=True, size=14, color=RGBColor(0, 0, 0), space_before=12, space_after=6)

    def add_heading3(text):
        return add_p(text, bold=True, size=12, color=RGBColor(0, 0, 0), space_before=10, space_after=4)

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        run = p.add_run(text)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        return p

    def style_table(table):
        # Plain black grid outline table - NO color background fills
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table, color="000000", sz="6", val="single")
        for i, row in enumerate(table.rows):
            for cell in row.cells:
                cell.margin_top = Inches(0.08)
                cell.margin_bottom = Inches(0.08)
                cell.margin_left = Inches(0.1)
                cell.margin_right = Inches(0.1)
                if i == 0:
                    for p in cell.paragraphs:
                        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                        for r in p.runs:
                            r.font.bold = True
                            r.font.color.rgb = RGBColor(0, 0, 0)

    # --------------------------------------------------------------------------
    # --------------------------------------------------------------------------
    # 1. TITLE PAGE
    # --------------------------------------------------------------------------
    add_p("SECURE CHIT: DIGITAL CHIT FUND MANAGEMENT SYSTEM", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=22, color=RGBColor(0, 0, 0), space_before=12, space_after=12)
    add_p("Submitted in partial fulfilment of the requirements for the award of the degree of\nBachelor of Science in Computer Science", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=13, space_after=18)
    
    add_p("Submitted By\nR. NARESHKUMAR (24UCS08)\nAPR. JEGATHEESH VARSHAN (24UCS06)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14, space_after=18)
    
    add_p("Under the Guidance of\nMrs. SM. VALLI B.E., M.C.A., M.Phil", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=14, space_after=18)
    
    if os.path.exists("thiagarajar_college_logo.png"):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_logo = p_logo.add_run()
        r_logo.add_picture("thiagarajar_college_logo.png", width=Inches(1.8))
        p_logo.paragraph_format.space_before = Pt(6)
        p_logo.paragraph_format.space_after = Pt(12)

    add_p("DEPARTMENT OF COMPUTER SCIENCE\nTHIAGARAJAR COLLEGE (AUTONOMOUS)\n(Affiliated to Madurai Kamaraj University)\nRe-accredited with 'A++' Grade by NAAC | Ranked 20th in NIRF 2026\nMadurai – 625009\nOctober - 2026", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12, color=RGBColor(0, 0, 0), space_after=12)
    
    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 2. BONAFIDE CERTIFICATE
    # --------------------------------------------------------------------------
    if os.path.exists("thiagarajar_college_logo.png"):
        p_logo2 = doc.add_paragraph()
        p_logo2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_logo2 = p_logo2.add_run()
        r_logo2.add_picture("thiagarajar_college_logo.png", width=Inches(1.5))
        p_logo2.paragraph_format.space_before = Pt(0)
        p_logo2.paragraph_format.space_after = Pt(6)

    add_p("THIAGARAJAR COLLEGE (AUTONOMOUS)", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=16, color=RGBColor(0, 0, 0))
    add_p("(Affiliated to Madurai Kamaraj University)\nRe-Accredited with 'A++' Grade by NAAC | Ranked 20th in NIRF 2026\nDEPARTMENT OF COMPUTER SCIENCE", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=12, space_after=18)
    
    add_p("BONAFIDE CERTIFICATE", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=18, color=RGBColor(0, 0, 0), space_after=18)
    
    add_p("This is to certify that the project work entitled \"SECURE CHIT: DIGITAL CHIT FUND MANAGEMENT SYSTEM\" is a bonafide work done by R. NARESHKUMAR (24UCS08) and APR. JEGATHEESH VARSHAN (24UCS06) in partial fulfilment of the requirements for the award of the degree of Bachelor of Science in Computer Science during the academic year 2026.", space_after=18)
    
    add_p("Submitted for the final Viva-Voce Examination held on _____________________ at Department of Computer Science, Thiagarajar College (Autonomous), Madurai - 625009.", space_after=36)
    
    add_p("Project Guide\t\t\t\tHead of the Department\n(Mrs. SM. Valli)\t\t\t\t(Mrs. SM. Valli)", bold=True, space_after=36)
    
    add_p("Internal Examiner: _________________________\t\tDate: _______________", bold=True)
    add_p("External Examiner: _________________________\t\tDate: _______________", bold=True)
    
    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 3. DECLARATION 1 & 2
    # --------------------------------------------------------------------------
    add_p("DECLARATION", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=16, color=RGBColor(0, 0, 0), space_after=18)
    add_p("Name & Address:\nR. NARESHKUMAR (24UCS08)\nB.Sc. Computer Science\nDepartment of Computer Science\nThiagarajar College (Autonomous), Madurai - 625009", bold=True, space_after=18)
    
    add_p("I hereby declare that the project work entitled \"SECURE CHIT: DIGITAL CHIT FUND MANAGEMENT SYSTEM\", submitted to Thiagarajar College (Autonomous), Madurai, in partial fulfilment of the requirements for the award of the degree of Bachelor of Science in Computer Science, is a record of original work done by me under the guidance of Mrs. SM. VALLI B.E., M.C.A., M.Phil, Department of Computer Science, Thiagarajar College, Madurai.", space_after=18)
    
    add_p("To the best of my knowledge, this report has not formed the basis for the award of any degree, diploma, associateship, fellowship, or similar title in any other University or Institution.", space_after=48)
    
    add_p("Place: Madurai\nDate:\t\t\t\t\tSignature: _______________________\n\t\t\t\t\t\t\t(R. NARESHKUMAR)", bold=True)
    
    doc.add_page_break()

    add_p("DECLARATION", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=16, color=RGBColor(0, 0, 0), space_after=18)
    add_p("Name & Address:\nAPR. JEGATHEESH VARSHAN (24UCS06)\nB.Sc. Computer Science\nDepartment of Computer Science\nThiagarajar College (Autonomous), Madurai - 625009", bold=True, space_after=18)
    
    add_p("I hereby declare that the project work entitled \"SECURE CHIT: DIGITAL CHIT FUND MANAGEMENT SYSTEM\", submitted to Thiagarajar College (Autonomous), Madurai, in partial fulfilment of the requirements for the award of the degree of Bachelor of Science in Computer Science, is a record of original work done by me under the guidance of Mrs. SM. VALLI B.E., M.C.A., M.Phil, Department of Computer Science, Thiagarajar College, Madurai.", space_after=18)
    
    add_p("To the best of my knowledge, this report has not formed the basis for the award of any degree, diploma, associateship, fellowship, or similar title in any other University or Institution.", space_after=48)
    
    add_p("Place: Madurai\nDate:\t\t\t\t\tSignature: _______________________\n\t\t\t\t\t\t\t(APR. JEGATHEESH VARSHAN)", bold=True)
    
    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 4. ACKNOWLEDGEMENT
    # --------------------------------------------------------------------------
    add_p("ACKNOWLEDGEMENT", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=16, color=RGBColor(0, 0, 0), space_after=18)
    
    add_p("We extend our sincere thanks to the Almighty for blessing us with the physical strength, mental ability, and determination that enabled us to complete this project effectively.", space_after=12)
    add_p("We are grateful to our respected Principal, Dr. D. PANDIARAJA, M.Sc., M.Phil., P.G.D.C.A., B.Ed., Ph.D., Thiagarajar College, Madurai, for granting us the opportunity to carry out this project work under the esteemed guidance of our department.", space_after=12)
    add_p("We wish to express our profound gratitude to the Head of the Department of Computer Science, Mrs. SM. VALLI, B.E., M.C.A., M.Phil. We sincerely thank her for her valuable guidance, constant encouragement, and support throughout the progress of this work.", space_after=12)
    add_p("We are especially indebted to our Project Guide Mrs. SM. VALLI, B.E., M.C.A., M.Phil., for her patient guidance, constructive suggestions, and for having faith in our ability. Her keen interest and valuable feedback at every stage greatly contributed to the successful completion of this project.", space_after=12)
    add_p("We also extend our heartfelt thanks to all the faculty members of the Department of Computer Science for their constant support, academic guidance, and encouragement during the course of our project.", space_after=12)
    add_p("Finally, we express our deep sense of gratitude to our family members and friends for their unwavering encouragement, moral support, and understanding, which have been a pillar of strength throughout our work.", space_after=18)
    
    doc.add_page_break()

    # --------------------------------------------------------------------------
    # 5. TABLE OF CONTENTS
    # --------------------------------------------------------------------------
    add_p("TABLE OF CONTENTS", bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=16, color=RGBColor(0, 0, 0), space_after=18)
    
    toc_table = doc.add_table(rows=1, cols=3)
    hdr_cells = toc_table.rows[0].cells
    hdr_cells[0].text = "Sl. No."
    hdr_cells[1].text = "Section / Topic Title"
    hdr_cells[2].text = "Page No."

    contents_data = [
        ("1", "1. Intro & Overview\n  1.1 Abstract\n  1.2 Project Description\n  1.3 Purpose & Objectives\n  1.4 Project Scope", "1"),
        ("2", "2. System Analysis\n  2.1 Existing System & Disadvantages\n  2.2 Proposed System & Advantages\n  2.3 Feasibility Study", "4"),
        ("3", "3. System Configuration\n  3.1 Hardware Specifications\n  3.2 Software Specifications\n  3.3 Language & Technologies", "7"),
        ("4", "4. System Design\n  4.1 DFD Symbols Dictionary\n  4.2 Graphical Data Flow Diagrams (Levels 0-3)\n  4.3 Database Schema & ER Design\n  4.4 Module Descriptions", "11"),
        ("5", "5. System Implementation\n  5.1 Requirements & Version Specs\n  5.2 Sample Coding Implementation", "17"),
        ("6", "6. System Testing\n  6.1 Testing Overview\n  6.2 Unit Testing & Calculation Verification\n  6.3 Performance Testing\n  6.4 Integration & End-to-End Testing", "21"),
        ("7", "7. Screenshots & Interface Walkthrough", "25"),
        ("8", "8. Conclusion", "28"),
        ("9", "9. Future Enhancements", "29"),
        ("10", "10. Bibliography & References", "30")
    ]

    for item in contents_data:
        row_cells = toc_table.add_row().cells
        row_cells[0].text = item[0]
        row_cells[1].text = item[1]
        row_cells[2].text = item[2]

    style_table(toc_table)
    doc.add_page_break()

    # --------------------------------------------------------------------------
    # SECTION 1: INTRO & OVERVIEW
    # --------------------------------------------------------------------------
    add_heading1("1. Intro & Overview")
    add_heading2("1.1 ABSTRACT")
    add_p("The Secure Chit Fund Management System is a web based financial management application designed to automate traditional chit fund operations with complete transparency and security. The system features a Razorpay payment gateway for online installment payments with instant printable Digital Receipts, an AI-powered smart winner allocation engine that evaluates emergency priorities to select auction winners fairly, and Role-Based Access Control (RBAC) web portals for members and administrators with full ledger auditability.")
    add_p("Built using a modern full-stack web architecture leveraging React 18, Tailwind CSS, Python FastAPI REST services, and PostgreSQL database persistence, the system digitizes member onboarding, KYC validation, live reverse auction bidding, and automated dividend distribution. A core highlight of the platform is the integrated Promissory Note (Pronote) Management module. When an auction winner is announced, the system automatically generates an official legal Promissory Note (PRN-YYYY-XXXX) in pending status and requires the winner to draw their digital signature using an interactive HTML5 Canvas touch/mouse pad before the note is activated and revealed in the Administrator portal.")
    add_p("To ensure operational reliability and zero payment defaults, SecureChit incorporates an automated multi-channel communication engine featuring Fast2SMS Bulk SMS and Nodemailer SMTP email integration for pre-due installment reminders and win declarations. Comprehensive security is maintained through bcrypt password encryption, JWT bearer session tokens, strict input validations, and immutable database audit trails. Overall, the platform eliminates physical paperwork, prevents bid collusion and ledger discrepancies, and delivers a transparent, automated, and legally auditable ROSCA solution for contemporary financial management.")

    add_heading2("1.2 PROJECT DESCRIPTION")
    add_p("Chit funds represent a unique indigenous financial institution in India that combines savings and credit. A group of individuals agrees to contribute a fixed amount of money periodically into a single pool for a specified duration. In every cycle, the collected pool is auctioned to the subscriber willing to accept the highest discount, with the remaining balance (minus foreman commission) distributed equally among all members as a dividend.")
    add_bullet("User Registration & Identity Verification: Onboarding subscribers with identity proof validation and role assignment.")
    add_bullet("Chit Pool Builder: Enabling foremen to define pool value, tenure (months), member capacity, and bid floor discount limits.")
    add_bullet("Live Reverse Bidding Console: Facilitating transparent real-time bidding where members enter discount offers digitally.")
    add_bullet("Automated Dividend Algorithm: Instant calculation of 5% foreman commission, net dividend pool, individual dividend shares, and net payable monthly installments.")
    add_bullet("Promissory Note & Canvas Digital Signature: Auto-generation of official loan Promissory Notes for draw winners with HTML5 canvas touch/mouse signature capture.")
    add_bullet("Installment Ledger & Approval Workflow: Digital logging of payment references, receipt screenshot submission, and one-click admin verification.")

    add_heading2("1.3 PURPOSE & OBJECTIVES")
    add_bullet("Eliminate Paperwork: Replace physical registers, paper receipts, and handwritten passbooks with an encrypted relational database.")
    add_bullet("100% Financial Transparency: Provide real-time visibility into pool value, bid discounts, foreman commission, and individual dividend payouts.")
    add_bullet("Promissory Note Automation: Generate legal Promissory Notes automatically upon auction win, forcing canvas-based digital signatures before admin activation.")

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # SECTION 2: SYSTEM ANALYSIS
    # --------------------------------------------------------------------------
    add_heading1("2. System Analysis")
    add_heading2("2.1 EXISTING SYSTEM ANALYSIS")
    add_p("Currently, most traditional chit fund organizations rely on manual or semi-automated processes. Members are required to physically attend monthly auction meetings, submit handwritten bid slips, and sign physical paper promissory notes.")
    
    add_heading2("2.2 PROPOSED SYSTEM ANALYSIS")
    add_p("The proposed SecureChit system transforms traditional chit operations into a secure web application. Subscribers can register online, view active schemes, bid in live reverse auctions, digitally sign auto-generated Promissory Notes, and track their savings history from any device.")

    add_heading2("2.3 FEASIBILITY STUDY")
    feas_table = doc.add_table(rows=1, cols=3)
    f_hdr = feas_table.rows[0].cells
    f_hdr[0].text = "Feasibility Dimension"
    f_hdr[1].text = "Evaluation Parameters & Criteria"
    f_hdr[2].text = "Feasibility Status"
    feas_data = [
        ("Technical Feasibility", "Uses open-source React 18, FastAPI, PostgreSQL. Low server demands, runs on standard Web infrastructure.", "HIGHLY FEASIBLE"),
        ("Operational Feasibility", "Clean responsive UI tailored for non-technical users. Automated notifications simplify workflow.", "HIGHLY FEASIBLE"),
        ("Economic Feasibility", "Zero software licensing costs. Reduces paper printing, passbooks, and manual collection expenses.", "HIGHLY FEASIBLE"),
        ("Schedule Feasibility", "Designed and deployed within the fifth semester academic timeline.", "HIGHLY FEASIBLE")
    ]
    for item in feas_data:
        r = feas_table.add_row().cells
        r[0].text = item[0]
        r[1].text = item[1]
        r[2].text = item[2]
    style_table(feas_table)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # SECTION 3: SYSTEM CONFIGURATION
    # --------------------------------------------------------------------------
    add_heading1("3. System Configuration")
    add_heading2("3.1 HARDWARE SPECIFICATIONS")
    add_bullet("Processor: Intel Core i5-1235U / AMD Ryzen 5 5500U (2.0 GHz - 4.4 GHz)")
    add_bullet("RAM: 8 GB DDR4 / DDR5")
    add_bullet("Storage: 512 GB NVMe Solid State Drive (SSD)")
    add_bullet("Display: 15.6\" Full HD (1920 x 1080) Color Display")

    add_heading2("3.2 SOFTWARE SPECIFICATIONS")
    add_bullet("Operating System: Windows 11 64-bit / Linux Ubuntu 22.04 LTS")
    add_bullet("Frontend Framework: React 18, Vite, Tailwind CSS, Canvas API, Lucide React Icons")
    add_bullet("Backend Framework: Python 3.11 (FastAPI) / Uvicorn Server")
    add_bullet("Database Engine: PostgreSQL 16 / SQLAlchemy 2.0 ORM")

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # SECTION 4: SYSTEM DESIGN & LARGE GRAPHICAL DFDs
    # --------------------------------------------------------------------------
    add_heading1("4. System Design")
    add_heading2("4.1 DFD SYMBOLS DICTIONARY")
    dfd_table = doc.add_table(rows=1, cols=3)
    d_hdr = dfd_table.rows[0].cells
    d_hdr[0].text = "Symbol Name"
    d_hdr[1].text = "Graphic Notation"
    d_hdr[2].text = "Functional Description in SecureChit"
    dfd_data = [
        ("Data Flow", "---> (Arrow)", "Represents movement of bid data, payment receipts, or alerts."),
        ("Process", "Circle / Ellipse", "Transforms data (e.g., Compute Dividend, Verify Payment)."),
        ("External Entity", "Rectangle", "External actor (Subscriber, Chit Foreman, Fast2SMS API)."),
        ("Data Store", "Open Cylinder", "Database tables (Users DB, Schemes DB, Payments DB).")
    ]
    for item in dfd_data:
        r = dfd_table.add_row().cells
        r[0].text = item[0]
        r[1].text = item[1]
        r[2].text = item[2]
    style_table(dfd_table)

    add_heading2("4.1 DATA FLOW DIAGRAM")

    # DFD 1: Level 0 (Full Page)
    doc.add_page_break()
    add_heading3("Context Level Diagram (Level 0 DFD)")
    if os.path.exists("dfd_level_0.png"):
        p_img0 = doc.add_paragraph()
        p_img0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_img0 = p_img0.add_run()
        r_img0.add_picture("dfd_level_0.png", width=Inches(6.8))
        add_p("Figure : Level 0 Context Diagram showing Member User, Admin Foreman, Central System, and PostgreSQL Database.", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    # DFD 2: Level 1 (Full Page)
    add_heading3("System Overview & Subsystem Decomposition (Level 1 DFD)")
    if os.path.exists("dfd_level_1.png"):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_img1 = p_img1.add_run()
        r_img1.add_picture("dfd_level_1.png", width=Inches(6.8))
        add_p("Figure : Level 1 DFD (Decomposition Diagram)", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    # DFD 3: Level 2 (Full Page)
    add_heading3("Auction Bidding & Workflow (Level 2 DFD)")
    if os.path.exists("dfd_level_2.png"):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_img2 = p_img2.add_run()
        r_img2.add_picture("dfd_level_2.png", width=Inches(6.8))
        add_p("Figure : Level 2 DFD - Auction Bidding and Workflow", italic=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    doc.add_page_break()

    add_heading2("4.3 DATABASE SCHEMA DICTIONARY")
    add_p("Table 1: users (Subscriber & Admin Accounts)", bold=True)
    u_table = doc.add_table(rows=1, cols=4)
    u_hdr = u_table.rows[0].cells
    u_hdr[0].text = "Column Name"; u_hdr[1].text = "Data Type"; u_hdr[2].text = "Constraints"; u_hdr[3].text = "Description"
    u_data = [
        ("user_id", "INTEGER", "PRIMARY KEY, AUTOINC", "Unique identifier for user"),
        ("full_name", "VARCHAR(100)", "NOT NULL", "Full name of subscriber/admin"),
        ("email", "VARCHAR(100)", "UNIQUE, NOT NULL", "Email address for login & alerts"),
        ("phone", "VARCHAR(15)", "UNIQUE, NOT NULL", "Mobile number for Fast2SMS alerts"),
        ("password_hash", "VARCHAR(255)", "NOT NULL", "Bcrypt hashed security password"),
        ("role", "VARCHAR(20)", "DEFAULT 'MEMBER'", "User role ('ADMIN' or 'MEMBER')")
    ]
    for item in u_data:
        r = u_table.add_row().cells
        for idx in range(4): r[idx].text = item[idx]
    style_table(u_table)

    add_p("Table 2: promissory_note (Digital Promissory Notes & Signatures)", bold=True, space_before=12)
    pr_table = doc.add_table(rows=1, cols=4)
    pr_hdr = pr_table.rows[0].cells
    pr_hdr[0].text = "Column Name"; pr_hdr[1].text = "Data Type"; pr_hdr[2].text = "Constraints"; pr_hdr[3].text = "Description"
    pr_data = [
        ("pronote_id", "VARCHAR(50)", "PRIMARY KEY", "Auto-generated PRN-YYYY-XXXX code"),
        ("member_id", "INTEGER", "FOREIGN KEY (users)", "Winning member ID"),
        ("chit_id", "INTEGER", "FOREIGN KEY (plans)", "Associated Chit Plan ID"),
        ("loan_amount", "DECIMAL(12,2)", "NOT NULL", "Net loan amount payout"),
        ("interest_rate", "DECIMAL(5,2)", "DEFAULT 0.00", "Monthly interest rate"),
        ("signature", "TEXT", "NOT NULL", "Base64 encoded HTML5 canvas signature PNG"),
        ("status", "ENUM", "DEFAULT 'pending_signature'", "Status: pending_signature / active / paid")
    ]
    for item in pr_data:
        r = pr_table.add_row().cells
        for idx in range(4): r[idx].text = item[idx]
    style_table(pr_table)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # SECTION 5: SYSTEM IMPLEMENTATION
    # --------------------------------------------------------------------------
    add_heading1("5. System Implementation & Source Code")
    add_heading2("5.1 REQUIREMENTS & VERSION SPECIFICATIONS")
    add_bullet("Python 3.11.4 | FastAPI 0.100.0 | Uvicorn 0.22.0")
    add_bullet("React 18.2.0 | Tailwind CSS 3.3.2 | Canvas API")

    add_heading2("5.2 SAMPLE CODING IMPLEMENTATION")
    add_p("Sample backend financial dividend algorithm, auction draw handler, and HTML5 canvas digital signature encoder are included in the source code repository.")

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # SECTION 6: SYSTEM TESTING
    # --------------------------------------------------------------------------
    add_heading1("6. System Testing")
    add_heading2("6.1 SYSTEM TEST CASES TABLE")
    test_table = doc.add_table(rows=1, cols=5)
    t_hdr = test_table.rows[0].cells
    t_hdr[0].text = "Test ID"; t_hdr[1].text = "Module / Feature"; t_hdr[2].text = "Test Case Description"; t_hdr[3].text = "Expected Result"; t_hdr[4].text = "Status"
    test_data = [
        ("TC-01", "User Authentication", "Submit valid email & password", "Returns JWT access token & redirects to dashboard", "PASSED"),
        ("TC-02", "Scheme Management", "Admin creates scheme with 20 members & ₹10L pool", "Saves scheme in DB and lists under active schemes", "PASSED"),
        ("TC-03", "Reverse Auction", "Member submits bid discount", "Updates lowest bid floor and computes 5% commission", "PASSED"),
        ("TC-04", "Auto Winner Pronote", "Conduct monthly auction draw", "Auto-generates Promissory Note for winner in pending_signature status", "PASSED"),
        ("TC-05", "Member Digital Signature", "Winner draws signature on canvas & submits", "Updates pronote status to active and reveals note in Admin portal", "PASSED"),
        ("TC-06", "Payment Verification", "Member submits UPI transaction UTR reference", "Admin verifies receipt and status updates to PAID", "PASSED"),
        ("TC-07", "Automated Reminders", "Execute due reminder scheduler", "Dispatches Fast2SMS text & Nodemailer SMTP email to unpaid members", "PASSED")
    ]
    for item in test_data:
        r = test_table.add_row().cells
        for idx in range(5): r[idx].text = item[idx]
    style_table(test_table)

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # SECTION 7: SCREENSHOTS
    # --------------------------------------------------------------------------
    add_heading1("7. Screenshots & Interface Walkthrough")
    add_p("1. User Login & Registration Interface: JWT-authenticated credential entry page.")
    add_p("2. Subscriber Dashboard: Overview of subscribed chit plans, total dividend earned, and current dues.")
    add_p("3. Scheme Explorer: Grid of available chit pools with duration, total value, and capacity.")
    add_p("4. Live Bidding Console: Real-time reverse auction console showing lowest bid floor.")
    add_p("5. Digital Promissory Note Signing Modal: HTML5 canvas touchscreen/mouse signature pad with Clear & Save buttons.")
    add_p("6. Admin Dashboard & Promissory Notes Portal: Administrative panel for scheme creation, join approvals, and signed pronotes verification.")

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # SECTION 8: CONCLUSION
    # --------------------------------------------------------------------------
    add_heading1("8. Conclusion")
    add_p("The SecureChit: Digital Chit Fund Management System successfully modernizes traditional chit fund savings and credit operations into a transparent, automated web application. By combining React 18, Python FastAPI, PostgreSQL, and HTML5 Canvas Digital Signatures, the platform eliminates paper record loss, bid manipulation, manual calculation errors, and payment defaults.")

    doc.add_page_break()

    # --------------------------------------------------------------------------
    # SECTION 9 & 10: FUTURE ENHANCEMENTS & BIBLIOGRAPHY
    # --------------------------------------------------------------------------
    add_heading1("9. Future Enhancements")
    add_bullet("Native Mobile Application: React Native app for iOS and Android with push notifications.")
    add_bullet("Biometric & Facial Verification: Aadhaar e-KYC integration using biometric fingerprint & OTP validation.")
    add_bullet("Automated UPI Payment Gateway: Integration of Razorpay / PhonePe UPI intent gateway for auto-reconciliation.")

    add_heading1("10. Bibliography & References")
    add_p("1. Alex Banks & Eve Porcello, \"Learning React: Modern Patterns for Developing React Applications, 2nd Edition\", O'Reilly Media, 2020.")
    add_p("2. David Choi, \"Full-Stack React Projects: Build real-world modern web apps\", Packt Publishing, 2020.")
    add_p("3. React Official Documentation: https://react.dev")
    add_p("4. FastAPI Official Documentation: https://fastapi.tiangolo.com")

    # Save to files
    for filename in ['c:\\chit fund\\SecureChit_Full_Project_Report.docx', 'c:\\chit fund\\SecureChit_Project_Report.docx', 'c:\\chit fund\\report.docx', 'c:\\chit fund\\SecureChit_Report_With_DFDs_v10.docx']:
        try:
            doc.save(filename)
            print(f"Saved docx: {filename}")
        except Exception as e:
            print(f"Could not save {filename}: {e}")

if __name__ == '__main__':
    generate_full_report_docx()

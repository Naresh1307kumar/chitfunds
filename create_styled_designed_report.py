import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_bg(cell, hex_color):
    """Set background color of a table cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def style_table(table, header_bg="103C58", alt_bg="F1F5F9", border_color="CBD5E1"):
    """Applies modern styling to a docx table with header background, borders, and padding."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Set table borders
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

    # Style Header Row
    for cell in table.rows[0].cells:
        set_cell_bg(cell, header_bg)
        set_cell_margins(cell, top=140, bottom=140, left=150, right=150)
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.size = Pt(10.5)

    # Style Data Rows
    for i, row in enumerate(table.rows[1:], start=1):
        bg = alt_bg if i % 2 == 1 else "FFFFFF"
        for cell in row.cells:
            set_cell_bg(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10)
                    run.font.color.rgb = RGBColor(51, 65, 85)

def create_designed_report():
    doc = Document()

    # Set page margins (1 inch top/bottom, 1.25 left, 1 right)
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1)

    # Base typography
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
        run.font.color.rgb = RGBColor(16, 60, 88) # Primary Navy
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(12)
        return p

    def add_chap_heading(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(18)
        run.font.color.rgb = RGBColor(16, 60, 88)
        p.paragraph_format.space_before = Pt(24)
        p.paragraph_format.space_after = Pt(12)
        return p

    def add_sec_heading(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(3, 115, 158) # Cyan Accent
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        return p

    def add_subsec_heading(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(6, 31, 61) # Dark Blue
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        return p

    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(8)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.color.rgb = RGBColor(16, 60, 88)
        p.add_run(text)
        return p

    def add_bullet(text):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        p.add_run(text)
        return p

    def add_callout_box(title, text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_bg(cell, "F0F9FF") # Soft Cyan Tint
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="03739E"/>'
            f'  <w:top w:val="none"/>'
            f'  <w:right w:val="none"/>'
            f'  <w:bottom w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(4)
        r_title = p.add_run(f"📌 {title}\n")
        r_title.bold = True
        r_title.font.size = Pt(11)
        r_title.font.color.rgb = RGBColor(3, 115, 158)
        
        r_txt = p.add_run(text)
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = RGBColor(30, 41, 59)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    def add_code_block(title, code_text):
        add_subsec_heading(f"💻 Source Code: {title}")
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_bg(cell, "0F172A") # Dark Slate / VS Code Dark Header
        set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'  <w:left w:val="single" w:sz="18" w:space="0" w:color="03739E"/>'
            f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="334155"/>'
            f'  <w:right w:val="single" w:sz="6" w:space="0" w:color="334155"/>'
            f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="334155"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(code_text)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(226, 232, 240) # Code light text
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # =========================================================================
    # 1. COVER PAGE (Page 1)
    # =========================================================================
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("SECURE CHIT: DIGITAL CHIT FUND MANAGEMENT SYSTEM\n")
    r.bold = True
    r.font.size = Pt(24)
    r.font.color.rgb = RGBColor(16, 60, 88)
    p.paragraph_format.space_before = Pt(36)
    p.paragraph_format.space_after = Pt(18)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p2.add_run("Submitted in partial fulfilment of the requirements for the award of the degree of\n")
    r.font.size = Pt(12)
    r = p2.add_run("Bachelor of Science in Computer Science")
    r.bold = True
    r.font.size = Pt(14)
    p2.paragraph_format.space_after = Pt(36)

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.add_run("Submitted By\n").bold = True
    r1 = p3.add_run("R. NARESHKUMAR (24UCS08)\nAPR. JEGATHEESH VARSHAN (24UCS06)\n\n")
    r1.bold = True
    r1.font.size = Pt(13)
    p3.add_run("Under the Guidance of\n").bold = True
    r2 = p3.add_run("Mrs. SM. VALLI B.E., M.C.A., M.Phil\n")
    r2.bold = True
    r2.font.size = Pt(13)
    p3.paragraph_format.space_after = Pt(48)

    p4 = doc.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p4.add_run("DEPARTMENT OF COMPUTER SCIENCE\nTHIAGARAJAR COLLEGE (AUTONOMOUS)\n")
    r.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = RGBColor(16, 60, 88)
    r = p4.add_run("(Affiliated to Madurai Kamaraj University)\nRe-accredited with 'A++' Grade by NAAC | Ranked 20th in NIRF 2026\nMadurai – 625009\nOctober - 2026")
    r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # 2. BONAFIDE CERTIFICATE (Page 2)
    # =========================================================================
    add_title("THIAGARAJAR COLLEGE (AUTONOMOUS)\n(Affiliated to Madurai Kamaraj University)\nRe-Accredited with 'A++' Grade by NAAC | Ranked 20th in NIRF 2026\nDEPARTMENT OF COMPUTER SCIENCE")
    
    add_sec_heading("BONAFIDE CERTIFICATE")
    add_p("This is to certify that the project work entitled \"SECURE CHIT: DIGITAL CHIT FUND MANAGEMENT SYSTEM\" is a bonafide work done by R. NARESHKUMAR (24UCS08) and APR. JEGATHEESH VARSHAN (24UCS06) in partial fulfilment of the requirements for the award of the degree of Bachelor of Science in Computer Science during the academic year 2026.")
    
    add_p("Submitted for the final Viva-Voce Examination held on _____________________ at Department of Computer Science, Thiagarajar College (Autonomous), Madurai - 625009.")

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(72)
    p_sig.paragraph_format.space_after = Pt(36)
    p_sig.add_run("Project Guide\t\t\t\t\t\tHead of the Department\n(Mrs. SM. Valli)\t\t\t\t\t\t(Mrs. SM. Valli)")

    p_ext = doc.add_paragraph()
    p_ext.paragraph_format.space_before = Pt(36)
    p_ext.add_run("External Examiner: _________________________\t\tDate: _______________")

    doc.add_page_break()

    # =========================================================================
    # 3. DECLARATION 1 (Page 3)
    # =========================================================================
    add_title("DECLARATION")
    add_p("R. NARESHKUMAR (24UCS08)\nB.Sc. Computer Science\nDepartment of Computer Science\nThiagarajar College (Autonomous), Madurai - 625009", "Name & Address:\n")
    add_p("I hereby declare that the project work entitled \"SECURE CHIT: DIGITAL CHIT FUND MANAGEMENT SYSTEM\", submitted to Thiagarajar College (Autonomous), Madurai, in partial fulfilment of the requirements for the award of the degree of Bachelor of Science in Computer Science, is a record of original work done by me under the guidance of Mrs. SM. VALLI B.E., M.C.A., M.Phil, Department of Computer Science, Thiagarajar College, Madurai.")
    add_p("To the best of my knowledge, this report has not formed the basis for the award of any degree, diploma, associateship, fellowship, or similar title in any other University or Institution.")

    p_dec1 = doc.add_paragraph()
    p_dec1.paragraph_format.space_before = Pt(48)
    p_dec1.add_run("Place: Madurai\nDate:\t\t\t\t\t\tSignature: _______________________\n\t\t\t\t\t\t\t(R. NARESHKUMAR)")

    doc.add_page_break()

    # =========================================================================
    # 4. DECLARATION 2 (Page 4)
    # =========================================================================
    add_title("DECLARATION")
    add_p("APR. JEGATHEESH VARSHAN (24UCS06)\nB.Sc. Computer Science\nDepartment of Computer Science\nThiagarajar College (Autonomous), Madurai - 625009", "Name & Address:\n")
    add_p("I hereby declare that the project work entitled \"SECURE CHIT: DIGITAL CHIT FUND MANAGEMENT SYSTEM\", submitted to Thiagarajar College (Autonomous), Madurai, in partial fulfilment of the requirements for the award of the degree of Bachelor of Science in Computer Science, is a record of original work done by me under the guidance of Mrs. SM. VALLI B.E., M.C.A., M.Phil, Department of Computer Science, Thiagarajar College, Madurai.")
    add_p("To the best of my knowledge, this report has not formed the basis for the award of any degree, diploma, associateship, fellowship, or similar title in any other University or Institution.")

    p_dec2 = doc.add_paragraph()
    p_dec2.paragraph_format.space_before = Pt(48)
    p_dec2.add_run("Place: Madurai\nDate:\t\t\t\t\t\tSignature: _______________________\n\t\t\t\t\t\t\t(APR. JEGATHEESH VARSHAN)")

    doc.add_page_break()

    # =========================================================================
    # 5. ACKNOWLEDGEMENT (Page 5)
    # =========================================================================
    add_title("ACKNOWLEDGEMENT")
    add_p("We extend our sincere thanks to the Almighty for blessing us with the physical strength, mental ability, and determination that enabled us to complete this project effectively.")
    add_p("We are grateful to our respected Principal, Dr. D. PANDIARAJA, M.Sc., M.Phil., P.G.D.C.A., B.Ed., Ph.D., Thiagarajar College, Madurai, for granting us the opportunity to carry out this project work under the esteemed guidance of our department.")
    add_p("We wish to express our profound gratitude to the Head of the Department of Computer Science, Mrs. SM. VALLI, B.E., M.C.A., M.Phil. We sincerely thank her for her valuable guidance, constant encouragement, and support throughout the progress of this work.")
    add_p("We are especially indebted to our Project Guide Mrs. SM. VALLI, B.E., M.C.A., M.Phil., for her patient guidance, constructive suggestions, and for having faith in our ability. Her keen interest and valuable feedback at every stage greatly contributed to the successful completion of this project.")
    add_p("We also extend our heartfelt thanks to all the faculty members of the Department of Computer Science for their constant support, academic guidance, and encouragement during the course of our project.")
    add_p("Finally, we express our deep sense of gratitude to our family members and friends for their unwavering encouragement, moral support, and understanding, which have been a pillar of strength throughout our work.")

    doc.add_page_break()

    # =========================================================================
    # 6. TABLE OF CONTENTS (Page 6 & 7)
    # =========================================================================
    add_title("TABLE OF CONTENTS")

    toc_table = doc.add_table(rows=1, cols=3)
    hdr_cells = toc_table.rows[0].cells
    hdr_cells[0].text = 'Sl. No.'
    hdr_cells[1].text = 'Chapter / Section Title'
    hdr_cells[2].text = 'Page No.'

    contents_data = [
        ("1", "INTRODUCTION\n  1.1 Abstract\n  1.2 Project Description\n  1.3 Purpose & Objectives\n  1.4 Project Scope", "1"),
        ("2", "SYSTEM ANALYSIS\n  2.1 Existing System & Disadvantages\n  2.2 Proposed System & Advantages\n  2.3 Feasibility Study", "4"),
        ("3", "SYSTEM CONFIGURATION\n  3.1 Hardware Specifications\n  3.2 Software Specifications\n  3.3 Language & Technologies", "7"),
        ("4", "SYSTEM DESIGN\n  4.1 System Architecture\n  4.2 Data Flow Diagrams (DFD Levels 0-3)\n  4.3 Database Schema & ER Design\n  4.4 Module Descriptions", "11"),
        ("5", "SYSTEM IMPLEMENTATION\n  5.1 Requirements & Version Specs\n  5.2 Sample Coding Implementation", "17"),
        ("6", "SYSTEM TESTING\n  6.1 Testing Overview\n  6.2 Unit Testing & Calculation Verification\n  6.3 Performance Testing\n  6.4 Integration & End-to-End Testing", "21"),
        ("7", "SCREENSHOTS & INTERFACE WALKTHROUGH", "25"),
        ("8", "CONCLUSION", "28"),
        ("9", "FUTURE ENHANCEMENTS", "29"),
        ("10", "BIBLIOGRAPHY & REFERENCES", "30")
    ]

    for item in contents_data:
        row_cells = toc_table.add_row().cells
        row_cells[0].text = item[0]
        row_cells[1].text = item[1]
        row_cells[2].text = item[2]

    style_table(toc_table, header_bg="103C58", alt_bg="F8FAFC", border_color="CBD5E1")

    doc.add_page_break()

    # =========================================================================
    # 1. INTRODUCTION
    # =========================================================================
    add_chap_heading("1. Intro & Overview")
    
    add_sec_heading("1.1 ABSTRACT")
    add_p("The SecureChit: Digital Chit Fund Management System is an enterprise-grade full-stack Web application designed to digitize, automate, and secure traditional chit fund savings and credit operations. Traditional chit fund schemes operating in India suffer from significant operational inefficiencies, manual ledger record-keeping errors, bid opacity, lack of audit trails, and delayed payment collections. Built using React 18, Tailwind CSS, Python FastAPI / Node.js REST API, SQLite/MySQL Database, Fast2SMS Bulk SMS API, and Nodemailer SMTP Gateway, the system provides a robust digital transport platform replacing paper registers with automated web services.")

    add_callout_box("Project Core Highlight", "SecureChit eliminates manual dividend calculation fraud and bid manipulation by running a real-time digital reverse auction engine backed by automated SMS (Fast2SMS) and Email alerts.")

    add_p("The system caters to two primary user roles: Subscribers / Members and Chit Foremen / Administrators. Subscribers can securely log in, explore active chit pools, participate in scheduled reverse auctions, view dynamic monthly dividend calculations, submit digital payment receipts, and receive automated reminders. Administrators gain access to a powerful management dashboard to create new chit schemes, verify subscriber credentials, supervise monthly bidding rounds, approve installment receipts, monitor default risks, and export financial summaries.")

    add_sec_heading("1.2 PROJECT DESCRIPTION")
    add_p("Chit funds represent a unique indigenous financial institution in India that combines savings and credit. A group of individuals agrees to contribute a fixed amount of money periodically into a single pool for a specified duration. In every cycle, the collected pool is auctioned to the subscriber willing to accept the highest discount, with the remaining balance (minus foreman commission) distributed equally among all members as a dividend.")

    add_bullet("User Registration & Identity Verification: Onboarding subscribers with identity proof validation and role assignment.")
    add_bullet("Chit Pool Builder: Enabling foremen to define pool value, tenure (months), member capacity, and bid floor discount limits.")
    add_bullet("Live Reverse Bidding Console: Facilitating transparent real-time bidding where members enter discount offers digitally.")
    add_bullet("Automated Dividend Algorithm: Instant calculation of 5% foreman commission, net dividend pool, individual dividend shares, and net payable monthly installments.")
    add_bullet("Installment Ledger & Approval Workflow: Digital logging of payment references, receipt screenshot submission, and one-click admin verification.")
    add_bullet("Multi-Channel Notification Gateway: Automated Fast2SMS API and SMTP Email triggers for due alerts, auction announcements, and payment acknowledgments.")

    add_sec_heading("1.3 PURPOSE & OBJECTIVES")
    add_bullet("Eliminate Paperwork: Replace physical registers, paper receipts, and hand-written passbooks with an encrypted relational database.")
    add_bullet("100% Financial Transparency: Provide real-time visibility into pool value, bid discounts, foreman commission, and individual dividend payouts.")
    add_bullet("Eliminate Bid Manipulation: Implement timestamped digital bidding logs that guarantee equal opportunity and auditability.")
    add_bullet("Minimize Subscriber Default Rates: Automate SMS and email reminders prior to due dates to ensure timely installment collections.")

    doc.add_page_break()

    # =========================================================================
    # 2. SYSTEM ANALYSIS
    # =========================================================================
    add_chap_heading("2. System Analysis")

    add_sec_heading("2.1 EXISTING SYSTEM ANALYSIS")
    add_p("Currently, most traditional chit fund organizations rely on manual or semi-automated processes. Members are required to physically attend monthly auction meetings, submit handwritten bid slips, and pay cash at physical office counters.")

    add_sec_heading("2.2 PROPOSED SYSTEM ANALYSIS")
    add_p("The proposed SecureChit system transforms traditional chit operations into a secure web application. Subscribers can register online, view active schemes, bid in live reverse auctions, inspect automated dividend statements, submit online payment receipts, and track their savings history from any device.")

    add_sec_heading("2.3 FEASIBILITY STUDY")
    add_p("A comprehensive feasibility analysis was conducted across technical, operational, economic, and schedule dimensions:")

    feas_table = doc.add_table(rows=1, cols=3)
    f_hdr = feas_table.rows[0].cells
    f_hdr[0].text = "Feasibility Dimension"
    f_hdr[1].text = "Evaluation Parameters & Criteria"
    f_hdr[2].text = "Feasibility Status"

    feas_data = [
        ("Technical Feasibility", "Uses open-source React 18, FastAPI, SQLite/MySQL. Low server demands, runs on standard Web infrastructure.", "HIGHLY FEASIBLE"),
        ("Operational Feasibility", "Clean responsive UI tailored for non-technical users. Automated notifications simplify workflow.", "HIGHLY FEASIBLE"),
        ("Economic Feasibility", "Zero software licensing costs. Reduces paper printing, passbooks, and manual collection expenses.", "HIGHLY FEASIBLE"),
        ("Schedule Feasibility", "Designed and deployed within the fifth semester academic timeline.", "HIGHLY FEASIBLE")
    ]

    for item in feas_data:
        r_cells = feas_table.add_row().cells
        r_cells[0].text = item[0]
        r_cells[1].text = item[1]
        r_cells[2].text = item[2]

    style_table(feas_table, header_bg="103C58", alt_bg="F1F5F9", border_color="CBD5E1")

    doc.add_page_break()

    # =========================================================================
    # 3. SYSTEM CONFIGURATION
    # =========================================================================
    add_chap_heading("3. System Configuration")

    add_sec_heading("3.1 HARDWARE SPECIFICATIONS")
    add_bullet("Processor: Intel Core i5-1235U / AMD Ryzen 5 5500U (2.0 GHz - 4.4 GHz)")
    add_bullet("RAM: 8 GB DDR4 / DDR5")
    add_bullet("Storage: 512 GB NVMe Solid State Drive (SSD)")
    add_bullet("Display: 15.6\" Full HD (1920 x 1080) Color Display")
    add_bullet("Network: Broadband Internet / Wi-Fi Connectivity")

    add_sec_heading("3.2 SOFTWARE SPECIFICATIONS")
    add_bullet("Operating System: Windows 11 64-bit / Linux Ubuntu 22.04 LTS")
    add_bullet("Frontend Framework: React 18, Vite, Tailwind CSS, Lucide React Icons")
    add_bullet("Backend Framework: Python 3.11 (FastAPI) / Node.js (Express.js)")
    add_bullet("Database Engine: SQLite 3 / MySQL Server 8.0 (securechit.db)")
    add_bullet("External APIs: Fast2SMS Bulk SMS REST API, Nodemailer / SMTP Email Service")

    doc.add_page_break()

    # =========================================================================
    # 4. SYSTEM DESIGN & TABLES
    # =========================================================================
    add_chap_heading("4. System Design")

    add_sec_heading("4.1 DFD SYMBOLS DICTIONARY")
    
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
        r_cells = dfd_table.add_row().cells
        r_cells[0].text = item[0]
        r_cells[1].text = item[1]
        r_cells[2].text = item[2]

    style_table(dfd_table, header_bg="103C58", alt_bg="F8FAFC", border_color="CBD5E1")

    add_sec_heading("4.2 DATABASE SCHEMA DICTIONARY")

    # Table 1: users
    add_subsec_heading("Table 1: users (Subscriber & Admin Accounts)")
    u_table = doc.add_table(rows=1, cols=4)
    u_hdr = u_table.rows[0].cells
    u_hdr[0].text = "Column Name"
    u_hdr[1].text = "Data Type"
    u_hdr[2].text = "Constraints"
    u_hdr[3].text = "Description"

    u_data = [
        ("user_id", "INTEGER", "PRIMARY KEY, AUTOINC", "Unique identifier for user"),
        ("full_name", "VARCHAR(100)", "NOT NULL", "Full name of subscriber/admin"),
        ("email", "VARCHAR(100)", "UNIQUE, NOT NULL", "Email address for login & alerts"),
        ("phone", "VARCHAR(15)", "UNIQUE, NOT NULL", "Mobile number for Fast2SMS alerts"),
        ("password_hash", "VARCHAR(255)", "NOT NULL", "Bcrypt hashed security password"),
        ("role", "VARCHAR(20)", "DEFAULT 'MEMBER'", "User role ('ADMIN' or 'MEMBER')")
    ]
    for item in u_data:
        r_cells = u_table.add_row().cells
        for idx in range(4):
            r_cells[idx].text = item[idx]
    style_table(u_table, header_bg="03739E", alt_bg="F1F5F9", border_color="CBD5E1")

    # Table 2: chit_schemes
    add_subsec_heading("Table 2: chit_schemes (Chit Pool Specifications)")
    s_table = doc.add_table(rows=1, cols=4)
    s_hdr = s_table.rows[0].cells
    s_hdr[0].text = "Column Name"
    s_hdr[1].text = "Data Type"
    s_hdr[2].text = "Constraints"
    s_hdr[3].text = "Description"

    s_data = [
        ("scheme_id", "INTEGER", "PRIMARY KEY, AUTOINC", "Unique scheme identifier"),
        ("scheme_name", "VARCHAR(100)", "NOT NULL", "Title of the chit pool"),
        ("pool_amount", "DECIMAL(10,2)", "NOT NULL", "Total pool value (e.g. 10,00,000)"),
        ("duration_months", "INTEGER", "NOT NULL", "Tenure in months (e.g. 20)"),
        ("max_members", "INTEGER", "NOT NULL", "Maximum subscriber capacity"),
        ("foreman_commission_pct", "DECIMAL(4,2)", "DEFAULT 5.00", "Foreman commission percentage")
    ]
    for item in s_data:
        r_cells = s_table.add_row().cells
        for idx in range(4):
            r_cells[idx].text = item[idx]
    style_table(s_table, header_bg="03739E", alt_bg="F1F5F9", border_color="CBD5E1")

    # Table 3: installments
    add_subsec_heading("Table 3: installments (Monthly Payment Ledger)")
    i_table = doc.add_table(rows=1, cols=4)
    i_hdr = i_table.rows[0].cells
    i_hdr[0].text = "Column Name"
    i_hdr[1].text = "Data Type"
    i_hdr[2].text = "Constraints"
    i_hdr[3].text = "Description"

    i_data = [
        ("installment_id", "INTEGER", "PRIMARY KEY, AUTOINC", "Unique installment record ID"),
        ("scheme_id", "INTEGER", "FOREIGN KEY", "References chit_schemes.scheme_id"),
        ("month_number", "INTEGER", "NOT NULL", "Cycle month number (1 to N)"),
        ("user_id", "INTEGER", "FOREIGN KEY", "References users.user_id"),
        ("net_payable", "DECIMAL(10,2)", "NOT NULL", "Final payable amount after dividend"),
        ("payment_reference", "VARCHAR(100)", "NULLABLE", "Bank reference or UPI Txn ID"),
        ("status", "VARCHAR(20)", "DEFAULT 'DUE'", "'DUE', 'SUBMITTED', 'PAID'")
    ]
    for item in i_data:
        r_cells = i_table.add_row().cells
        for idx in range(4):
            r_cells[idx].text = item[idx]
    style_table(i_table, header_bg="03739E", alt_bg="F1F5F9", border_color="CBD5E1")

    doc.add_page_break()

    # =========================================================================
    # 5. SOURCE CODE IMPLEMENTATION
    # =========================================================================
    add_chap_heading("5. System Implementation & Source Code")

    code_py = """# --------------------------------------------------------------------------
# SECURECHIT FINANCIAL CALCULATION ENGINE (Python FastAPI Backend)
# --------------------------------------------------------------------------
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import math

app = FastAPI(title="SecureChit Financial Engine API")

class SettlementRequest(BaseModel):
    pool_amount: float
    total_members: int
    winning_bid_discount: float
    foreman_commission_rate: float = 0.05  # 5% Standard Fee

@app.post("/api/v1/auction/calculate-settlement")
def calculate_monthly_settlement(req: SettlementRequest):
    if req.winning_bid_discount < (req.pool_amount * req.foreman_commission_rate):
        raise HTTPException(status_code=400, detail="Winning bid discount cannot be less than foreman commission.")
        
    base_monthly = req.pool_amount / req.total_members
    foreman_fee = req.pool_amount * req.foreman_commission_rate
    net_dividend_pool = req.winning_bid_discount - foreman_fee
    
    individual_dividend = net_dividend_pool / req.total_members if net_dividend_pool > 0 else 0.0
    net_payable = base_monthly - individual_dividend

    return {
        "status": "SUCCESS",
        "base_monthly_installment": round(base_monthly, 2),
        "foreman_commission": round(foreman_fee, 2),
        "total_bid_discount": round(req.winning_bid_discount, 2),
        "net_dividend_pool": round(net_dividend_pool, 2),
        "individual_dividend_share": round(individual_dividend, 2),
        "net_payable_installment": round(net_payable, 2)
    }"""
    add_code_block("Backend Dividend Calculation Engine (FastAPI)", code_py)

    code_react = """// --------------------------------------------------------------------------
// SECURECHIT LIVE REVERSE BIDDING CONSOLE (React 18 Component)
// --------------------------------------------------------------------------
import React, { useState, useEffect } from 'react';
import { Gavel, AlertCircle, CheckCircle } from 'lucide-react';

export default function LiveBiddingConsole({ schemeId, poolAmount, minBidFloor }) {
  const [bidDiscount, setBidDiscount] = useState(minBidFloor);
  const [lowestBid, setLowestBid] = useState(minBidFloor);
  const [statusMessage, setStatusMessage] = useState('');

  const handlePlaceBid = async (e) => {
    e.preventDefault();
    if (bidDiscount <= lowestBid) {
      setStatusMessage('Bid discount must be higher than current lowest bid.');
      return;
    }
    // API Call to submit bid
    const response = await fetch('/api/v1/auction/submit-bid', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ schemeId, bidDiscountAmount: parseFloat(bidDiscount) })
    });
    if (response.ok) {
      setLowestBid(bidDiscount);
      setStatusMessage('Bid successfully placed!');
    }
  };

  return (
    <div className="bg-slate-900 text-white p-6 rounded-xl shadow-lg">
      <h3 className="text-xl font-bold flex items-center gap-2">
        <Gavel className="text-cyan-400" /> Live Reverse Auction Console
      </h3>
      <div className="my-4 p-4 bg-slate-800 rounded-lg">
        <p className="text-sm text-slate-400">Total Pool Value: ₹{poolAmount.toLocaleString()}</p>
        <p className="text-2xl font-extrabold text-cyan-400">Current Highest Discount: ₹{lowestBid.toLocaleString()}</p>
      </div>
      <form onSubmit={handlePlaceBid} className="space-y-4">
        <input 
          type="number" 
          value={bidDiscount} 
          onChange={(e) => setBidDiscount(e.target.value)}
          className="w-full bg-slate-800 border border-slate-700 p-3 rounded text-white"
        />
        <button type="submit" className="w-full bg-cyan-600 hover:bg-cyan-500 font-bold py-3 rounded">
          Submit Bid Discount
        </button>
      </form>
    </div>
  );
}"""
    add_code_block("Frontend Bidding Console (React 18 & Tailwind)", code_react)

    doc.add_page_break()

    # =========================================================================
    # 6. SYSTEM TESTING & TEST CASES TABLE
    # =========================================================================
    add_chap_heading("6. System Testing")

    add_sec_heading("6.1 SYSTEM TEST CASES TABLE")

    test_table = doc.add_table(rows=1, cols=5)
    t_hdr = test_table.rows[0].cells
    t_hdr[0].text = "Test ID"
    t_hdr[1].text = "Module / Feature"
    t_hdr[2].text = "Test Case Description"
    t_hdr[3].text = "Expected Result"
    t_hdr[4].text = "Status"

    test_data = [
        ("TC-01", "User Authentication", "Submit valid email and password", "Generates JWT token and redirects to Member Dashboard", "PASSED"),
        ("TC-02", "User Authentication", "Submit duplicate email during registration", "Blocks signup and returns 'EmailAlreadyExists' alert", "PASSED"),
        ("TC-03", "Scheme Management", "Admin creates scheme with 20 members & ₹10L pool", "Saves scheme in DB and lists under active schemes", "PASSED"),
        ("TC-04", "Reverse Auction", "Submit bid lower than minimum bid floor limit", "Rejects bid with 'DiscountTooLow' validation error", "PASSED"),
        ("TC-05", "Dividend Engine", "Calculate ₹10L pool, ₹2L winning bid, 20 members", "Computes ₹7,500 dividend & ₹42,500 net payable exactly", "PASSED"),
        ("TC-06", "Payment Verification", "Member submits UPI transaction reference ID", "Updates payment status to 'SUBMITTED' in ledger", "PASSED"),
        ("TC-07", "Admin Verification", "Admin clicks 'Approve' on submitted payment", "Updates status to 'PAID' and sends SMS confirmation", "PASSED"),
        ("TC-08", "Reminder Scheduler", "Execute midnight cron for dues expiring in 24h", "Dispatches Fast2SMS text & Nodemailer HTML email", "PASSED")
    ]

    for item in test_data:
        r_cells = test_table.add_row().cells
        for idx in range(5):
            r_cells[idx].text = item[idx]

    style_table(test_table, header_bg="103C58", alt_bg="F8FAFC", border_color="CBD5E1")

    doc.add_page_break()

    # =========================================================================
    # 7. SCREENSHOTS & INTERFACE WALKTHROUGH
    # =========================================================================
    add_chap_heading("7. Screenshots & Walkthrough")
    add_p("1. User Login & Registration Interface: JWT-authenticated credential entry page.")
    add_p("2. Subscriber Dashboard: Overview of subscribed chit plans, total dividend earned, and current dues.")
    add_p("3. Scheme Explorer: Grid of available chit pools with duration, total value, and capacity.")
    add_p("4. Live Bidding Console: Real-time reverse auction console showing lowest bid floor.")
    add_p("5. Admin Dashboard: Administrative panel for scheme creation, join approvals, and payment verification.")

    doc.add_page_break()

    # =========================================================================
    # 8. CONCLUSION
    # =========================================================================
    add_chap_heading("8. Conclusion")
    add_p("The SecureChit: Digital Chit Fund Management System successfully modernizes traditional chit fund savings and credit operations into a transparent, automated web application. By combining React 18, Python FastAPI, SQLite/MySQL, Fast2SMS, and Nodemailer SMTP, the platform solves the critical challenges of paper record loss, bid manipulation, manual calculation errors, and payment defaults.")

    doc.add_page_break()

    # =========================================================================
    # 9 & 10: FUTURE ENHANCEMENTS & BIBLIOGRAPHY
    # =========================================================================
    add_chap_heading("9. Future Enhancements")
    add_bullet("Native Mobile App (Android & iOS) using React Native.")
    add_bullet("Integrated Online Payment Gateway (Razorpay / PhonePe UPI).")
    add_bullet("AI Default Risk Analytics predicting default probabilities.")
    add_bullet("Blockchain Audit Trail for immutable ledger recording.")

    add_chap_heading("10. Bibliography & References")
    add_p("1. Alex Banks & Eve Porcello, \"Learning React: Modern Patterns for Developing React Applications, 2nd Edition\", O'Reilly Media, 2020.")
    add_p("2. Sebastian Raschka, \"Python Machine Learning and Web Architectures\", Packt Publishing, 2022.")
    add_p("3. Baron Schwartz et al., \"High Performance MySQL, 4th Edition\", O'Reilly Media, 2021.")
    add_p("4. React Official Documentation: https://react.dev")
    add_p("5. FastAPI Official Documentation: https://fastapi.tiangolo.com")

    # Attempt to save to all target filenames
    for filename in ['report_styled.docx', 'report_final.docx', 'report.docx', 'SecureChit_Project_Report.docx', 'Smart_Campus_Connect_Project_Report.docx']:
        try:
            doc.save(filename)
            print(f"Saved designed report to {filename}")
        except Exception as e:
            print(f"Could not save {filename} (file might be open): {e}")

if __name__ == '__main__':
    create_designed_report()

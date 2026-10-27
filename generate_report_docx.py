import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = Document()

    # Set page margins (1 inch on all sides)
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

    # Helper function to add styled headings
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

    # -------------------------------------------------------------
    # 1. FRONT PAGE / COVER PAGE
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = title_p.add_run("SMART CAMPUS CONNECT")
    r.bold = True
    r.font.size = Pt(24)
    r.font.color.rgb = RGBColor(16, 60, 88)
    title_p.paragraph_format.space_before = Pt(24)
    title_p.paragraph_format.space_after = Pt(18)

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
    
    r_aff = inst_p.add_run("(Affiliated to Madurai Kamaraj University)\nRe-accredited with ‘A++’ Grade by NAAC\nRanked 20th in NIRF 2024\nMadurai – 625009\n\nOctober – 2025")
    r_aff.font.size = Pt(11)
    inst_p.paragraph_format.space_after = Pt(12)

    doc.add_page_break()

    # -------------------------------------------------------------
    # 2. BONAFIDE CERTIFICATE
    # -------------------------------------------------------------
    cert_h = doc.add_paragraph()
    cert_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = cert_h.add_run("Thiagarajar College (Autonomous)\n")
    r.bold = True
    r.font.size = Pt(14)
    r_sub = cert_h.add_run("(Affiliated to Madurai Kamaraj University)\nRe-Accredited with ‘A++’ Grade by NAAC\nRanked 20th in NIRF\nDepartment of Computer Science\n")
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
    r_proj = cert_body.add_run("SMART CAMPUS CONNECT")
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

    # -------------------------------------------------------------
    # 3. DECLARATIONS
    # -------------------------------------------------------------
    # Declaration 1
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
    d1_b.add_run("SMART CAMPUS CONNECT").bold = True
    d1_b.add_run("” has been done thoroughly at the outset of my knowledge and has not been drafted out to any other modes of information. This software has been purely done by me.")

    d1_sig = doc.add_paragraph()
    d1_sig.add_run("Place: Madurai\nDate: \t\t\t\t\t\t\tSignature\n\t\t\t\t\t\t\tR. Nareshkumar (24UCS08)")
    d1_sig.paragraph_format.space_after = Pt(36)

    # Declaration 2
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
    d2_b.add_run("SMART CAMPUS CONNECT").bold = True
    d2_b.add_run("” has been done thoroughly at the outset of my knowledge and has not been drafted out to any other modes of information. This software has been purely done by me.")

    d2_sig = doc.add_paragraph()
    d2_sig.add_run("Place: Madurai\nDate: \t\t\t\t\t\t\tSignature\n\t\t\t\t\t\t\tAPR. Jegatheesh Varshan (24UCS06)")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 4. ACKNOWLEDGEMENT
    # -------------------------------------------------------------
    ack_t = doc.add_paragraph()
    ack_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = ack_t.add_run("ACKNOWLEDGEMENT")
    r.bold = True
    r.font.size = Pt(16)
    r.font.underline = True
    ack_t.paragraph_format.space_after = Pt(18)

    ack_b1 = add_body_p("We extend our sincere thanks to the almighty for giving us physical, mental strength and ability for the effective completion of this project.")
    ack_b2 = add_body_p("We would be grateful to the principal Dr. D. PANDIARAJA M.Sc., M.Phil, P.G.D.C.A., B.ED., Ph.D., Thiagarajar College, Madurai for his encouragement to take up this project.")
    ack_b3 = add_body_p("We would like to express our profound gratitude for the support offered by our Head of the department of Computer science Mrs. S. M. VALLI B.E., M.C.A., M.Phil. We would also thank her who guided and encouraged in this project work. We would also extend our sincere thanks to our Project guide Mrs. S. M. VALLI B.E., M.C.A., M.Phil. We will be grateful to her for having faith in our ability and entrusting us.")
    ack_b4 = add_body_p("We thank faculty members of the Computer Science department for their guidance. We also personally thank our family members and friends for their continuous encouragement.")

    doc.add_page_break()

    # -------------------------------------------------------------
    # 5. CONTENTS PAGE (Only 1, 2, 3, 4, 8, 9, 10)
    # -------------------------------------------------------------
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
        ("1", "INTRODUCTION\n  1.1 Abstract\n  1.2 Project Description", "2\n3"),
        ("2", "SYSTEM ANALYSIS\n  2.1 Existing System\n  2.2 Proposed System", "5\n5"),
        ("3", "SYSTEM CONFIGURATION\n  3.1 Hardware Specification\n  3.2 Software Specification\n  About The Language", "6\n6\n7"),
        ("4", "SYSTEM DESIGN\n  4.1 Data Flow Diagram\n  4.2 Module Design\n  4.3 Module Description", "11\n12\n15"),
        ("8", "CONCLUSION", "62"),
        ("9", "FUTURE ENHANCEMENT", "65"),
        ("10", "BIBLIOGRAPHY", "67"),
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

    # -------------------------------------------------------------
    # 6. MAIN CONTENT SECTIONS (1, 2, 3, 4, 8, 9, 10)
    # -------------------------------------------------------------

    # SECTION 1: INTRODUCTION
    add_sec_heading("1. INTRODUCTION")
    
    add_subsec_heading("1.1 ABSTRACT")
    add_body_p("In today’s academic environment, educational institutions manage large volumes of data related to students, staff, and administration. Manual processes and disconnected digital tools often lead to inefficiency, errors, and delayed communication. To overcome these challenges, Smart Campus Connect has been developed as a comprehensive College Management System using the MERN stack (MongoDB, Express.js, React.js, Node.js).")
    add_body_p("The system provides a centralized platform for academic and administrative tasks with role-based access for administrators and staff. Administrators can manage student records, staff details, and events, while staff can handle attendance, departmental communication, and academic updates. Students do not have login access; instead, they receive email notifications and SMS alerts about attendance, events, and announcements, keeping both students and parents informed.")
    add_body_p("A major feature is the communication module, which ensures seamless interaction between the institution and stakeholders. Attendance tracking is automated with SMS alerts to parents of absent students. Event details and academic updates are shared through targeted email notifications. The system also maintains student profiles with personal, departmental, and academic information, updated by staff and accessible to administrators.")
    add_body_p("With features like a dashboard displaying real-time analytics, department-wise student counts, and detailed profiles, Smart Campus Connect reduces paperwork, minimizes errors, and enables fast communication. It bridges the gap between traditional college practices and digital solutions.")
    add_body_p("The system is designed with future scalability in mind, allowing integration of mobile applications, AI-driven analytics, and online examination modules. By automating processes and improving coordination, Smart Campus Connect builds the foundation of a truly smart campus, enhancing efficiency and academic experience for administrators, staff, students, and parents alike.")

    add_subsec_heading("1.2 PROJECT DESCRIPTION")
    add_body_p("The project Smart Campus Connect is developed to streamline academic and administrative processes in colleges using the MERN stack (MongoDB, Express.js, React.js, Node.js). It provides a centralized digital platform for managing student data, attendance, staff activities, and event notifications while ensuring reliable communication with students and parents through email and SMS integration.")
    add_body_p("The following stages summarize the system:")
    
    add_body_p("The system uses role-based authentication to ensure security and proper access. Administrators manage student data, staff information, and events. Staff handle attendance, departmental updates, and communications. Students do not have login access; they only receive email notifications and SMS alerts for attendance, events, and announcements. This approach ensures controlled access and data privacy.", bold_prefix="1. User Authentication: ")
    
    add_body_p("The system follows a modular MERN architecture comprising React.js (Frontend user interface with dashboards, forms, and tables), Express.js & Node.js (Backend logic, API endpoints, and communication), MongoDB (Database storing student, staff, and event records), and SMS/Email APIs for notifications. The modular design ensures easy maintenance and scalability.", bold_prefix="2. System Design: ")

    add_body_p("Core features include Student data management, Attendance monitoring with SMS to parents of absentees, Department-wise email notifications for events and academic updates, and Dashboard with real-time analytics (student count, department-wise data).", bold_prefix="3. Feature Development: ")

    add_body_p("The system uses MongoDB to manage student, staff, and event data. Stores student ID, name, department, email, mobile, community, blood group, and photo. Attendance records, internal and external marks are linked to student profiles. Data is structured for future scalability.", bold_prefix="4. Database Management: ")

    add_body_p("The project underwent multiple testing stages: Unit Testing (checking each module individually), Integration Testing (ensuring frontend, backend, and database work together), System Testing (validating real-time functioning and notifications), and Debugging (fixing issues like SMS/email errors and data retrieval problems).", bold_prefix="5. Testing and Debugging: ")

    add_body_p("The system was deployed on cloud platforms such as Render/Railway for backend and web hosting for frontend. Evaluation focused on Performance (fast and responsive), Usability (simple interface for non-technical staff), Reliability (accurate SMS and email delivery), and Scalability (ability to grow with future institutional needs).", bold_prefix="6. Deployment and Evaluation: ")

    # SECTION 2: SYSTEM ANALYSIS
    add_sec_heading("2. SYSTEM ANALYSIS")
    add_body_p("System analysis involves studying the current methods of managing college activities, identifying drawbacks, and proposing a more efficient system.")

    add_subsec_heading("2.1 EXISTING SYSTEM")
    add_body_p("In most colleges, records are maintained manually or with basic tools like spreadsheets. Attendance is marked in registers, event details are shared on notice boards, and communication with parents is delayed. This leads to:")
    add_body_p("• Time-consuming processes.\n• Higher chances of human error.\n• Difficulty in retrieving and updating student data.\n• Lack of instant communication with students and parents.")
    add_body_p("The existing system, while functional, is inefficient, error-prone, and unsuitable for modern institutions.")

    add_subsec_heading("2.2 PROPOSED SYSTEM")
    add_body_p("The proposed Smart Campus Connect provides a centralized digital platform built on the MERN stack. It addresses existing challenges by offering:")
    add_body_p("• Centralized Data Management – student and staff details stored securely in MongoDB.\n• Role-Based Access – logins for administrators and staff; students only receive emails/SMS alerts.\n• Automated Attendance Monitoring – absentees’ parents notified instantly via SMS.\n• Efficient Communication – department-wise email notifications for events and updates.\n• Dashboard Analytics – real-time student counts and department-wise reports.\n• Student Profile Management – complete record with ID, department, email, mobile, community, blood group, and photo.")
    add_body_p("Conclusion: The proposed system minimizes paperwork, reduces errors, and ensures faster communication. It transforms the traditional college environment into a smart, connected campus with scope for future enhancements like mobile integration, AI analytics, and online exams.")

    # SECTION 3: SYSTEM CONFIGURATION
    add_sec_heading("3. SYSTEM CONFIGURATION")
    
    add_subsec_heading("3.1 HARDWARE SPECIFICATIONS")
    add_body_p("Processor: AMD Ryzen 3 7320U with Radeon Graphics, 2.40 GHz\nRAM: 8 GB\nStorage: 500 GB SSD for server, 250 GB HDD/SSD for client machines\nMonitor: Standard 15-inch display with 1024×768 resolution\nNetwork: Stable broadband internet connection for real-time communication, email, and SMS notifications")

    add_subsec_heading("3.2 SOFTWARE SPECIFICATIONS")
    add_body_p("Operating System: Windows 11 (Version 23H2), 64-bit, x64-based processor\nFrontend Technologies: React.js, Tailwind CSS\nBackend Technologies: Node.js with Express.js framework\nDatabase: MongoDB for storing student, staff, and event-related data\nODM Tool: Mongoose for managing database interactions\nCommunication Tools: Nodemailer for email notifications, Fast2SMS API for SMS alerts")

    add_subsec_heading("3.3 ABOUT THE LANGUAGE & TECHNOLOGIES")
    add_body_p("FRONT-END TECHNOLOGY: React.js, TailwindCSS\nBACK-END TECHNOLOGY: Node.js, Express.js, MongoDB")
    add_body_p("Front-end technologies refer to the set of tools, frameworks, and programming languages that enable developers to design the part of an application visible to end users. In Smart Campus Connect, the front end is developed using React.js and styled with TailwindCSS, providing modular, reusable components for responsive user interaction.", bold_prefix="Front-End Technologies: ")
    add_body_p("The backend forms the foundation of the application, managing server-side logic, routing, database interactions, and secure communication. Built using Node.js and Express.js, it handles student and staff records, asynchronous mail/SMS notifications, and API routes efficiently.", bold_prefix="Back-End Technologies: ")
    add_body_p("MongoDB is a NoSQL document database used to manage student profiles, staff details, attendance records, and events. Its flexible JSON-like document structure allows quick querying and seamless horizontal scalability.", bold_prefix="Database Technology: ")

    # SECTION 4: SYSTEM DESIGN
    add_sec_heading("4. SYSTEM DESIGN")

    add_subsec_heading("4.1 DATA FLOW DIAGRAM (DFD)")
    add_body_p("The Data Flow Diagram (DFD) is a graphical representation of the flow of data through an information system. It depicts data sources, data destinations, processes, and data stores.")

    # DFD Symbol table
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
        ("Circle / Ellipse", "Process", "Performs transformations on input data to yield output data."),
        ("Parallelogram", "Input / Output", "Represents input or output operations where data is received or displayed."),
        ("Rectangle", "External Entity", "A source of system inputs or sink of system outputs."),
        ("Open Rectangle / Cylinder", "Data Store", "Repository of data; arrowheads indicate inputs/outputs to the store.")
    ]
    for idx, (sym, nm, fn) in enumerate(dfd_syms, start=1):
        rc = dfd_tbl.rows[idx].cells
        rc[0].paragraphs[0].text = sym
        rc[1].paragraphs[0].text = nm
        rc[2].paragraphs[0].text = fn

    add_subsec_heading("4.2 MODULE DESIGN")
    add_body_p("• Level 0 DFD: Overview of Login -> Admin/Staff -> Dashboard -> Database.\n• Level 1 DFD: Homepage -> Login -> Admin / Staff Dashboard -> Database.\n• Level 2 DFD: Admin Dashboard detailed hierarchy (Students, Staff, Events, Results).\n• Level 3 DFD: Staff Dashboard detailed hierarchy (Attendance, Events, Internal Marks, HOD Report Generation).")

    add_subsec_heading("4.3 MODULE DESCRIPTION")
    add_body_p("LEVEL 0 AND LEVEL 1: Smart Campus Connect provides a secure role-based authentication platform allowing Admin, Staff, and HOD to access the system via centralized login validation.")
    add_body_p("LEVEL 2 (Admin Dashboard): Admin manages Student records, Staff details, Event scheduling, and Result Publishing (external marks entry, scheduling publish date, automatic email marksheet dispatch).")
    add_body_p("LEVEL 3 (Staff / HOD Dashboard): Staff marks attendance, enters internal assessment marks (Internal 1, 2, Quiz, Seminar, Assignment). If HOD role is active, consolidated class report generation and Excel export functionality are enabled.")

    # SECTION 8: CONCLUSION
    add_sec_heading("8. CONCLUSION")
    add_body_p("The Smart Campus Connect System is designed to modernize and streamline campus management by integrating academics, administration, and communication into a unified digital platform. Its structured architecture ensures smooth navigation and efficient handling of tasks for administrators, staff, HODs, and students, making it an ideal solution for institutions aiming to enhance productivity and communication.")
    add_body_p("The system provides role-based access: administrators, HODs, and staff members have customized dashboards with relevant features. The familiar web-based interface ensures ease of use, while the enhanced functionalities bring automation, transparency, and improved coordination across the campus ecosystem.")
    add_body_p("The Admin Dashboard offers features to add, edit, view, and manage student and staff records. Admins can send notifications via email or SMS for events, scholarships, and urgent needs. The Events Module allows admins to create events and instantly send invitations to students. The Result Management Module enables admins to enter external marks, schedule result publication, and automatically generate student marksheets linked to their profiles.")
    add_body_p("The Staff Dashboard empowers faculty members with tools for student engagement and academic management. Staff can view student details, organize departmental events, mark attendance (notifying parents via SMS for absentees and low attendance), and enter internal assessment marks.")
    add_body_p("For HODs, additional features such as consolidated report generation are provided, supporting effective academic monitoring. Overall, the system replaces manual paperwork with a fast, automated, and secure digital platform.")

    # SECTION 9: FUTURE ENHANCEMENT
    add_sec_heading("9. FUTURE ENHANCEMENT")
    add_body_p("• Automated Attendance System: Integration of biometric or RFID-based attendance to automatically record student presence, reducing manual effort and ensuring higher accuracy.")
    add_body_p("• Library Management Integration: A digital library system can be combined with the platform to manage book issues, returns, and fines with automated alerts.")
    add_body_p("• Vehicle Fee Management: Transport management module to handle student bus fees, reminders, and payment tracking.")
    add_body_p("• Mobile Application Support: Extending the system to Android and iOS mobile applications for instant push notifications and real-time tracking.")
    add_body_p("• AI-Based Analytics: Advanced predictive analytics for evaluating student academic performance trends and attendance forecasting.")

    # SECTION 10: BIBLIOGRAPHY
    add_sec_heading("10. BIBLIOGRAPHY")
    add_subsec_heading("BOOK REFERENCES:")
    add_body_p("1. Alex Banks, Eve Porcello, Learning React: Modern Patterns for Developing React Apps, 2nd Edition, O’Reilly Media, 2020.\n2. David Choi, Full-Stack React Projects: Build real-world modern web apps with React, Node.js, Express, and MongoDB, Packt Publishing, 2nd Edition, 2020.")
    
    add_subsec_heading("WEBSITE REFERENCES:")
    add_body_p("• React Official Documentation: https://react.dev/learn\n• CodeIO YouTube Tutorials: http://www.youtube.com/@codeio\n• GeeksforGeeks MERN Stack Guide: https://www.geeksforgeeks.org/introduction-to-mern-stack\n• W3Schools React Tutorial: https://www.w3schools.com/react")

    output_path = "c:\\chit fund\\Smart_Campus_Connect_Project_Report.docx"
    doc.save(output_path)
    print(f"Report successfully saved to {output_path}")

if __name__ == "__main__":
    create_report()

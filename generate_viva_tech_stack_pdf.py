import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib import colors

pdf_path = r"c:\chit fund\SecureChit_Tech_Stack_Viva_Guide.pdf"

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=36,
    leftMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()

# Custom styles
primary_color = colors.HexColor("#1E3A8A")    # Deep Navy
secondary_color = colors.HexColor("#0D9488")  # Teal
dark_text = colors.HexColor("#1F2937")        # Charcoal
gray_bg = colors.HexColor("#F3F4F6")          # Light gray
card_bg = colors.HexColor("#F8FAFC")          # Slate 50
accent_blue = colors.HexColor("#2563EB")

title_style = ParagraphStyle(
    "DocTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=22,
    leading=26,
    textColor=primary_color,
    alignment=1
)

subtitle_style = ParagraphStyle(
    "DocSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=12,
    leading=16,
    textColor=secondary_color,
    alignment=1
)

h1_style = ParagraphStyle(
    "SectionH1",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=17,
    textColor=primary_color,
    spaceBefore=8,
    spaceAfter=4
)

body_style = ParagraphStyle(
    "BodyDark",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9.5,
    leading=13.5,
    textColor=dark_text
)

bullet_style = ParagraphStyle(
    "BulletText",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9.5,
    leading=13.5,
    textColor=dark_text,
    leftIndent=12
)

table_header = ParagraphStyle(
    "TableHeader",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9.5,
    leading=12,
    textColor=colors.white
)

table_body = ParagraphStyle(
    "TableBody",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=12,
    textColor=dark_text
)

story = []

# Title & Subtitle
story.append(Paragraph("SecureChit - Technology Stack & Viva Guide", title_style))
story.append(Spacer(1, 4))
story.append(Paragraph("Full Stack Architecture & Explanations in Thanglish", subtitle_style))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))

# 1. 30-Second Quick Pitch (Boxed)
pitch_heading = Paragraph("<b>⚡ 30-Second Quick Pitch (Viva Start-la Solla Vendiyathu):</b>", ParagraphStyle("PHead", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10, textColor=primary_color))
pitch_body = Paragraph(
    '<i>"Sir/Madam, namma project <b>Decoupled 4-Tier Architecture</b>-la develop pannirukkom.<br/>'
    '• <b>Frontend:</b> React 18 with Vite & Tailwind CSS (for modern & responsive UI)<br/>'
    '• <b>Backend:</b> Python FastAPI with Uvicorn (for high-speed async REST APIs)<br/>'
    '• <b>Database:</b> PostgreSQL / SQLite with SQLAlchemy ORM & Alembic migrations<br/>'
    '• <b>Security:</b> JWT stateless tokens + Bcrypt password encryption<br/>'
    '• <b>Services:</b> ReportLab PDF invoices, UPI QR generation & SMTP Email alerts."</i>',
    body_style
)

pitch_table = Table([[pitch_heading], [pitch_body]], colWidths=[540])
pitch_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
    ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#3B82F6")),
    ("PADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
]))
story.append(pitch_table)
story.append(Spacer(1, 8))

# 2. Frontend Tier
story.append(Paragraph("1. Frontend (Client Tier)", h1_style))
story.append(Paragraph("• <b>React 18:</b> Component-based SPA (Single Page Application). Reusable components & fast state updates with Virtual DOM.", bullet_style))
story.append(Paragraph("• <b>Vite 5 (Bundler):</b> Webpack / CRA vida romba fast-ah run aagum. Instant Hot Module Replacement (HMR) & lightning build time.", bullet_style))
story.append(Paragraph("• <b>Tailwind CSS:</b> Utility-first CSS framework. Consistent theme, zero CSS conflicts & fast responsive mobile design.", bullet_style))
story.append(Paragraph("• <b>React Router DOM v7:</b> Client-side routing. Admin routes & Member routes separate panni role-based security guard pannudhu.", bullet_style))
story.append(Paragraph("• <b>Axios:</b> Backend API kooda communicate panna. Request interceptor moolama JWT token auto-ah attach aagum.", bullet_style))
story.append(Paragraph("• <b>UI Libraries:</b> Lucide React (clean icons), React Hot Toast (instant toast alerts), React Custom Roulette & Canvas Confetti (auction draw animation).", bullet_style))
story.append(Spacer(1, 8))

# 3. Backend Tier
story.append(Paragraph("2. Backend (API & Business Logic Tier)", h1_style))
story.append(Paragraph("• <b>Python FastAPI:</b> High-performance asynchronous framework (<code>async/await</code>). Django/Flask vida romba lightweight & fast.", bullet_style))
story.append(Paragraph("• <b>Swagger Documentation:</b> Automatic interactive API documentation generate aagum (<code>/docs</code> URL moolama test pannalam).", bullet_style))
story.append(Paragraph("• <b>Uvicorn:</b> FastAPI-kku ASGI web server. High concurrent connections smooth-ah handle pannum.", bullet_style))
story.append(Paragraph("• <b>Pydantic v2:</b> Strict data validation. Request body inputs types & constraints auto-check panni invalid data thadukkum.", bullet_style))
story.append(Paragraph("• <b>Authentication (JWT):</b> <code>python-jose</code> use panni stateless authentication & Role-Based Access Control (RBAC: Admin vs Member).", bullet_style))
story.append(Paragraph("• <b>Password Security:</b> <code>passlib[bcrypt]</code> vachu plain text passwords salt panni hash aagi DB-la store aagum.", bullet_style))
story.append(Paragraph("• <b>SlowAPI:</b> Rate limiting implement panni brute-force attacks and DDOS traffic prevent pannum.", bullet_style))
story.append(Spacer(1, 8))

# 4. Database Tier
story.append(Paragraph("3. Database Tier (Persistence & Migrations)", h1_style))
story.append(Paragraph("• <b>PostgreSQL / SQLite:</b> Relational database (RDBMS). Chit plans, users, bids, payments ellam foreign keys and ACID compliance oda secure-ah save aagum.", bullet_style))
story.append(Paragraph("• <b>SQLAlchemy 2.0 (ORM):</b> Direct SQL queries ezhudha thevailla. Python classes/models moolama DB manage aagum. SQL Injection attacks 100% block pannum.", bullet_style))
story.append(Paragraph("• <b>Alembic:</b> Database schema version control. Table structure changes-ah structured-ah upgrade/downgrade panna mudiyum.", bullet_style))
story.append(Spacer(1, 8))

# 5. Extra Utilities & Services
story.append(Paragraph("4. External Services & Utilities", h1_style))
story.append(Paragraph("• <b>ReportLab:</b> Payment passbook, transaction receipts and statements dynamic PDF-ah generate panna.", bullet_style))
story.append(Paragraph("• <b>OpenPyXL:</b> Admin monthly audit & balance sheets Excel (.xlsx) file-ah export panna.", bullet_style))
story.append(Paragraph("• <b>qrcode + Pillow:</b> Dynamic UPI QR codes generate panna, so members easily scan panni pay pannalam.", bullet_style))
story.append(Paragraph("• <b>SMTP Email:</b> Due date reminders and payment confirmation mail automatic-ah notify aaga.", bullet_style))
story.append(Spacer(1, 8))

# 6. Important Viva Q&A Table
story.append(Paragraph("5. Top Viva Questions & Instant Answers", h1_style))

data = [
    [
        Paragraph("<b>Viva Question</b>", table_header),
        Paragraph("<b>How to Answer (Thanglish)</b>", table_header)
    ],
    [
        Paragraph("<b>Why FastAPI over Django / Flask?</b>", table_body),
        Paragraph("FastAPI async architecture (`asyncio`) moolama high concurrency support pannum. Built-in Pydantic data validation and auto Swagger `/docs` documentation iruku.", table_body)
    ],
    [
        Paragraph("<b>Why Vite instead of Create-React-App?</b>", table_body),
        Paragraph("CRA uses Webpack which bundles slow. Vite browser-oda native ES Modules (ESM) use pandrathala instant dev server launch and fast hot reloading kedaikkum.", table_body)
    ],
    [
        Paragraph("<b>How is authentication secured?</b>", table_body),
        Paragraph("Stateless JWT Tokens headers-la pass aagudhu. Passwords plain text-ah pogama cryptographic salt panni Bcrypt hashing vachu store pannirukkom.", table_body)
    ],
    [
        Paragraph("<b>How is Database integrity maintained?</b>", table_body),
        Paragraph("SQLAlchemy ORM + RDBMS foreign keys use pannirukkom. Transactions commit/rollback aaguradhala payment/auction calculations-la partial write aagathu.", table_body)
    ]
]

qa_table = Table(data, colWidths=[180, 360])
qa_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), primary_color),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F9FAFB")]),
    ("PADDING", (0, 0), (-1, -1), 5),
]))

story.append(qa_table)

# Build PDF
doc.build(story)
print("PDF created successfully at:", pdf_path)

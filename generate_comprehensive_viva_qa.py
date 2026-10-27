import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
from reportlab.lib import colors

pdf_path = r"c:\chit fund\SecureChit_Comprehensive_Viva_Questions.pdf"

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    rightMargin=36,
    leftMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()

primary_color = colors.HexColor("#1E3A8A")    # Deep Navy
secondary_color = colors.HexColor("#0D9488")  # Teal
dark_text = colors.HexColor("#1F2937")        # Charcoal
accent_blue = colors.HexColor("#2563EB")
accent_red = colors.HexColor("#DC2626")

title_style = ParagraphStyle(
    "DocTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=20,
    leading=24,
    textColor=primary_color,
    alignment=1
)

subtitle_style = ParagraphStyle(
    "DocSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=11,
    leading=15,
    textColor=secondary_color,
    alignment=1
)

h1_style = ParagraphStyle(
    "SectionH1",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=12,
    leading=16,
    textColor=primary_color,
    spaceBefore=8,
    spaceAfter=4
)

table_header = ParagraphStyle(
    "TableHeader",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9,
    leading=11,
    textColor=colors.white
)

q_style = ParagraphStyle(
    "QText",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=8.5,
    leading=11.5,
    textColor=colors.HexColor("#1E40AF")
)

ans_style = ParagraphStyle(
    "AnsText",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8.5,
    leading=11.5,
    textColor=dark_text
)

story = []

# Title
story.append(Paragraph("SecureChit - Comprehensive Viva Questions & Answers", title_style))
story.append(Spacer(1, 4))
story.append(Paragraph("All Anticipated Examiner Questions Across 6 Core Domains (in Thanglish)", subtitle_style))
story.append(Spacer(1, 6))
story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8))

def build_qa_table(qa_list, col_widths=[170, 370]):
    data = [[Paragraph("<b>Expected Question / Topic</b>", table_header), Paragraph("<b>Smart Answer (Thanglish & Technical)</b>", table_header)]]
    for q, a in qa_list:
        data.append([Paragraph(q, q_style), Paragraph(a, ans_style)])
    
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), primary_color),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("PADDING", (0, 0), (-1, -1), 4.5),
    ]))
    return t

# 1. Project Concept & Business Logic
story.append(Paragraph("Category 1: Chit Fund Business Logic & Domain Understanding", h1_style))
cat1_data = [
    (
        "<b>1. Chit Fund epdi work aagudhu? Explain your project flow.</b>",
        "Group of members oru fix period-ku monthly fixed amount (Installment) pay pannuvanga. Every month oru <b>Reverse Auction</b> nadakkum. Adhula highest discount bid panra member prize money edupparu. Remaining discount dividend-ah split aagi matha members dues-la deduct aagum."
    ),
    (
        "<b>2. Reverse Auction-na enna? Normal auction-kum idhukum enna difference?</b>",
        "Normal auction-la highest price solravanga win pannuvanga. Aana Chit Fund <b>Reverse Auction</b>: Chit pool amount-la irundhu lowest amount-ku yar eduka thayaara irukangalo (highest discount kudukravanga) avanga win pannuvanga. Eg: 1 Lakh chit-la 15,000 discount vitu 85,000 vangikravanga winner."
    ),
    (
        "<b>3. Dividend calculation epdi compute pannirukinga?</b>",
        "<b>Dividend = (Auction Discount Amount - Foreman/Admin Commission) / Total Members</b>. Winner vitra discount-la admin 5% commission eduthukitu, meedhi amount ellarukum equal-ah split aagum. Idhu adutha maasam installment-la discount-ah apply aagum."
    ),
    (
        "<b>4. Oru member prize amount eduthutu adutha maasam kattalana enna pannuvinga? (Defaulter Handling)</b>",
        "Prize money release panradhuku munnadi <b>Guarantors / Promissory Note</b> verify pannuvom. Kattala na: 1) System auto-ah penalty interest calculate pannum, 2) Daily due reminder emails send aagum, 3) Legal export statements generate panni legal action initiate pannalam."
    )
]
story.append(build_qa_table(cat1_data))
story.append(Spacer(1, 8))

# 2. Database & Data Integrity
story.append(Paragraph("Category 2: Database Architecture, ACID & Schema Design", h1_style))
cat2_data = [
    (
        "<b>5. Unga DB-la main tables enna ellam irukku? Relationships explain pannu.</b>",
        "Main tables: <code>Users</code>, <code>ChitPlans</code>, <code>PlanEnrollments</code>, <code>Auctions/Draws</code>, <code>Bids</code>, <code>Payments/Installments</code>, <code>AuditLogs</code>.<br/>One User can have Many Enrollments (1:N), One Plan has Many Auctions (1:N), One Auction has Many Bids (1:N)."
    ),
    (
        "<b>6. Concurrency issue epdi avoid panreenga? (Orey time-la 2 per bid panna?)</b>",
        "Database level-la <b>Pessimistic / Optimistic Locking</b> and <b>SQLAlchemy Database Transactions</b> use panrom. <code>db.commit()</code> and <code>db.rollback()</code> use panradhala, race condition aagathu. Higher bid/lower discount immediately validate aagi reject aagidum."
    ),
    (
        "<b>7. Why Relational DB (SQL) instead of NoSQL (MongoDB)?</b>",
        "Chit Fund oru pure financial domain. Inga strict <b>ACID Properties</b> (Atomicity, Consistency, Isolation, Durability) romba mukkiyam. Balance thappa compute aagakoodadhu, foreign key relationships & constraints SQL-la dhaan 100% reliable-ah maintain aagum."
    )
]
story.append(build_qa_table(cat2_data))
story.append(Spacer(1, 8))

# Page Break for Clean Layout
story.append(PageBreak())

# 3. Security & Authentication
story.append(Paragraph("Category 3: Security, Authentication & Role Access", h1_style))
cat3_data = [
    (
        "<b>8. JWT Token flow explain pannu. Token expiry enna aagum?</b>",
        "User login panna credentials verify aagi server oru signed <b>JWT (Header + Payload + Signature)</b> return pannum. Frontend adhaye <code>Authorization: Bearer &lt;token&gt;</code> header-la anuppum. Expiry time 30 mins. Token expire aana user redirect aagi marubadi login pannanum."
    ),
    (
        "<b>9. Admin endpoint-ah member call pannita enna aagum? (RBAC)</b>",
        "FastAPI-la <b>Dependency Injection</b> vachu <code>get_current_admin_user</code> validator function irukku. Token payload-la role check pannum: role <code>admin</code> illana HTTP <code>403 Forbidden</code> return pannum. So member admin API-ya access panna mudiyadhu."
    ),
    (
        "<b>10. SQL Injection and XSS epdi prevent panreenga?</b>",
        "• <b>SQL Injection:</b> SQLAlchemy parameterized queries use panradhala raw input direct-ah execute aagathu.<br/>• <b>XSS:</b> React automatically JSX-la render panra data-va escape pannidum. Malicious script run aagathu.<br/>• <b>Rate Limit:</b> SlowAPI vachu spamming prevent panrom."
    )
]
story.append(build_qa_table(cat3_data))
story.append(Spacer(1, 8))

# 4. Frontend & User Experience
story.append(Paragraph("Category 4: Frontend Development & State Management", h1_style))
cat4_data = [
    (
        "<b>11. React-la State management-ku enna use pannirukinga?</b>",
        "Component level-ku React <code>useState</code> and <code>useEffect</code> hooks. Global auth state-ku (logged-in user details, token) <b>React Context API</b> or <code>localStorage</code> token flow use pannirukkom."
    ),
    (
        "<b>12. Axios interceptors ethuku theva patruchhu?</b>",
        "Every single API call-kum manual-ah token ezhuthaama, Axios <b>Request Interceptor</b> automatically header-la token attach pannidum. Adhey pola <b>Response Interceptor</b> 401 Unauthorized vandha auto-logout trigger pannum."
    ),
    (
        "<b>13. Live auction draw animation epdi work aagudhu?</b>",
        "Backend random algorithm draw winner-ah select pannum. Frontend-la <code>React Custom Roulette</code> wheel spin aagi, winner reveal aana udaney <code>Canvas-Confetti</code> trigger aagi visual feedback tharum."
    )
]
story.append(build_qa_table(cat4_data))
story.append(Spacer(1, 8))

# 5. Testing, Real-world & Future Scope
story.append(Paragraph("Category 5: System Testing, Challenges & Future Enhancements", h1_style))
cat5_data = [
    (
        "<b>14. Project develop pannumbodhu ungalukku vandha biggest challenge enna?</b>",
        "Chit installment interest, dividend split, and reverse auction calculation sync panradhu dhaan biggest challenge. Oru member pay pannalana adutha auction pool and dividend affect aagum. Adha handle panna automated batch recalculation script build pannom."
    ),
    (
        "<b>15. Project-ah epdi test panneenga?</b>",
        "1) <b>Unit Testing:</b> <code>pytest</code> use panni core calculation functions test pannom.<br/>2) <b>Integration Testing:</b> Complete member payment to admin approval flow test panna scripts run pannom.<br/>3) <b>End-to-End:</b> <code>Puppeteer</code> use panni UI screenshots and automation test pannom."
    ),
    (
        "<b>16. Future Scope / Next versions-la enna add pannalam?</b>",
        "• Real payment gateway integration (Razorpay/Stripe live auto-debit).<br/>• WebSockets (Socket.IO) for real-time live bidding without page refresh.<br/>• Blockchain ledger for 100% transparent and tamper-proof chit fund audit."
    )
]
story.append(build_qa_table(cat5_data))

# Build Document
doc.build(story)
print("Comprehensive Viva Questions PDF successfully generated at:", pdf_path)

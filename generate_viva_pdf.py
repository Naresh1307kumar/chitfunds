import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages after page 1)
        if self._pageNumber > 1:
            self.drawString(40, 810, "SecureChit - Viva Voce Comprehensive Preparation Guide")
            self.drawRightString(555, 810, "B.Sc. Computer Science | 2026")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(40, 804, 555, 804)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(40, 42, 555, 42)
        self.drawString(40, 30, "Thiagarajar College (Autonomous), Madurai - Department of Computer Science")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 30, page_str)
        self.restoreState()


def build_pdf():
    pdf_filename = "SecureChit_Viva_Guide.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=48,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1A365D")   # Deep Navy
    secondary_color = colors.HexColor("#2B6CB0") # Slate Blue
    accent_dark = colors.HexColor("#2D3748")     # Charcoal
    box_bg = colors.HexColor("#F7FAFC")
    border_color = colors.HexColor("#CBD5E0")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        alignment=1, # Center
        spaceAfter=6
    )

    sub_title_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        alignment=1,
        spaceAfter=12
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#4A5568"),
        alignment=1
    )

    h1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=accent_dark,
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'CustomBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    q_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13.5,
        textColor=primary_color,
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    ans_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=accent_dark,
        spaceAfter=8
    )

    tanglish_bubble = ParagraphStyle(
        'TanglishText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#2C5282")
    )

    story = []

    # Logo & Header Banner
    logo_path = "thiagarajar_college_logo.png"
    if os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=54, height=54)
            img.hAlign = 'CENTER'
            story.append(img)
            story.append(Spacer(1, 4))
        except Exception:
            pass

    story.append(Paragraph("THIAGARAJAR COLLEGE (AUTONOMOUS), MADURAI - 625009", meta_style))
    story.append(Paragraph("Department of Computer Science | B.Sc. Computer Science (2026)", meta_style))
    story.append(Spacer(1, 6))
    story.append(Paragraph("SECURE CHIT: DIGITAL CHIT FUND MANAGEMENT SYSTEM", title_style))
    story.append(Paragraph("COMPREHENSIVE PROJECT VIVA-VOCE QUESTION & ANSWER GUIDE", sub_title_style))

    # Project Info Table
    info_data = [
        [
            Paragraph("<b>Students:</b> R. NARESHKUMAR (24UCS08)<br/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;APR. JEGATHEESH VARSHAN (24UCS06)", body_style),
            Paragraph("<b>Project Guide:</b> Mrs. SM. VALLI B.E., M.C.A., M.Phil<br/><b>HOD,</b> Dept. of Computer Science", body_style)
        ]
    ]
    info_table = Table(info_data, colWidths=[270, 245])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EDF2F7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 10))

    # --- SECTION 1: QUICK PROJECT SNAPSHOT & TECH STACK ---
    story.append(Paragraph("1. System Architecture & Tech Stack Summary", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    stack_data = [
        [Paragraph("<b>Component</b>", body_bold), Paragraph("<b>Technology Used</b>", body_bold), Paragraph("<b>Key Role in SecureChit</b>", body_bold)],
        [
            Paragraph("<b>Frontend UI</b>", body_style),
            Paragraph("React 18 + Tailwind CSS", body_style),
            Paragraph("Component-based reactive UI, real-time bid monitoring dashboards, responsive styling without CSS overhead.", body_style)
        ],
        [
            Paragraph("<b>Digital Signature</b>", body_style),
            Paragraph("HTML5 Canvas Pad", body_style),
            Paragraph("Interactive mouse/touchpad for drawing signatures onto legal Promissory Notes (PRN-YYYY-XXXX).", body_style)
        ],
        [
            Paragraph("<b>Backend API</b>", body_style),
            Paragraph("Python FastAPI", body_style),
            Paragraph("High-performance asynchronous REST endpoints, Swagger UI documentation, background task workers.", body_style)
        ],
        [
            Paragraph("<b>Winner Allocation</b>", body_style),
            Paragraph("AI Priority Evaluation Engine", body_style),
            Paragraph("Analyzes emergency score parameters to fairly prioritize winning bids rather than blindly lowest bids.", body_style)
        ],
        [
            Paragraph("<b>Database</b>", body_style),
            Paragraph("PostgreSQL", body_style),
            Paragraph("Strict ACID compliance, relational integrity, immutable financial ledgers and transaction audit trail.", body_style)
        ],
        [
            Paragraph("<b>Payment Gateway</b>", body_style),
            Paragraph("Razorpay API", body_style),
            Paragraph("Instant online monthly installment payments with automated digital receipt generation.", body_style)
        ],
        [
            Paragraph("<b>Notifications</b>", body_style),
            Paragraph("Fast2SMS & SMTP Email", body_style),
            Paragraph("Automated pre-due installment reminders and win announcements to guarantee zero default rates.", body_style)
        ],
        [
            Paragraph("<b>Security & Auth</b>", body_style),
            Paragraph("JWT + bcrypt + RBAC", body_style),
            Paragraph("Role-Based Access Control (Admin / Member), salted password hashing, stateless Bearer token authorization.", body_style)
        ]
    ]

    stack_table = Table(stack_data, colWidths=[100, 140, 275])
    stack_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(stack_table)
    story.append(Spacer(1, 10))

    # --- SECTION 2: VIVA-VOCE FORMAL QUESTIONS & ANSWERS ---
    story.append(Paragraph("2. Technical & Domain Viva-Voce Questions & Answers", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    qa_list = [
        (
            "Q1: What is the primary objective of your project 'SecureChit'?",
            "<b>Answer:</b> The primary objective of SecureChit is to digitize and automate traditional chit fund operations. It replaces manual ledgers, paper promissory notes, and informal bidding with a transparent, cloud-based platform featuring live priority-based bidding, instant digital receipts, legal promissory note e-signatures, and automated dividend distribution."
        ),
        (
            "Q2: How does a traditional Chit Fund operate, and how does SecureChit modernize it?",
            "<b>Answer:</b> In a traditional chit fund (ROSCA), all members contribute a fixed sum monthly to create a pool. In ordinary schemes, members bid down the pot (reverse auction). However, SecureChit replaces this with an <b>AI-powered priority-based bidding model</b> that evaluates urgent emergency priorities to award the fund ethically. It accurately computes the 5% foreman commission and distributes remaining dividend discounts among all non-winning members while keeping an immutable digital audit ledger."
        ),
        (
            "Q3: Why did your project use Priority-Based Bidding instead of a simple Reverse Auction?",
            "<b>Answer:</b> In traditional reverse auctions, speculative bidders or financially aggressive participants bid down excessively, depriving genuinely needy members who have real medical, educational, or business emergencies. SecureChit's Priority Bidding Engine evaluates verified priority scores and genuine emergency parameters so that chit allocations are equitable, fair, and transparent without bid manipulation or collusion."
        ),
        (
            "Q4: What are the primary functional modules implemented in SecureChit?",
            "<b>Answer:</b> The system consists of 7 tightly integrated modules:<br/>"
            "1. <b>Member Onboarding & KYC:</b> Digital member registration and verification.<br/>"
            "2. <b>Role-Based Access Control (RBAC):</b> Dedicated dashboards for Admin (Foreman) and Members.<br/>"
            "3. <b>Priority-Based Bidding Engine:</b> Bid submission and emergency assessment.<br/>"
            "4. <b>AI Smart Winner Allocation Engine:</b> Fair multi-factor evaluation of winner priorities.<br/>"
            "5. <b>Pronote Management (HTML5 Canvas):</b> Legal Promissory Note creation with touch signature capture.<br/>"
            "6. <b>Payment Gateway & Digital Receipts:</b> Razorpay integration for online installments.<br/>"
            "7. <b>Automated Communication Engine:</b> Fast2SMS & SMTP email reminders."
        ),
        (
            "Q5: Why did you choose Python over Java for the backend server?",
            "<b>Answer:</b> We selected Python over Java for three compelling engineering reasons:<br/>"
            "<b>1. Native AI/Algorithmic Ecosystem:</b> Python is the global standard for AI, priority weighting algorithms, and data analysis. Integrating our Smart Winner Allocation Engine directly within Python is seamless and lightweight.<br/>"
            "<b>2. Rapid Development & Minimal Boilerplate:</b> Java frameworks (like Spring Boot) require excessive boilerplate code (DTOs, DAOs, XML/annotations). Python's concise syntax drastically accelerated our sprint delivery.<br/>"
            "<b>3. High Asynchronous Concurrency with FastAPI:</b> Using Python's modern <code>async/await</code> paradigm via Starlette and Uvicorn, FastAPI provides microsecond throughput comparable to Node.js and Go, handling concurrent bidding without the heavy JVM memory overhead."
        ),
        (
            "Q6: Why did you choose FastAPI over other Python frameworks like Django or Flask?",
            "<b>Answer:</b> While Django is monolithic and Flask is synchronous by default, FastAPI was built from the ground up for modern asynchronous microservices. It features automatic schema validation using Pydantic, auto-generates interactive OpenAPI/Swagger documentation, and natively supports <code>async/await</code>, making it ideal for real-time bid processing."
        ),
        (
            "Q7: Why was PostgreSQL chosen over NoSQL databases like MongoDB?",
            "<b>Answer:</b> Chit funds are financial accounting systems where balances, ledger audits, and double-entry integrity are paramount. PostgreSQL guarantees strict <b>ACID (Atomicity, Consistency, Isolation, Durability)</b> properties and relational foreign key constraints. In contrast, document databases like MongoDB can lead to eventual consistency anomalies and ledger discrepancies during simultaneous bid/payment transactions."
        ),
        (
            "Q8: How does the Promissory Note (Pronote) digital signature feature work?",
            "<b>Answer:</b> Upon winner declaration, the system auto-generates a unique legal Promissory Note record (<code>PRN-YYYY-XXXX</code>) marked with status 'Pending Signature'. On the member dashboard, an interactive HTML5 Canvas element allows the winner to draw their touch or stylus signature. The signature vector is converted to Base64 image data, securely transmitted via authenticated API, stored in PostgreSQL, and stamped onto the formal digital document, making it visible to the Admin."
        ),
        (
            "Q9: How is online payment and installment tracking handled?",
            "<b>Answer:</b> We integrated the <b>Razorpay Payment Gateway API</b>. When a member clicks 'Pay Installment', Razorpay handles card/UPI/net-banking processing. Upon transaction completion, SecureChit verifies the payment signature webhook, updates the member ledger immediately, recalculates outstanding dues, and generates an instant printable digital payment receipt."
        ),
        (
            "Q10: How does SecureChit minimize payment defaults?",
            "<b>Answer:</b> SecureChit prevents defaults proactively using a multi-channel automated communication dispatcher. Integrated with <b>Fast2SMS</b> for transactional SMS and <b>SMTP (Nodemailer)</b> for email, the backend runs scheduled cron jobs sending automated reminder alerts 3 days and 1 day prior to due dates, as well as instant win declarations and receipts."
        ),
        (
            "Q11: Explain the security mechanisms implemented in the project.",
            "<b>Answer:</b> Security is enforced at every layer:<br/>"
            "&bull; <b>Password Hashing:</b> Uses <code>bcrypt</code> with random cryptographic salt.<br/>"
            "&bull; <b>Stateless Authentication:</b> Uses JWT (JSON Web Tokens) with HMAC-SHA256 signing and expiration timestamps.<br/>"
            "&bull; <b>Role-Based Access Control:</b> Backend middleware blocks unauthorized endpoints (e.g., members cannot access chit creation or approval routes).<br/>"
            "&bull; <b>Data Sanitization:</b> Pydantic schemas prevent SQL injection and cross-site scripting (XSS)."
        ),
        (
            "Q12: Can you describe the Data Flow (DFD Levels) of the system?",
            "<b>Answer:</b> At <b>Level 0 (Context Diagram)</b>, entities are Member, Admin, Razorpay, and SMS Gateway. Inputs include KYC, bids, and payments; outputs include digital receipts, winning alerts, and MIS reports. <b>Level 1</b> breaks down the application into User Auth, Chit Lifecycle Manager, Priority Bid Evaluator, Payment Processing, and Notification Engine. <b>Level 2 & 3</b> detail database reads/writes to tables like <code>users</code>, <code>chit_groups</code>, <code>bids</code>, <code>pronotes</code>, and <code>payments</code>."
        ),
        (
            "Q13: What was the most significant technical challenge during development?",
            "<b>Answer:</b> The biggest engineering hurdle was synchronizing the priority-based bidding evaluation in real time while maintaining transactional atomicity across database tables. Handling the HTML5 Canvas vector signature conversion, securely encrypting the Base64 payload, and locking the state so a member cannot re-sign or tamper with an issued promissory note was also a key challenge successfully solved."
        ),
        (
            "Q14: What future enhancements can be added to SecureChit?",
            "<b>Answer:</b> Future roadmaps include:<br/>"
            "1. Mobile App build using React Native for Android and iOS.<br/>"
            "2. Integration with Government DigiLocker and Aadhaar e-KYC APIs.<br/>"
            "3. Hyperledger / Ethereum smart contracts to achieve fully decentralized, tamper-proof chit ledgers."
        )
    ]

    for q, a in qa_list:
        card = [
            Paragraph(q, q_style),
            Paragraph(a, ans_style)
        ]
        story.append(KeepTogether(card))

    # --- SECTION 3: TANGLISH VIVA SPEAKING GUIDE ---
    story.append(PageBreak())
    story.append(Paragraph("3. Spoken Tanglish Viva Cheat Sheet (Examiner kitta epdi pesanum)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))
    story.append(Paragraph("Viva hall-la examiner kitta Tamil + English (Tanglish)-la explain panna idho standard speaking points:", meta_style))
    story.append(Spacer(1, 6))

    tanglish_qa = [
        (
            "1. Project Introduction (1-Minute Opening Pitch)",
            "\"Good morning Sir / Mam. Namma project title <b>'Secure Chit'</b>. "
            "Normal-a chit fund-la manual paperwork, ledger disputes, and bid collusion irukkum. "
            "Idha resolve panna nanga oru complete digital web platform develop pannirukom. "
            "Namma project-oda main highlight enna-na: <b>AI-based Priority Bidding</b>, "
            "HTML5 Canvas moolama <b>Promissory Note Digital Signature</b>, <b>Razorpay Online Payment</b>, "
            "and automated SMS/Email alerts to prevent payment defaults.\""
        ),
        (
            "2. Why Python over Java? (Crucial Viva Question)",
            "\"Sir, Python choose panna 3 main reasons irukku:<br/>"
            "<b>1. AI & Priority Logic:</b> Namma project-la AI priority allocation algorithm irukku. Python-la AI libraries integrate panradhu romba direct and easy, Java-la idhu romba complex.<br/>"
            "<b>2. Fast Development & Clean Code:</b> Java-la neraya boilerplate code (getters, setters, configs) ezhudhanum. Python syntax clean-a irundhadhala nanga core features-la focus panna mudinjadhu.<br/>"
            "<b>3. FastAPI Real-time Performance:</b> Nanga FastAPI use panrom. Idhula built-in <code>async/await</code> irukkaradhala live bidding-la concurrent requests-ah hang aagama high speed-la handle pannum. Java JVM memory-ah vida idhu lightweight.\""
        ),
        (
            "3. Priority Bidding vs Reverse Auction (Important Clarification)",
            "\"Sir, normal chit fund-la <b>Reverse Auction</b> nadakkum (yaaru kammiya bid pandrangalo avanga winner). "
            "Aana SecureChit-la nanga <b>Priority-Based Bidding</b> implement pannirukom. "
            "Because emergency thevai irukkura members (medical, education emergencies) pathu namma AI algorithm "
            "priority calculate panni fair-a allocate pannum. Idhanala bid collusion and unfair bidding thadukkappadudhu.\""
        ),
        (
            "4. Promissory Note & HTML5 Canvas Signature",
            "\"Chit win pannavangala Promissory Note sign panna solluvom. "
            "SecureChit-la win aana udane system automatic-a legal Promissory Note (PRN code) generate pannum. "
            "Winner avaroda phone or laptop screen-la <b>HTML5 Canvas</b> use panni digital sign poduvanga. "
            "Sign pannadhukku approm dhan admin portal-la amount release aagum. Paperwork complete-a zero aayirum.\""
        ),
        (
            "5. Database & Security (PostgreSQL, JWT, bcrypt)",
            "\"Money transactions irukkaradhala nanga <b>PostgreSQL</b> use pannirukom, because it strictly follows ACID properties. "
            "Passwords ellam <b>bcrypt</b> algorithm vachi hash panni store aagum. "
            "User session and login-ku <b>JWT tokens</b> use panrom, so safe and secure-a irukkum.\""
        )
    ]

    for title, content in tanglish_qa:
        card = [
            Paragraph(f"<b>{title}</b>", h2_style),
            Table(
                [[Paragraph(content, tanglish_bubble)]],
                colWidths=[515]
            )
        ]
        t_table = card[1]
        t_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BEE3F8")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(KeepTogether(card))
        story.append(Spacer(1, 6))

    # --- SECTION 4: RAPID FIRE & TRICKY EXAMINER QUESTIONS ---
    story.append(Spacer(1, 8))
    story.append(Paragraph("4. Examiner Tricky Questions & Smart Answers", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=8))

    tricky_qa = [
        (
            "Trap Q: What if two members have the exact same emergency priority score?",
            "<b>Smart Answer:</b> The AI engine evaluates secondary tie-breaking parameters: past prompt payment track record (credit reliability score), number of months already participated without claiming chit, and timestamp priority of the bid submission."
        ),
        (
            "Trap Q: If member loses internet connection during payment, will money be lost?",
            "<b>Smart Answer:</b> No. We use <b>Razorpay Webhooks</b>. Even if the member's browser crashes or internet disconnects, Razorpay's server sends an automated backend webhook confirmation to our FastAPI server, which verifies the cryptographic signature and safely updates the database ledger."
        ),
        (
            "Trap Q: Why not use MongoDB if JSON data is convenient?",
            "<b>Smart Answer:</b> Chit funds deal with financial ledger balances. MongoDB has eventual consistency and lacks strict multi-table relational schema constraints. In contrast, PostgreSQL ensures strict ACID transactions, ensuring debits and credits always match without data corruption."
        ),
        (
            "Trap Q: How is the 5% foreman commission handled mathematically?",
            "<b>Smart Answer:</b> Total Pool = (Monthly Installment &times; Total Months). Foreman Commission = 5% of Total Pool. Remaining pot minus discount is allocated to winner, and the discount balance is equally credited back to all participating members as dividend deductions in their next installment."
        )
    ]

    for q, a in tricky_qa:
        card = [
            Paragraph(f"<b>{q}</b>", q_style),
            Paragraph(a, ans_style)
        ]
        story.append(KeepTogether(card))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"SUCCESS: Generated {pdf_filename}")

if __name__ == "__main__":
    build_pdf()

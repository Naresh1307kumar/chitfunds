import shutil
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

src = r'C:\chit fund\SecureChit_Report_With_DFDs_v3.docx'
out = r'C:\chit fund\SecureChit_Report_With_DFDs_v4.docx'
doc = Document(src)

parent = doc.element.body
anchor = parent[-1]  # Insert at very end of document

def ins(elem):
    parent.append(elem)

def heading(text, size=13, bold=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    ins(p._element)
    return p

def subheading(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(11)
    ins(p._element)
    return p

def bullet(label, body):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    from docx.shared import Pt as _Pt
    p.paragraph_format.left_indent = __import__('docx').shared.Inches(0.25)
    r0 = p.add_run(u"\u2022  ")
    r0.font.size = Pt(11)
    if label:
        r1 = p.add_run(label + ": ")
        r1.bold = True
        r1.font.size = Pt(11)
    r2 = p.add_run(body)
    r2.bold = False
    r2.font.size = Pt(11)
    ins(p._element)

def blank():
    p = doc.add_paragraph()
    p.add_run("").font.size = Pt(6)
    ins(p._element)

# ─── 4.3 MODULE DESCRIPTION ───────────────────────────────────────────────────
blank()
heading("4.3 MODULE DESCRIPTION", size=13)
blank()

# ── Member Module ──────────────────────────────────────────────────────────────
subheading("Member Module")
blank()

bullet("Account Registration & KYC",
       "Self-service registration with username, email, phone, Aadhaar and PAN number. "
       "Member uploads KYC documents (Aadhaar front/back, PAN card, passport photo, address proof) "
       "for admin verification before account activation.")

bullet("Chit Plan Discovery",
       "Browse available Bronze, Silver and Gold tier chit plans filtered by monthly installment amount, "
       "total pool value, duration and current vacancy. Members can view full plan details and "
       "net prize amount before enrolling.")

bullet("Plan Enrollment",
       "One-click enrollment into an active chit plan. System auto-assigns a unique ticket number "
       "(TCK-YYYY-N) and records the joining date. A member cannot enroll in the same plan twice "
       "(unique constraint on user_id and plan_id).")

bullet("Monthly Installment Payment",
       "View monthly due statements showing base amount, penalty (if overdue) and total payable after "
       "dividend deduction. Settle dues via UPI / QR code scan (GPay, PhonePe) by submitting a "
       "12-digit UTR reference number, or via bank transfer / cash.")

bullet("Auction Bidding",
       "Participate in the monthly reverse-auction draw. Submit a bid discount amount along with a "
       "1-to-5 emergency priority rank (1 = Medical Emergency, 2 = Education, 3 = Marriage, "
       "4 = Business, 5 = Personal Savings) to compete for the monthly prize pool.")

bullet("Promissory Note Execution",
       "Upon winning the auction draw, the member receives an auto-generated Promissory Note "
       "(PRN-2026-XXXX). The member digitally signs the pronote using the HTML5 Canvas signature pad. "
       "The signed agreement is compiled as a downloadable PDF and stored securely.")

bullet("Receipt & Certificate Download",
       "Download tamper-proof PDF payment receipts (REC-2026-XXXX) for every verified installment "
       "and a scheme completion certificate upon chit maturity.")

bullet("Notification Centre",
       "Receive real-time in-app notifications for auction results, installment due reminders, "
       "payment verification updates, and KYC status changes (success / warning / alert / info).")

blank()

# ── Admin / Foreman Module ─────────────────────────────────────────────────────
subheading("Admin / Foreman Module")
blank()

bullet("Secure Administrative Login",
       "Separate role-based authentication for administrators. JWT Bearer tokens with RBAC middleware "
       "restrict all admin-only endpoints. Failed login attempts are tracked and accounts are locked "
       "after repeated failures.")

bullet("Member KYC Verification",
       "Review the uploaded KYC documents (Aadhaar, PAN, address proof, passport photo) for each "
       "member. Approve the member to activate their account or reject with a recorded rejection reason. "
       "KYC status updates trigger instant member notifications.")

bullet("Chit Plan Management",
       "Create, configure and activate chit plans by setting plan name, tier (Bronze / Silver / Gold), "
       "monthly installment amount, total members, duration, commission rate and start date. "
       "The system auto-calculates total pool value and net prize amount.")

bullet("Monthly Auction Conduct",
       "Open the monthly bidding session, monitor live bids, and trigger the AI Emergency Priority "
       "Engine (Rank 1–5) to determine the draw winner. Finalise the auction winner, record the "
       "winning bid, and auto-trigger dividend distribution across all active members.")

bullet("Dividend & Commission Calculation",
       "System enforces the statutory 5% foreman commission cap on each auction discount. "
       "Net discount is distributed equally among all plan members, automatically reducing "
       "their next monthly installment (net_payable = monthly_amount - dividend_per_member).")

bullet("Installment Verification",
       "Review submitted UTR references against payment records. Verify or reject installment "
       "payments. Verified installments trigger PDF receipt generation (REC-2026-XXXX) and "
       "update the member's payment ledger.")

bullet("Guarantor & Pronote Oversight",
       "View guarantor details submitted by members. Monitor all active Promissory Notes "
       "(PRN-2026-XXXX), track their status (pending_signature / active / paid / overdue) "
       "and send overdue alerts.")

bullet("Report Generation",
       "Generate downloadable reports in PDF, CSV or Excel format covering member roster, "
       "KYC status, installment ledger, overdue accounts, auction history, revenue summary "
       "and full audit log.")

bullet("System Settings",
       "Configure platform-wide parameters such as commission rate, penalty percentages "
       "and notification templates through the system_settings key-value store.")

blank()

# ── System / Backend Module ────────────────────────────────────────────────────
subheading("System / Backend Module")
blank()

bullet("Authentication & Security Engine",
       "FastAPI JWT Bearer token issuance and verification using python-jose. BCrypt password "
       "hashing via Passlib with unique cryptographic salts. SlowAPI rate-limiting middleware "
       "prevents brute-force attacks. All sensitive endpoints require valid role-scoped JWT.")

bullet("AI Emergency Priority Engine",
       "Automated bidding tie-breaker that ranks competing bids by declared emergency category: "
       "Rank 1 (Hospital / Medical) > Rank 2 (Higher Education) > Rank 3 (Marriage / Family) > "
       "Rank 4 (Business Capital) > Rank 5 (Personal Savings / Investment). Stored in plan_members.priority_score.")

bullet("UPI / QR Payment Engine",
       "Dynamically generates UPI QR codes using the Python qrcode library for GPay and PhonePe "
       "integration. Validates submitted transaction references against the pattern ^[0-9]{12}$ "
       "— invalid UTR format returns HTTP 400 Bad Request.")

bullet("PDF Generation Engine",
       "ReportLab 5.0.0 compiles legally structured Promissory Note PDFs (PRN-2026-XXXX) embedding "
       "the member's Base64-encoded Canvas digital signature. Pillow 12.2.0 generates tamper-proof "
       "PDF installment receipts (REC-2026-XXXX) with QR verification codes.")

bullet("Email Notification Relay",
       "Python smtplib via Google SMTP TLS (Port 587) dispatches automated transactional emails for "
       "auction winner announcements, installment due reminders, KYC approval / rejection alerts "
       "and account activation confirmations.")

bullet("Audit Log Engine",
       "Immutable audit_logs table records every critical platform action — LOGIN, KYC_VERIFIED, "
       "PAYMENT_VERIFIED, AUCTION_CONDUCTED, PRONOTE_SIGNED — with user ID, entity reference, "
       "IP address and timestamp for full regulatory compliance.")

blank()

# ── Workflow Rules ─────────────────────────────────────────────────────────────
subheading("Workflow Rules")
blank()

bullet("UTR Validation",
       "Every UPI transaction reference must match the pattern ^[0-9]{12}$ (exactly 12 numeric digits). "
       "Non-conforming references are rejected with HTTP 400 Bad Request before any database write.")

bullet("Installment Total Calculation",
       "Total Payable = Base Installment Amount + Penalty Amount. "
       "Net Payable (post-dividend) = Total Payable - Dividend Per Member.")

bullet("Auction Settlement Formula",
       "Discount = Chit Value - Winning Bid Amount. "
       "Company Commission = Discount x 0.05 (5%). "
       "Net Discount = Discount - Commission. "
       "Dividend Per Member = Net Discount / Total Members.")

bullet("Promissory Note Workflow",
       "Auto-generated on auction winner selection (status: pending_signature). "
       "Activated only after member submits a valid Base64 Canvas digital signature (status: active). "
       "Marked paid upon full repayment settlement.")

blank()

# ── Save ───────────────────────────────────────────────────────────────────────
doc.save(out)
print(f"Saved: {out}")

shutil.copy(out, r'C:\Users\nares\.gemini\antigravity\brain\f74afe5d-2f73-4013-bc1e-3562e05df0f5\SecureChit_Report_With_DFDs.docx')
print("Copied to artifact dir!")

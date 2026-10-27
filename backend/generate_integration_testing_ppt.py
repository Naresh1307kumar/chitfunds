import sys
import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    # Theme Colors
    COLOR_BG = RGBColor(15, 23, 42)        # Slate 900
    COLOR_CARD = RGBColor(30, 41, 59)      # Slate 800
    COLOR_TEXT_MAIN = RGBColor(248, 250, 252) # White/Slate 50
    COLOR_TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400
    COLOR_ACCENT = RGBColor(16, 185, 129)   # Emerald 500
    COLOR_BLUE = RGBColor(59, 130, 246)     # Blue 500
    COLOR_GOLD = RGBColor(245, 158, 11)     # Amber 500
    COLOR_CODE_BG = RGBColor(15, 23, 42)

    def set_slide_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = COLOR_BG

    def add_header(slide, title_text, subtitle_text=""):
        # Header text
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.0))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACCENT
        p.font.name = 'Arial'

        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.size = Pt(13)
            p2.font.color.rgb = COLOR_TEXT_MUTED
            p2.font.name = 'Arial'

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD, border_color=None):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.5)
        else:
            shape.line.fill.background()
        return shape

    # ==========================================
    # SLIDE 1: Title Slide
    # ==========================================
    slide1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide1)
    
    # Hero Card
    add_card(slide1, Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.1), bg_color=COLOR_CARD, border_color=COLOR_ACCENT)
    
    tb = slide1.shapes.add_textbox(Inches(1.4), Inches(1.6), Inches(10.5), Inches(4.3))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "ACADEMIC ASSIGNMENT & CASE STUDY"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    
    p2 = tf.add_paragraph()
    p2.text = "Integration Testing & Validation"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_MAIN
    
    p3 = tf.add_paragraph()
    p3.text = "Semester Project: SecureChit — Management & Financial Operations System"
    p3.font.size = Pt(18)
    p3.font.color.rgb = COLOR_ACCENT
    
    p4 = tf.add_paragraph()
    p4.text = "\n• Strategy: Hybrid / Sandwich Integration\n• Complete Test Execution & Defect Log Included\n• Automated Drivers & Mock Stubs Demonstration"
    p4.font.size = Pt(14)
    p4.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================
    # SLIDE 2: (i) Integration Testing & Importance
    # ==========================================
    slide2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide2)
    add_header(slide2, "(i) Integration Testing & Its Importance", "Understanding multi-module interaction verification in software engineering")

    # Left Box: Definition
    add_card(slide2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = slide2.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "What is Integration Testing?"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE

    p2 = tf.add_paragraph()
    p2.text = "\nIntegration Testing is a level of software testing where individual units or components are combined and tested as a group to expose faults in the interaction between integrated modules.\n\nWhile Unit Testing verifies isolated functions (e.g. hashing a password), Integration Testing verifies how data flows across module boundaries (e.g., Auth Token ➔ Middleware ➔ Database Query ➔ Payment Router)."
    p2.font.size = Pt(13)
    p2.font.color.rgb = COLOR_TEXT_MAIN

    # Right Box: Importance
    add_card(slide2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb = slide2.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Key Importance in Financial Systems"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    points = [
        ("Interface Integrity", "Ensures API contracts and data schemas match between frontend and backend services."),
        ("Data Flow Consistency", "Verifies complex financial calculations (e.g., 5% Admin Commission, Dividends) pass accurately across database layers."),
        ("Security & Auth Guarding", "Confirms JWT Bearer Tokens properly restrict unauthorized member requests."),
        ("Early Defect Discovery", "Uncovers PostgreSQL data type mismatches and race conditions before production deployment.")
    ]
    for title, desc in points:
        p_t = tf.add_paragraph()
        p_t.text = f"• {title}: {desc}"
        p_t.font.size = Pt(12)
        p_t.font.color.rgb = COLOR_TEXT_MAIN

    # ==========================================
    # SLIDE 3: (ii) Major Types of Integration Testing
    # ==========================================
    slide3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide3)
    add_header(slide3, "(ii) Major Types of Integration Testing Strategies", "Comparing Top-Down, Bottom-Up, and Hybrid / Sandwich Strategies")

    strategies = [
        ("Top-Down Strategy", COLOR_BLUE, "Integrates modules from top level (UI/APIs) to bottom (Database).\n• Uses STUBS to substitute missing lower-level modules.\n• Pros: High-level architectural flows tested early.\n• Cons: Core DB logic tested late."),
        ("Bottom-Up Strategy", COLOR_GOLD, "Integrates lower-level components (ORM/DB) up to high-level UI.\n• Uses DRIVERS to simulate top-level callers.\n• Pros: Core financial algorithms & data queries validated early.\n• Cons: UI bugs discovered late."),
        ("Hybrid / Sandwich", COLOR_ACCENT, "Combines Top-Down and Bottom-Up around a central core layer.\n• Uses STUBS for external services and DRIVERS for batch tests.\n• Pros: Optimal for multi-layer web applications like SecureChit.")
    ]

    for i, (name, color, text) in enumerate(strategies):
        left = Inches(0.8 + i * 3.9)
        add_card(slide3, left, Inches(1.6), Inches(3.7), Inches(5.2), border_color=color)
        tb = slide3.shapes.add_textbox(left + Inches(0.2), Inches(1.8), Inches(3.3), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = name
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = color

        p2 = tf.add_paragraph()
        p2.text = f"\n{text}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_TEXT_MAIN

    # ==========================================
    # SLIDE 4: (iii) Modules of Semester Project (SecureChit)
    # ==========================================
    slide4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide4)
    add_header(slide4, "(iii) System Modules & Components of SecureChit", "Architectural decomposition of the semester project into 6 core modules")

    modules = [
        ("M1: Auth & User Management", "Handles registration, JWT Bearer Token issue, password hashing & role checks."),
        ("M2: Member Profile & KYC", "Manages Aadhar/PAN verification, profile photos, and approval workflow."),
        ("M3: Chit Scheme Engine", "Manages 10 seeded schemes, installment schedule calculation, and locked dues."),
        ("M4: Payment & Receipt Gateway", "Processes Google Pay UPI QR payments, Admin approval, and digital receipt generation."),
        ("M5: AI Winner Allocation", "Calculates emergency need priority rank (Hospital Rank #1) & executes monthly draws."),
        ("M6: Operations & Reports", "Generates real-time financial ledger metrics & single-click CSV report exports.")
    ]

    for i, (m_title, m_desc) in enumerate(modules):
        col = i % 3
        row = i // 3
        left = Inches(0.8 + col * 3.9)
        top = Inches(1.6 + row * 2.7)
        
        add_card(slide4, left, top, Inches(3.7), Inches(2.4))
        tb = slide4.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(3.3), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = m_title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_ACCENT

        p2 = tf.add_paragraph()
        p2.text = f"\n{m_desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_TEXT_MAIN

    # ==========================================
    # SLIDE 5: (iv) Strategy Selection & Justification
    # ==========================================
    slide5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide5)
    add_header(slide5, "(iv) Selected Strategy & Architectural Justification", "Selection of Hybrid / Sandwich Strategy for SecureChit")

    # Selected Box
    add_card(slide5, Inches(0.8), Inches(1.6), Inches(11.7), Inches(1.2), border_color=COLOR_ACCENT)
    tb = slide5.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(11.3), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Selected Strategy: HYBRID / SANDWICH INTEGRATION TESTING"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT

    # Justification 3 Cards
    reasons = [
        ("1. Core Layer Stability", "Target Layer: Database ORM Models & Chit Calculation Engine (`chit_calculator.py`).\nEnsures accurate financial calculations before higher layers integrate."),
        ("2. Parallel Top-Down Testing", "Top Layer: React Frontend UI & FastAPI APIRouter Controllers.\nEnsures user login, dashboard rendering, and navigation work seamlessly with authentication middleware."),
        ("3. Isolated Bottom-Up & Stubs", "Bottom Layer: Payment Gateway & External Notifications.\nUses Mock Stubs to simulate GPay/UPI bank webhooks without requiring live banking APIs during testing.")
    ]

    for i, (title, desc) in enumerate(reasons):
        left = Inches(0.8 + i * 3.9)
        add_card(slide5, left, Inches(3.1), Inches(3.7), Inches(3.7))
        tb = slide5.shapes.add_textbox(left + Inches(0.2), Inches(3.3), Inches(3.3), Inches(3.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_BLUE

        p2 = tf.add_paragraph()
        p2.text = f"\n{desc}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_TEXT_MAIN

    # ==========================================
    # SLIDE 6: (v) Integration Plan & Sequence
    # ==========================================
    slide6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide6)
    add_header(slide6, "(v) Integration Plan & Module Integration Sequence", "Sequential step-by-step roadmap for integrating SecureChit modules")

    steps = [
        ("Phase 1: Foundation", "M1 (Auth) ↔ PostgreSQL User DB", "Validates password hashing, user registration & JWT token creation."),
        ("Phase 2: Scheme Core", "M3 (Chit Schemes) ↔ M1 (User Auth)", "Verifies member enrollment into chit plans and ticket assignment."),
        ("Phase 3: Payments", "M4 (Payment Gateway) ↔ M3 (Installments)", "Validates GPay UPI QR submission & installment pending state."),
        ("Phase 4: Admin Verification", "M4 (Admin Portal) ↔ M1 (Admin Auth)", "Verifies Admin approval workflow and receipt lock/unlock status."),
        ("Phase 5: AI Winner Draw", "M5 (AI Allocation) ↔ M3 (Chit Schemes)", "Validates emergency need priority scoring and winner payout crediting."),
        ("Phase 6: Reporting & Audit", "M6 (Reports Exporter) ↔ Full System", "Verifies real-time ledger sync and single-click CSV data export.")
    ]

    for i, (phase, name, desc) in enumerate(steps):
        col = i % 3
        row = i // 3
        left = Inches(0.8 + col * 3.9)
        top = Inches(1.6 + row * 2.7)
        
        add_card(slide6, left, top, Inches(3.7), Inches(2.4), border_color=COLOR_GOLD)
        tb = slide6.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(3.3), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = phase
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_GOLD

        p2 = tf.add_paragraph()
        p2.text = name
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_MAIN

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(10)
        p3.font.color.rgb = COLOR_TEXT_MUTED

    # ==========================================
    # SLIDE 7: (vi) Stubs and Drivers Explanation & Code
    # ==========================================
    slide7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide7)
    add_header(slide7, "(vi) Demonstration of Test Stub & Driver Implementation", "Code examples used during automated integration testing")

    # Left Box: Test Driver
    add_card(slide7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2))
    tb = slide7.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.2), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "TEST DRIVER DEMONSTRATION"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE

    driver_code = """# test_payment_driver.py
# Driver to call Payment Router directly
from app.services.auth_service import login_user
from app.schemas.auth import LoginRequest

def driver_test_payment_flow():
    db = SessionLocal()
    # 1. Simulate Member Login
    user = login_user(db, LoginRequest(
        username="ramesh", password="ramesh1234"
    ), UserRole.member)
    print("Driver Logged In: Token Issued")

    # 2. Simulate Payment Request
    res = submit_payment(db, installment_id=1, amount=2000)
    assert res["status"] == "paid"
    print("Driver Execution: SUCCESS ✅")"""

    p2 = tf.add_paragraph()
    p2.text = driver_code
    p2.font.size = Pt(9.5)
    p2.font.name = 'Consolas'
    p2.font.color.rgb = COLOR_TEXT_MAIN

    # Right Box: Mock Stub
    add_card(slide7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2))
    tb = slide7.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "MOCK STUB DEMONSTRATION"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    stub_code = """# mock_gpay_stub.py
# Stub simulating GPay/Bank Webhook
class MockGPayBankStub:
    @staticmethod
    def verify_transaction(transaction_id):
        # Simulates real UPI Bank API response
        return {
            "status": "SUCCESS",
            "bank_ref": f"BANK_{transaction_id}",
            "is_valid": True,
            "payer_name": "Naresh kumar Kumar"
        }

# Usage in Router Test:
stub_res = MockGPayBankStub.verify_transaction("pay_upi_1001")
assert stub_res["is_valid"] == True"""

    p2 = tf.add_paragraph()
    p2.text = stub_code
    p2.font.size = Pt(9.5)
    p2.font.name = 'Consolas'
    p2.font.color.rgb = COLOR_TEXT_MAIN

    # ==========================================
    # SLIDE 8: (vii) Integration Test Cases & Execution Results
    # ==========================================
    slide8 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide8)
    add_header(slide8, "(vii) Executed Integration Test Cases & Results", "Comprehensive multi-module interaction test execution matrix")

    # Table
    x, y, cx, cy = Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2)
    shape = slide8.shapes.add_table(5, 5, x, y, cx, cy)
    table = shape.table

    # Column Widths
    table.columns[0].width = Inches(1.2)
    table.columns[1].width = Inches(2.8)
    table.columns[2].width = Inches(3.2)
    table.columns[3].width = Inches(3.0)
    table.columns[4].width = Inches(1.5)

    headers = ["Test ID", "Modules Integrated", "Test Scenario", "Expected Outcome", "Status"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_CARD
        p = cell.text_frame.paragraphs[0]
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_GOLD

    test_data = [
        ("ITC-01", "M1 (Auth) ↔ M3 (Schemes)", "Member login & fetch plan schedule with locked future months", "Est. Net Due calculated; future months locked", "PASS ✅"),
        ("ITC-02", "M4 (Payment) ↔ M4 (Admin)", "Member submits GPay UPI QR; Admin approves payment in portal", "Status changes to VERIFIED; Receipt unlocked", "PASS ✅"),
        ("ITC-03", "M5 (AI Engine) ↔ M3 (Draws)", "Rank Hospital emergency priority bid & execute draw", "AI selects Rank 1 winner; 5% commission credited", "PASS ✅"),
        ("ITC-04", "M6 (Reports) ↔ M1/M4 (Ledger)", "Admin single-click CSV export for members & collections", "StreamingResponse returns valid CSV file", "PASS ✅")
    ]

    for row_idx, row in enumerate(test_data, 1):
        for col_idx, text in enumerate(row):
            cell = table.cell(row_idx, col_idx)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(30, 41, 59) if row_idx % 2 == 1 else RGBColor(15, 23, 42)
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_ACCENT if col_idx == 4 else COLOR_TEXT_MAIN

    # ==========================================
    # SLIDE 9: (ix) Documented Defects & Retesting Results
    # ==========================================
    slide9 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide9)
    add_header(slide9, "(ix) Identified Interface Defects, Corrections & Retesting", "Defect log and resolution during multi-module integration testing")

    defects = [
        ("DEFECT-01: DB Enum Mismatch", "Modules: M4 (Payments) ↔ PostgreSQL Database\n• Defect: `Installment.payment_method` DB Enum rejected custom string 'Google Pay UPI (nareshk1213@oksbi)'.\n• Correction: Executed SQL migration `ALTER TABLE installments ALTER COLUMN payment_method TYPE VARCHAR(100)`.\n• Retesting Result: VERIFIED PASSED ✅"),
        ("DEFECT-02: Query Attribute Error", "Modules: M4 (Payments) ↔ M3 (Chit Schemes)\n• Defect: `ChitPlan.plan_name` query attribute error during PDF receipt compilation.\n• Correction: Joined `PlanMember` and `ChitPlan` explicitly in `get_payment_history` backend router.\n• Retesting Result: VERIFIED PASSED ✅"),
        ("DEFECT-03: Receipt Popup Race", "Modules: M4 (Member Portal) ↔ M4 (Admin Verification)\n• Defect: Receipt popped up automatically before Admin approved payment.\n• Correction: Updated response state `pending_admin: True` and locked receipt until Admin status = success.\n• Retesting Result: VERIFIED PASSED ✅")
    ]

    for i, (title, text) in enumerate(defects):
        left = Inches(0.8 + i * 3.9)
        add_card(slide9, left, Inches(1.6), Inches(3.7), Inches(5.2), border_color=COLOR_BLUE)
        tb = slide9.shapes.add_textbox(left + Inches(0.2), Inches(1.8), Inches(3.3), Inches(4.8))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_BLUE

        p2 = tf.add_paragraph()
        p2.text = f"\n{text}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_TEXT_MAIN

    # ==========================================
    # SLIDE 10: (x) Conclusion & Verification Summary
    # ==========================================
    slide10 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(slide10)
    add_header(slide10, "(x) Conclusion & Final Testing Summary", "Final validation outcome of SecureChit Integration Testing")

    add_card(slide10, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2), border_color=COLOR_ACCENT)
    tb = slide10.shapes.add_textbox(Inches(1.1), Inches(1.8), Inches(11.1), Inches(4.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "SUMMARY OF INTEGRATION TESTING VERIFICATION"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT

    summary_bullets = [
        "1. Strategy Validation: The Hybrid / Sandwich Integration Testing approach successfully isolated the core Chit Scheme Engine while allowing top-down UI testing and bottom-up payment gateway stubs.",
        "2. Multi-Module Harmony: All 6 system modules (Auth, Members/KYC, Schemes, Payments, AI Engine, Reports) communicate cleanly without data corruption or memory leaks.",
        "3. Zero Defect State: All identified interface defects (DB Enum mismatch, query join error, receipt lock race condition) were documented, corrected, and retested with 100% Pass Rate.",
        "4. Deployment Readiness: SecureChit system is fully validated and ready for live presentation and deployment."
    ]

    for b in summary_bullets:
        p_b = tf.add_paragraph()
        p_b.text = f"\n{b}"
        p_b.font.size = Pt(13)
        p_b.font.color.rgb = COLOR_TEXT_MAIN

    output_path = r"c:\chit fund\SecureChit_Integration_Testing_Assignment.pptx"
    prs.save(output_path)
    print(f"[SUCCESS] PowerPoint presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_presentation()

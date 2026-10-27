import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_visual_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    NAVY = RGBColor(26, 43, 73)         # #1A2B49 (Header / Primary)
    GOLD = RGBColor(217, 119, 6)        # Amber-600
    SLATE_DARK = RGBColor(15, 23, 42)   # Slate-900
    LIGHT_BLUE = RGBColor(239, 246, 255)# Blue-50
    BORDER_BLUE = RGBColor(147, 197, 253)# Blue-300
    WHITE = RGBColor(255, 255, 255)
    GREEN = RGBColor(16, 185, 129)      # Emerald-500
    PURPLE = RGBColor(139, 92, 246)     # Purple-500
    AMBER_BG = RGBColor(254, 243, 199)  # Amber-100

    def add_header(slide, title_text, category_text="SECURECHIT SYSTEM ARCHITECTURE"):
        tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.3), Inches(12.1), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = category_text.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = GOLD
        
        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

    def add_box(slide, left, top, width, height, title, subtitle="", bg_color=LIGHT_BLUE, border_color=BORDER_BLUE, text_color=NAVY, is_oval=False):
        shape_type = MSO_SHAPE.OVAL if is_oval else MSO_SHAPE.ROUNDED_RECTANGLE
        shape = slide.shapes.add_shape(shape_type, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)

        tf = shape.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.CENTER
        p0.text = title
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = text_color

        if subtitle:
            p1 = tf.add_paragraph()
            p1.alignment = PP_ALIGN.CENTER
            p1.text = subtitle
            p1.font.size = Pt(9)
            p1.font.color.rgb = SLATE_DARK
        return shape

    # SLIDE 1: Title Slide
    s1 = prs.slides.add_slide(blank_layout)
    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(2.0), Inches(11.7), Inches(3.5))
    tf1 = tb1.text_frame
    p0 = tf1.paragraphs[0]
    p0.text = "SECURE CHIT FUND MANAGEMENT SYSTEM"
    p0.font.size = Pt(34)
    p0.font.bold = True
    p0.font.color.rgb = NAVY

    p1 = tf1.add_paragraph()
    p1.text = "Complete Visual Diagrams Deck (ER, DFD Level 0/1, Use Case & Database Schemas)"
    p1.font.size = Pt(18)
    p1.font.color.rgb = GOLD

    p2 = tf1.add_paragraph()
    p2.text = "\nTechnology Stack: FastAPI (Python) | React.js (Vite) | PostgreSQL | TailwindCSS | Mermaid"
    p2.font.size = Pt(13)
    p2.font.color.rgb = SLATE_DARK

    # SLIDE 2: Database Table Schemas (Visual Grid Cards)
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Relational Database Table Schemas", "DATA STRUCTURE")

    tables = [
        ("USERS", "id (PK), username, email, password_hash, role, status, kyc_status", RGBColor(239, 246, 255), RGBColor(59, 130, 246)),
        ("CHIT_PLANS", "id (PK), plan_name, monthly_amount, total_members, chit_value, commission_rate", RGBColor(254, 243, 199), RGBColor(245, 158, 11)),
        ("PLAN_MEMBERS", "id (PK), user_id (FK), plan_id (FK), ticket_number, has_won, reason, priority_score", RGBColor(236, 253, 245), RGBColor(16, 185, 129)),
        ("MONTHLY_DRAWS", "id (PK), plan_id (FK), winning_bid_amount, discount, company_commission, dividend_per_member, net_payable, prize_amount", RGBColor(243, 232, 255), RGBColor(139, 92, 246)),
        ("INSTALLMENTS", "id (PK), plan_member_id (FK), plan_id (FK), month_number, base_amount, total_amount, status", RGBColor(254, 242, 242), RGBColor(239, 68, 68)),
        ("PAYMENTS", "id (PK), installment_id (FK), user_id (FK), amount, payment_method, transaction_id, status", RGBColor(240, 253, 250), RGBColor(20, 184, 166))
    ]

    for idx, (t_name, t_cols, bg, brd) in enumerate(tables):
        row = idx // 3
        col = idx % 3
        l = Inches(0.8 + col * 3.9)
        t = Inches(1.4 + row * 2.8)
        add_box(s2, l, t, Inches(3.7), Inches(2.5), t_name, t_cols, bg_color=bg, border_color=brd)

    # SLIDE 3: Visual Entity-Relationship (ER) Diagram
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Entity-Relationship (ER) Diagram", "VISUAL DATA CARRIER")

    # Draw ER Nodes
    node_users = add_box(s3, Inches(0.8), Inches(1.6), Inches(2.6), Inches(1.8), "👤 USERS", "PK: id\nFK: role, kyc_status", LIGHT_BLUE, BORDER_BLUE)
    node_plans = add_box(s3, Inches(4.8), Inches(1.6), Inches(2.6), Inches(1.8), "🏢 CHIT_PLANS", "PK: id\nFields: chit_value, comm_rate", AMBER_BG, GOLD)
    node_draws = add_box(s3, Inches(9.2), Inches(1.6), Inches(2.6), Inches(1.8), "🏆 MONTHLY_DRAWS", "PK: id | FK: plan_id, winner_id\nFields: discount, dividend, net_pay", RGBColor(243, 232, 255), PURPLE)

    node_members = add_box(s3, Inches(2.8), Inches(4.5), Inches(2.8), Inches(1.8), "🎟️ PLAN_MEMBERS", "PK: id | FK: user_id, plan_id\nFields: ticket_number, reason", RGBColor(236, 253, 245), GREEN)
    node_inst = add_box(s3, Inches(6.4), Inches(4.5), Inches(2.6), Inches(1.8), "💳 INSTALLMENTS", "PK: id | FK: member_id\nFields: total_amount (Net Pay), status", RGBColor(254, 242, 242), RGBColor(239, 68, 68))
    node_pay = add_box(s3, Inches(9.8), Inches(4.5), Inches(2.5), Inches(1.8), "📱 PAYMENTS", "PK: id | FK: installment_id\nFields: transaction_id, status", RGBColor(240, 253, 250), RGBColor(20, 184, 166))

    # Legend text box
    tb_er = s3.shapes.add_textbox(Inches(0.8), Inches(6.5), Inches(11.0), Inches(0.6))
    tf_er = tb_er.text_frame
    p_er = tf_er.paragraphs[0]
    p_er.text = "Cardinality: USERS 1:N PLAN_MEMBERS | CHIT_PLANS 1:N PLAN_MEMBERS | CHIT_PLANS 1:N MONTHLY_DRAWS | PLAN_MEMBERS 1:N INSTALLMENTS 1:N PAYMENTS"
    p_er.font.size = Pt(10)
    p_er.font.bold = True
    p_er.font.color.rgb = NAVY

    # SLIDE 4: DFD Level 0 (Context Diagram)
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Data Flow Diagram — Level 0 (Context Diagram)", "PROCESS MODELING")

    # Entities and Process
    add_box(s4, Inches(0.8), Inches(3.0), Inches(3.0), Inches(2.2), "👤 MEMBER\n(External Entity)", "• Register & Submit KYC\n• Request to Join Plan\n• Pay Net Monthly Dues via UPI", LIGHT_BLUE, BORDER_BLUE)
    add_box(s4, Inches(4.8), Inches(2.5), Inches(3.7), Inches(3.2), "🏢 0.0\nSECURECHIT SYSTEM\n(Central Process)", "Automated Chit Fund Management,\nReal-Time Dividend Distribution,\nAI Emergency Allocation Engine", AMBER_BG, GOLD, is_oval=True)
    add_box(s4, Inches(9.5), Inches(3.0), Inches(3.0), Inches(2.2), "🛠️ ADMIN\n(External Entity)", "• Create & Start Schemes\n• Approve Members & KYC\n• Conduct Monthly Auction Draw", RGBColor(236, 253, 245), GREEN)

    tb_dfd0 = s4.shapes.add_textbox(Inches(0.8), Inches(6.1), Inches(11.7), Inches(1.0))
    tf_dfd0 = tb_dfd0.text_frame
    p0 = tf_dfd0.paragraphs[0]
    p0.text = "Data Flows: Member ──> System (Auth, Plan Request, UPI Payment) | System ──> Member (Digital Receipt, Dividends)"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = NAVY

    p1 = tf_dfd0.add_paragraph()
    p1.text = "Admin ──> System (Scheme Creation, Approvals, Auction Bidding) | System ──> Admin (AI Recommendations, Audit Reports)"
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = GOLD

    # SLIDE 5: DFD Level 1 (Subsystems & Data Stores)
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Data Flow Diagram — Level 1 (Subsystems & Data Stores)", "DETAILED PROCESS FLOW")

    # Subsystems
    add_box(s5, Inches(0.8), Inches(1.5), Inches(2.6), Inches(1.6), "1.0 Auth & KYC Subsystem", "User Login, Password Reset, Aadhar/PAN Upload", LIGHT_BLUE, BORDER_BLUE)
    add_box(s5, Inches(3.8), Inches(1.5), Inches(2.6), Inches(1.6), "2.0 Plan & Member Mgmt", "Create Scheme, Approve Registrations, Ticket Allocation", AMBER_BG, GOLD)
    add_box(s5, Inches(6.8), Inches(1.5), Inches(2.6), Inches(1.6), "3.0 Payment Gateway", "Instant UPI Checkout, Receipt Generator", RGBColor(240, 253, 250), RGBColor(20, 184, 166))
    add_box(s5, Inches(9.8), Inches(1.5), Inches(2.6), Inches(1.6), "4.0 AI Auction Engine", "Emergency Rank Scoring, Dividend Calculation", RGBColor(243, 232, 255), PURPLE)

    # Data Stores
    add_box(s5, Inches(0.8), Inches(4.5), Inches(2.2), Inches(1.5), "📂 D1: Users DB", "User Profiles, KYC Docs", LIGHT_BLUE, BORDER_BLUE)
    add_box(s5, Inches(3.3), Inches(4.5), Inches(2.2), Inches(1.5), "📂 D2: Chit Plans DB", "Scheme Rules, Chit Value", AMBER_BG, GOLD)
    add_box(s5, Inches(5.8), Inches(4.5), Inches(2.2), Inches(1.5), "📂 D3: Membership DB", "Tickets, Priority Scores", RGBColor(236, 253, 245), GREEN)
    add_box(s5, Inches(8.3), Inches(4.5), Inches(2.2), Inches(1.5), "📂 D4: Monthly Draws DB", "Bids, Dividends, Payouts", RGBColor(243, 232, 255), PURPLE)
    add_box(s5, Inches(10.8), Inches(4.5), Inches(1.8), Inches(1.5), "📂 D5: Payments DB", "Installments, UPI Ref", RGBColor(254, 242, 242), RGBColor(239, 68, 68))

    # SLIDE 6: Visual Use Case Diagram
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Use Case Design & Actor Roles", "BEHAVIORAL MODEL")

    # Member Actor
    add_box(s6, Inches(0.6), Inches(2.5), Inches(2.2), Inches(3.0), "👤 MEMBER ACTOR", "Subscribers who join schemes, pay monthly dues, and receive dividends", LIGHT_BLUE, BORDER_BLUE)

    # System Boundary Box
    add_box(s6, Inches(3.2), Inches(1.3), Inches(6.8), Inches(5.6), "SECURECHIT SYSTEM BOUNDARY", "", WHITE, NAVY)

    # Use Cases Ovals inside System Boundary
    ucs_member = [
        ("UC-1: Register & Login", 1.8),
        ("UC-2: Upload KYC & Guarantor", 2.6),
        ("UC-3: Explore & Request to Join Plan", 3.4),
        ("UC-4: View Schedule (Unlocked Due & Locked Future)", 4.2),
        ("UC-5: Pay Monthly Net Due via UPI", 5.0),
        ("UC-6: Download Receipt & Dividend Statement", 5.8)
    ]
    for uc_title, top_val in ucs_member:
        add_box(s6, Inches(3.5), Inches(top_val), Inches(3.0), Inches(0.65), uc_title, "", bg_color=LIGHT_BLUE, border_color=BORDER_BLUE, is_oval=True)

    ucs_admin = [
        ("UC-7: Review & Approve Member KYC", 1.8),
        ("UC-8: Create & Launch Chit Schemes", 2.8),
        ("UC-9: Conduct Monthly Auction Draw", 3.8),
        ("UC-10: AI Urgency Ranking (Hospital > Edu)", 4.8),
        ("UC-11: Generate Audit Logs & Financial Reports", 5.8)
    ]
    for uc_title, top_val in ucs_admin:
        add_box(s6, Inches(6.7), Inches(top_val), Inches(3.1), Inches(0.65), uc_title, "", bg_color=AMBER_BG, border_color=GOLD, is_oval=True)

    # Admin Actor
    add_box(s6, Inches(10.4), Inches(2.5), Inches(2.3), Inches(3.0), "🛠️ ADMIN ACTOR", "System Administrator who manages plans, approvals, and auction draws", RGBColor(236, 253, 245), GREEN)

    output_path = r"c:\chit fund\SecureChit_Presentation_Visual.pptx"
    prs.save(output_path)
    print(f"[SUCCESS] High-quality visual diagram presentation saved to {output_path}")

if __name__ == "__main__":
    build_visual_presentation()

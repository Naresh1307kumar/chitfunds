import os
import shutil
import math
from PIL import Image, ImageDraw, ImageFont

def draw_rounded_card(draw, bbox, title, bullets, bg_color, border_color, title_color, font_title, font_bullet, radius=12):
    x1, y1, x2, y2 = bbox
    # Draw rounded rectangle
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=bg_color, outline=border_color, width=2)
    
    # Title
    draw.text(((x1 + x2) // 2, y1 + 18), title, fill=title_color, font=font_title, anchor="mm")
    
    # Divider line under title
    draw.line([(x1 + 25, y1 + 32), (x2 - 25, y1 + 32)], fill=border_color, width=1)
    
    # Bullets
    start_y = y1 + 44
    line_spacing = 20
    for i, bullet in enumerate(bullets):
        draw.text((x1 + 20, start_y + i * line_spacing), "•  " + bullet, fill="#0F172A", font=font_bullet, anchor="lm")

def draw_double_arrow(draw, cx, y_start, y_end, label_lines, font_label):
    c_arrow = "#0F172A"
    # Vertical line
    draw.line([(cx, y_start), (cx, y_end)], fill=c_arrow, width=2)
    
    # Top arrowhead
    arrow_len = 8
    draw.polygon([(cx, y_start), (cx - 4, y_start + arrow_len), (cx + 4, y_start + arrow_len)], fill=c_arrow)
    # Bottom arrowhead
    draw.polygon([(cx, y_end), (cx - 4, y_end - arrow_len), (cx + 4, y_end - arrow_len)], fill=c_arrow)
    
    # Labels
    mid_y = (y_start + y_end) // 2
    if len(label_lines) == 1:
        draw.text((cx + 14, mid_y), label_lines[0], fill="#334155", font=font_label, anchor="lm")
    elif len(label_lines) == 2:
        draw.text((cx + 14, mid_y - 7), label_lines[0], fill="#334155", font=font_label, anchor="lm")
        draw.text((cx + 14, mid_y + 8), label_lines[1], fill="#64748B", font=font_label, anchor="lm")

def generate_four_tier_architecture():
    # Width: 720 px, Height: 940 px @ 150 DPI (~4.8" x 6.2" - Perfect for Word page)
    width, height = 720, 940
    img = Image.new('RGB', (width, height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        font_caption = ImageFont.truetype("arialbd.ttf", 12)
        font_title = ImageFont.truetype("arialbd.ttf", 12)
        font_bullet = ImageFont.truetype("arial.ttf", 10)
        font_label = ImageFont.truetype("arial.ttf", 9)
    except:
        font_caption = font_title = font_bullet = font_label = ImageFont.load_default()

    # Card dimensions
    card_w = 600
    card_h = 135
    card_x1 = (width - card_w) // 2
    card_x2 = card_x1 + card_w
    arrow_cx = card_x1 + 140  # Arrow placed neatly on left-middle

    # ----------------- TIER 1 -----------------
    y1_start = 35
    y1_end = y1_start + card_h
    t1_bullets = [
        "Single Page Application built with React 18, Vite 5, and Tailwind CSS",
        "Member Portal: Scheme Catalog, Live Reverse Auction Room, HTML5 Canvas Signing",
        "Admin Portal: KYC Verification Queue, Scheme Creator, Master Payment Ledger",
        "Modals & Viewers: UPI/QR Modal, Downloadable PDF Receipts (REC-2026-XXXX)"
    ]
    draw_rounded_card(draw, [card_x1, y1_start, card_x2, y1_end], 
                      "TIER 1: PRESENTATION LAYER (CLIENT)", t1_bullets,
                      bg_color="#EEF2FF", border_color="#4F46E5", title_color="#312E81",
                      font_title=font_title, font_bullet=font_bullet)

    # Arrow 1 -> 2
    arrow1_start = y1_end
    arrow1_end = arrow1_start + 65
    draw_double_arrow(draw, arrow_cx, arrow1_start + 6, arrow1_end - 6, 
                      ["HTTPS / RESTful requests", "JSON payloads / JWT Bearer tokens (Axios client)"], font_label)

    # ----------------- TIER 2 -----------------
    y2_start = arrow1_end
    y2_end = y2_start + card_h
    t2_bullets = [
        "FastAPI ASGI application server running on Uvicorn (Port 8000)",
        "APIRouters: AuthRouter, SchemeRouter, DrawRouter, PronoteRouter, PaymentRouter",
        "Security & Auth: JWT Bearer authentication, RBAC middleware, Passlib BCrypt hashing",
        "Request Validation: Pydantic v2 schemas, CORS handling, SlowAPI rate-limiting"
    ]
    draw_rounded_card(draw, [card_x1, y2_start, card_x2, y2_end], 
                      "TIER 2: API GATEWAY & SECURITY LAYER", t2_bullets,
                      bg_color="#F0FDFA", border_color="#0D9488", title_color="#134E4A",
                      font_title=font_title, font_bullet=font_bullet)

    # Arrow 2 -> 3
    arrow2_start = y2_end
    arrow2_end = arrow2_start + 65
    draw_double_arrow(draw, arrow_cx, arrow2_start + 6, arrow2_end - 6, 
                      ["Internal Service Pipelines / Async Handlers", "Pydantic DTO Serialization & Dependency Injection"], font_label)

    # ----------------- TIER 3 -----------------
    y3_start = arrow2_end
    y3_end = y3_start + card_h
    t3_bullets = [
        "Auction & Bidding Engine: Live reverse bidding & 5-tier AI Emergency Prioritization",
        "Financial Computation: 5% Foreman commission cap & equal net dividend distribution",
        "Pronote Execution Engine: HTML5 canvas Base64 signature capture & PDF rendering",
        "Notification & Verification: Dynamic UPI QR generator & SMTP email reminder service"
    ]
    draw_rounded_card(draw, [card_x1, y3_start, card_x2, y3_end], 
                      "TIER 3: BUSINESS LOGIC & COMPUTATION ENGINE LAYER", t3_bullets,
                      bg_color="#ECFDF5", border_color="#10B981", title_color="#064E3B",
                      font_title=font_title, font_bullet=font_bullet)

    # Arrow 3 -> 4
    arrow3_start = y3_end
    arrow3_end = arrow3_start + 65
    draw_double_arrow(draw, arrow_cx, arrow3_start + 6, arrow3_end - 6, 
                      ["SQLAlchemy 2.0 ORM / Psycopg2 Driver", "ACID Transactions & Database Connection Pooling"], font_label)

    # ----------------- TIER 4 -----------------
    y4_start = arrow3_end
    y4_end = y4_start + card_h
    t4_bullets = [
        "PostgreSQL 16 relational engine (Port 5433 / 5432, database: Secure)",
        "Tables: users, kyc, chit_plans, plan_members, draws, promissory_notes, installments, payments",
        "Enforces strict ACID transactions, foreign key integrity, and unique UTR/receipt constraints",
        "Maintains immutable financial audit logs and automated daily snapshot backups"
    ]
    draw_rounded_card(draw, [card_x1, y4_start, card_x2, y4_end], 
                      "TIER 4: DATA PERSISTENCE LAYER (DATABASE)", t4_bullets,
                      bg_color="#FEF3C7", border_color="#D97706", title_color="#78350F",
                      font_title=font_title, font_bullet=font_bullet)

    # Caption
    caption = "Figure 4.4: Four-Tier Architecture Diagram of SecureChit Platform"
    draw.text((width // 2, y4_end + 38), caption, fill="#0F172A", font=font_caption, anchor="mm")

    # Save output
    out_file = "Four_Tier_Architecture.png"
    img.save(out_file, dpi=(150, 150), quality=95)
    print(f"Generated {out_file} successfully!")

    # Copy to brain artifact directory
    artifact_dir = r"C:\Users\nares\.gemini\antigravity\brain\f74afe5d-2f73-4013-bc1e-3562e05df0f5"
    if os.path.exists(artifact_dir):
        shutil.copy(out_file, os.path.join(artifact_dir, "Four_Tier_Architecture.png"))
        print(f"Copied to artifact dir: {artifact_dir}")

if __name__ == "__main__":
    generate_four_tier_architecture()

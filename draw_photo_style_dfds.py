import os
import math
from PIL import Image, ImageDraw, ImageFont

def draw_open_cylinder(draw, bbox, name_text, font_bold=None):
    x1, y1, x2, y2 = bbox
    c_outline = "#222222"
    c_fill = "#FFFFFF"
    
    ellipse_h = 22
    # Top Oval
    draw.ellipse([x1, y1, x2, y1 + ellipse_h], fill="#FAFAFA", outline=c_outline, width=2)
    # Body
    draw.rectangle([x1, y1 + ellipse_h//2, x2, y2 - ellipse_h//2], fill=c_fill, outline=None)
    draw.line([(x1, y1 + ellipse_h//2), (x1, y2 - ellipse_h//2)], fill=c_outline, width=2)
    draw.line([(x2, y1 + ellipse_h//2), (x2, y2 - ellipse_h//2)], fill=c_outline, width=2)
    # Bottom Arc
    draw.arc([x1, y2 - ellipse_h, x2, y2], start=0, end=180, fill=c_outline, width=2)
    
    # Text inside Cylinder
    cy = (y1 + y2) // 2 + 2
    draw.text(( (x1+x2)//2, cy ), name_text, fill="#111827", font=font_bold, anchor="mm")

def draw_label_box(draw, bbox, text, font=None):
    x1, y1, x2, y2 = bbox
    draw.rounded_rectangle([x1, y1, x2, y2], radius=3, fill="#FFFFFF", outline="#444444", width=1)
    draw.text(( (x1+x2)//2, (y1+y2)//2 ), text, fill="#111827", font=font, anchor="mm")

def draw_arrow_line(draw, start, end, color="#222222", width=2):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=color, width=width)
    
    # Arrowhead at end
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 12
    p1 = (x2 - arrow_len * math.cos(angle - math.pi/6), y2 - arrow_len * math.sin(angle - math.pi/6))
    p2 = (x2 - arrow_len * math.cos(angle + math.pi/6), y2 - arrow_len * math.sin(angle + math.pi/6))
    draw.polygon([(x2, y2), p1, p2], fill=color)

# ------------------------------------------------------------------------------
# LEVEL 0 DFD - Photo 2 Exact Format
# ------------------------------------------------------------------------------
def generate_dfd_level_0():
    img = Image.new('RGB', (1400, 950), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 24)
        font_bold = ImageFont.truetype("arialbd.ttf", 15)
        font_main = ImageFont.truetype("arialbd.ttf", 13)
        font_sub = ImageFont.truetype("arial.ttf", 11)
    except:
        font_title = font_bold = font_main = font_sub = ImageFont.load_default()

    # Title at top
    draw.text((700, 35), "Level-0 (DFD) – System Context Diagram", fill="#111827", font=font_title, anchor="mt")

    # 1. Top Entity: ADMINISTRATOR (Rectangle)
    draw.rounded_rectangle([520, 100, 880, 175], radius=6, fill="#FFFFFF", outline="#222222", width=2)
    draw.text((700, 125), "ADMINISTRATOR", fill="#111827", font=font_bold, anchor="mm")
    draw.text((700, 150), "Enterprise Governance", fill="#555555", font=font_sub, anchor="mm")

    # 2. Bottom-Left Entity: SUBSCRIBER / MEMBER (Rectangle)
    draw.rounded_rectangle([40, 640, 340, 720], radius=6, fill="#FFFFFF", outline="#222222", width=2)
    draw.text((190, 668), "SUBSCRIBER / MEMBER", fill="#111827", font=font_bold, anchor="mm")
    draw.text((190, 693), "Chit Group Participant", fill="#555555", font=font_sub, anchor="mm")

    # 3. Bottom-Right Entity: PAYMENT & SMS GATEWAY (Rectangle)
    draw.rounded_rectangle([1060, 640, 1360, 720], radius=6, fill="#FFFFFF", outline="#222222", width=2)
    draw.text((1210, 668), "PAYMENT & SMS GATEWAY", fill="#111827", font=font_bold, anchor="mm")
    draw.text((1210, 693), "External Payment & Alert Services", fill="#555555", font=font_sub, anchor="mm")

    # 4. Center Circle: SecureChit Management System (SCMS)
    draw.ellipse([500, 420, 900, 700], fill="#FFFFFF", outline="#222222", width=3)
    draw.text((700, 535), "SecureChit Management\nSystem (SCMS)", fill="#111827", font=font_bold, anchor="mm")
    draw.text((700, 585), "Multi-Tenant Cloud Platform", fill="#555555", font=font_sub, anchor="mm")

    # --- ARROWS & FLOW LABEL BOXES ---
    # Top-Left Flow: ADMINISTRATOR -> SCMS
    draw_arrow_line(draw, (620, 175), (590, 425))
    draw_label_box(draw, [250, 280, 590, 330], "Chit Group Specs & Staff Accounts\nScheme Rules & Leader Allocation", font=font_sub)

    # Top-Right Flow: SCMS -> ADMINISTRATOR
    draw_arrow_line(draw, (790, 425), (780, 175))
    draw_label_box(draw, [810, 280, 1150, 330], "AI Delay Risk & Default Analytics\nSigned Pronotes & Financial Reports", font=font_sub)

    # Left-Top Flow: MEMBER -> SCMS
    draw_arrow_line(draw, (200, 640), (510, 510))
    draw_label_box(draw, [230, 440, 530, 490], "Registration & KYC Documents\nLive Reverse Bids & Canvas Signature", font=font_sub)

    # Left-Bottom Flow: SCMS -> MEMBER
    draw_arrow_line(draw, (510, 610), (340, 670))
    draw_label_box(draw, [150, 750, 470, 800], "Assigned Ticket & Plan Details\nInstant PDF Receipts & Dividend Alerts", font=font_sub)

    # Right-Top Flow: GATEWAY -> SCMS
    draw_arrow_line(draw, (1190, 640), (890, 510))
    draw_label_box(draw, [870, 440, 1170, 490], "UPI / Razorpay Status Updates\nSMS & Email Delivery Acknowledgments", font=font_sub)

    # Right-Bottom Flow: SCMS -> GATEWAY
    draw_arrow_line(draw, (890, 610), (1060, 670))
    draw_label_box(draw, [930, 750, 1250, 800], "Payment Order Triggers & Payload\nSMS / Email Notification Queue", font=font_sub)

    img.save("dfd_level_0.png")
    print("Generated photo-format dfd_level_0.png")

# ------------------------------------------------------------------------------
# LEVEL 1 DFD - Photo 1 Exact Format
# ------------------------------------------------------------------------------
def generate_dfd_level_1():
    img = Image.new('RGB', (1400, 1050), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 24)
        font_bold = ImageFont.truetype("arialbd.ttf", 15)
        font_main = ImageFont.truetype("arialbd.ttf", 13)
        font_sub = ImageFont.truetype("arial.ttf", 11)
    except:
        font_title = font_bold = font_main = font_sub = ImageFont.load_default()

    # Title at top
    draw.text((700, 35), "Level-1 (DFD) – Administrator & Organization Governance Module", fill="#111827", font=font_title, anchor="mt")

    # Left Entity: ADMINISTRATOR (Rectangle)
    draw.rounded_rectangle([60, 480, 280, 560], radius=6, fill="#FFFFFF", outline="#222222", width=2)
    draw.text((170, 510), "ADMINISTRATOR", fill="#111827", font=font_bold, anchor="mm")
    draw.text((170, 535), "Enterprise Governance", fill="#555555", font=font_sub, anchor="mm")

    processes = [
        ("Chit Scheme Onboarding\n& Workspace Setup", 180),
        ("Member Onboarding\n& KYC Provisioning", 400),
        ("Auction Bidding &\nWinner Allocation", 620),
        ("Pronote & Financial\nAudit Engine", 840),
    ]

    stores = [
        ("Chit Plans Database", 180, "Store Scheme Specs & Plan Rules"),
        ("Users & KYC Database", 400, "Save Member Credentials & KYC"),
        ("Auctions & Bids Database", 620, "Save Bids & Winner Allocation"),
        ("Pronotes & Payments Database", 840, "Query Pronotes, Receipts & Audit Logs"),
    ]

    for i, (p_name, cy) in enumerate(processes):
        draw.ellipse([500, cy-60, 680, cy+60], fill="#FFFFFF", outline="#222222", width=2)
        draw.text((590, cy), p_name, fill="#111827", font=font_main, anchor="mm")

    for i, (s_name, cy, flow_label) in enumerate(stores):
        draw_open_cylinder(draw, [960, cy-35, 1260, cy+35], s_name, font_bold=font_bold)
        draw_arrow_line(draw, (680, cy), (960, cy))
        draw_label_box(draw, [695, cy-45, 945, cy-15], flow_label, font=font_sub)

    flow_labels_admin = [
        ("Scheme Parameters & Tier Config", 180),
        ("Member Onboarding & KYC Details", 400),
        ("Trigger Monthly Auction Draw", 620),
        ("Inspect Pronotes & Audit Reports", 840),
    ]

    for label_text, cy in flow_labels_admin:
        draw_arrow_line(draw, (280, 520), (500, cy))
        lx = (280 + 500) // 2
        ly = (520 + cy) // 2
        draw_label_box(draw, [lx-110, ly-15, lx+110, ly+15], label_text, font=font_sub)

    img.save("dfd_level_1.png")
    print("Generated photo-format dfd_level_1.png")

# ------------------------------------------------------------------------------
# LEVEL 2 DFD - Photo Format
# ------------------------------------------------------------------------------
def generate_dfd_level_2():
    img = Image.new('RGB', (1400, 1050), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 24)
        font_bold = ImageFont.truetype("arialbd.ttf", 15)
        font_main = ImageFont.truetype("arialbd.ttf", 13)
        font_sub = ImageFont.truetype("arial.ttf", 11)
    except:
        font_title = font_bold = font_main = font_sub = ImageFont.load_default()

    # Title at top
    draw.text((700, 35), "Level-2 (DFD) – Auction Bidding & Pronote Execution Module", fill="#111827", font=font_title, anchor="mt")

    # Left Entity: SUBSCRIBER (Rectangle)
    draw.rounded_rectangle([60, 480, 280, 560], radius=6, fill="#FFFFFF", outline="#222222", width=2)
    draw.text((170, 510), "SUBSCRIBER / MEMBER", fill="#111827", font=font_bold, anchor="mm")
    draw.text((170, 535), "Auction Winner", fill="#555555", font=font_sub, anchor="mm")

    processes = [
        ("Reverse Auction Bidding\n& Floor Validation", 180),
        ("Dividend Calculation\n& 5% Fee Deduction", 400),
        ("Auto-Pronote Generation\n(PRN-YYYY-XXXX)", 620),
        ("Canvas Digital Signature\n& Admin Verification", 840),
    ]

    stores = [
        ("Bids & Auction DB", 180, "Store Valid Bid Amounts"),
        ("Chit Ledger DB", 400, "Update Monthly Net Payable"),
        ("Promissory Notes DB", 620, "Save Pending Pronote Record"),
        ("Signed Documents DB", 840, "Update Status to ACTIVE"),
    ]

    for i, (p_name, cy) in enumerate(processes):
        draw.ellipse([500, cy-60, 680, cy+60], fill="#FFFFFF", outline="#222222", width=2)
        draw.text((590, cy), p_name, fill="#111827", font=font_main, anchor="mm")

    for i, (s_name, cy, flow_label) in enumerate(stores):
        draw_open_cylinder(draw, [960, cy-35, 1260, cy+35], s_name, font_bold=font_bold)
        draw_arrow_line(draw, (680, cy), (960, cy))
        draw_label_box(draw, [695, cy-45, 945, cy-15], flow_label, font=font_sub)

    flow_labels_member = [
        ("Submit Discount Bid Amount", 180),
        ("Receive Dividend Share Credit", 400),
        ("Receive Pronote Alert", 620),
        ("Draw Canvas Touch Signature", 840),
    ]

    for label_text, cy in flow_labels_member:
        draw_arrow_line(draw, (280, 520), (500, cy))
        lx = (280 + 500) // 2
        ly = (520 + cy) // 2
        draw_label_box(draw, [lx-110, ly-15, lx+110, ly+15], label_text, font=font_sub)

    img.save("dfd_level_2.png")
    print("Generated photo-format dfd_level_2.png")

if __name__ == "__main__":
    generate_dfd_level_0()
    generate_dfd_level_1()
    generate_dfd_level_2()

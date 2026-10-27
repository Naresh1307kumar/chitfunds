import os
from PIL import Image, ImageDraw, ImageFont

def draw_open_cylinder(draw, bbox, store_id, store_name, font_bold, font_main):
    # bbox: [x1, y1, x2, y2]
    x1, y1, x2, y2 = bbox
    c_fill = "#FFFFFF" # Plain white fill
    c_outline = "#000000" # Black outline
    c_text_id = "#000000"
    c_text_name = "#000000"
    
    ellipse_h = 24
    draw.ellipse([x1, y1, x2, y1 + ellipse_h], fill="#F8FAFC", outline=c_outline, width=3)
    draw.rectangle([x1, y1 + ellipse_h//2, x2, y2 - ellipse_h//2], fill=c_fill, outline=None)
    draw.line([(x1, y1 + ellipse_h//2), (x1, y2 - ellipse_h//2)], fill=c_outline, width=3)
    draw.line([(x2, y1 + ellipse_h//2), (x2, y2 - ellipse_h//2)], fill=c_outline, width=3)
    draw.arc([x1, y2 - ellipse_h, x2, y2], start=0, end=180, fill=c_outline, width=3)
    
    div_x = x1 + 65
    draw.line([(div_x, y1 + ellipse_h//2), (div_x, y2)], fill=c_outline, width=3)
    
    cy = (y1 + y2) // 2 + 2
    draw.text((x1 + 32, cy), store_id, fill=c_text_id, font=font_bold, anchor="mm")
    draw.text((div_x + (x2 - div_x)//2, cy), store_name, fill=c_text_name, font=font_main, anchor="mm")

def draw_arrow(draw, start, end, label="", font=None, label_pos="above", color="#000000"):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=color, width=3)
    
    # Large Arrowhead
    if x2 > x1 and y1 == y2: # Right
        draw.polygon([(x2, y2), (x2-14, y2-7), (x2-14, y2+7)], fill=color)
    elif x2 < x1 and y1 == y2: # Left
        draw.polygon([(x2, y2), (x2+14, y2-7), (x2+14, y2+7)], fill=color)
    elif y2 > y1 and x1 == x2: # Down
        draw.polygon([(x2, y2), (x2-7, y2-14), (x2+7, y2-14)], fill=color)
    elif y2 < y1 and x1 == x2: # Up
        draw.polygon([(x2, y2), (x2-7, y2+14), (x2+7, y2+14)], fill=color)
    else:
        import math
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 14
        p1 = (x2 - arrow_len * math.cos(angle - math.pi/6), y2 - arrow_len * math.sin(angle - math.pi/6))
        p2 = (x2 - arrow_len * math.cos(angle + math.pi/6), y2 - arrow_len * math.sin(angle + math.pi/6))
        draw.polygon([(x2, y2), p1, p2], fill=color)

    if label and font:
        lx, ly = (x1 + x2) // 2, (y1 + y2) // 2
        offset_y = -16 if label_pos == "above" else 16
        draw.text((lx, ly + offset_y), label, fill="#000000", font=font, anchor="mm")

def draw_level_0():
    # Larger resolution and big fonts (Zoomed In)
    img = Image.new('RGB', (1400, 800), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 28)
        font_bold = ImageFont.truetype("arialbd.ttf", 20)
        font_main = ImageFont.truetype("arialbd.ttf", 16)
        font_sub = ImageFont.truetype("arial.ttf", 14)
    except:
        font_title = font_bold = font_main = font_sub = ImageFont.load_default()

    draw.text((700, 40), "Level 0 DFD: Context Diagram", fill="#000000", font=font_title, anchor="mt")

    # Member User (Rectangle) - BIG
    draw.rectangle([60, 280, 300, 420], fill="#FFFFFF", outline="#000000", width=4)
    draw.text((180, 335), "Member User", fill="#000000", font=font_bold, anchor="mm")
    draw.text((180, 375), "[External Entity]", fill="#000000", font=font_sub, anchor="mm")

    # Admin / Foreman (Rectangle) - BIG
    draw.rectangle([1100, 280, 1340, 420], fill="#FFFFFF", outline="#000000", width=4)
    draw.text((1220, 335), "Admin / Foreman", fill="#000000", font=font_bold, anchor="mm")
    draw.text((1220, 375), "[External Entity]", fill="#000000", font=font_sub, anchor="mm")

    # Process 0.0 SECURECHIT SYSTEM (Circle) - BIG
    draw.ellipse([500, 200, 900, 500], fill="#FFFFFF", outline="#000000", width=5)
    draw.text((700, 310), "0.0", fill="#000000", font=font_title, anchor="mm")
    draw.text((700, 360), "SECURECHIT SYSTEM", fill="#000000", font=font_bold, anchor="mm")
    draw.text((700, 400), "(Central Process Circle)", fill="#000000", font=font_sub, anchor="mm")

    # Open Cylinder Data Store - BIG
    draw_open_cylinder(draw, [520, 620, 880, 720], "D1", "PostgreSQL Database", font_bold, font_main)

    # Arrows with BIG fonts
    draw_arrow(draw, (300, 310), (500, 310), "Credentials, Bids, Payments, Signatures", font_sub, "above")
    draw_arrow(draw, (500, 390), (300, 390), "Receipts, Dividend Alerts, Pronotes", font_sub, "below")

    draw_arrow(draw, (1100, 310), (900, 310), "Scheme Setup, KYC Approval, Draw Conduct", font_sub, "above")
    draw_arrow(draw, (900, 390), (1100, 390), "Financial Reports, Signed Pronotes", font_sub, "below")

    draw_arrow(draw, (660, 500), (660, 620), "Store Records", font_sub, "above")
    draw_arrow(draw, (740, 620), (740, 500), "Retrieve Data", font_sub, "below")

    img.save("dfd_level_0.png")
    print("Saved zoomed-in dfd_level_0.png")


def draw_level_1():
    # Large 1500x1100 canvas with big fonts
    img = Image.new('RGB', (1500, 1100), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 28)
        font_bold = ImageFont.truetype("arialbd.ttf", 18)
        font_main = ImageFont.truetype("arialbd.ttf", 15)
        font_sub = ImageFont.truetype("arial.ttf", 13)
    except:
        font_title = font_bold = font_main = font_sub = ImageFont.load_default()

    draw.text((750, 35), "Level 1 DFD: Subsystem Decomposition Flow Diagram", fill="#000000", font=font_title, anchor="mt")

    # Member User (Rectangle Left)
    draw.rectangle([50, 420, 240, 580], fill="#FFFFFF", outline="#000000", width=4)
    draw.text((145, 480), "MEMBER USER", fill="#000000", font=font_bold, anchor="mm")
    draw.text((145, 520), "[External Entity]", fill="#000000", font=font_sub, anchor="mm")

    # Admin / Foreman (Rectangle Right)
    draw.rectangle([1260, 420, 1450, 580], fill="#FFFFFF", outline="#000000", width=4)
    draw.text((1355, 480), "ADMIN / FOREMAN", fill="#000000", font=font_bold, anchor="mm")
    draw.text((1355, 520), "[External Entity]", fill="#000000", font=font_sub, anchor="mm")

    # 5 Process Circles (Big circles)
    processes = [
        ("1.0", "Authentication &\nKYC Verification", (460, 180)),
        ("2.0", "Chit Plan &\nGroup Management", (1040, 180)),
        ("3.0", "Auction Bidding &\nDraw Engine", (460, 500)),
        ("4.0", "Promissory Note &\nCanvas Signature", (1040, 500)),
        ("5.0", "Installments &\nPayment Gateway", (750, 850)),
    ]

    for p_id, p_name, (cx, cy) in processes:
        draw.ellipse([cx-110, cy-80, cx+110, cy+80], fill="#FFFFFF", outline="#000000", width=4)
        draw.text((cx, cy-25), p_id, fill="#000000", font=font_bold, anchor="mm")
        draw.text((cx, cy+15), p_name, fill="#000000", font=font_main, anchor="mm")

    # 5 Open Cylinders Data Stores (Big cylinders)
    stores = [
        ("D1", "Users & KYC DB", (750, 180)),
        ("D2", "Chit Plans DB", (750, 330)),
        ("D3", "Auctions & Bids DB", (750, 500)),
        ("D4", "Promissory Notes DB", (750, 670)),
        ("D5", "Installments DB", (750, 1000)),
    ]

    for s_id, s_name, (cx, cy) in stores:
        draw_open_cylinder(draw, [cx-120, cy-35, cx+120, cy+35], s_id, s_name, font_bold, font_main)

    # --- MEMBER ARROWS ---
    draw_arrow(draw, (240, 440), (350, 200), "Credentials / KYC", font_sub)
    draw_arrow(draw, (240, 460), (930, 180), "Explore / Join Scheme", font_sub)
    draw_arrow(draw, (240, 500), (350, 500), "Submit Auction Bid", font_sub)
    draw_arrow(draw, (240, 540), (930, 500), "Canvas Signature", font_sub)
    draw_arrow(draw, (240, 560), (640, 850), "Pay Due / UTR Receipt", font_sub)

    # --- ADMIN ARROWS ---
    draw_arrow(draw, (1260, 440), (570, 180), "Approve Member KYC", font_sub)
    draw_arrow(draw, (1260, 460), (1150, 200), "Create Scheme / Group", font_sub)
    draw_arrow(draw, (1260, 500), (570, 500), "Conduct Auction Draw", font_sub)
    draw_arrow(draw, (1260, 540), (1150, 500), "View & Print Pronotes", font_sub)
    draw_arrow(draw, (1260, 560), (860, 850), "Verify Receipts", font_sub)

    # --- PROCESS TO STORE LINES ---
    draw.line([(570, 180), (630, 180)], fill="#000000", width=3)
    draw.line([(930, 190), (870, 330)], fill="#000000", width=3)
    draw.line([(570, 500), (630, 500)], fill="#000000", width=3)
    draw.line([(930, 510), (870, 670)], fill="#000000", width=3)
    draw.line([(750, 930), (750, 965)], fill="#000000", width=3)

    img.save("dfd_level_1.png")
    print("Saved zoomed-in dfd_level_1.png")


def draw_level_2():
    img = Image.new('RGB', (1400, 900), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 28)
        font_bold = ImageFont.truetype("arialbd.ttf", 18)
        font_main = ImageFont.truetype("arialbd.ttf", 15)
        font_sub = ImageFont.truetype("arial.ttf", 13)
    except:
        font_title = font_bold = font_main = font_sub = ImageFont.load_default()

    draw.text((700, 35), "Level 2 DFD: Auction & Pronote Detailed Engine", fill="#000000", font=font_title, anchor="mt")

    # Entities (Rectangles)
    draw.rectangle([50, 220, 220, 320], fill="#FFFFFF", outline="#000000", width=4)
    draw.text((135, 255), "Admin / Foreman", fill="#000000", font=font_bold, anchor="mm")
    draw.text((135, 290), "[External Entity]", fill="#000000", font=font_sub, anchor="mm")

    draw.rectangle([50, 600, 220, 700], fill="#FFFFFF", outline="#000000", width=4)
    draw.text((135, 635), "Winning Member", fill="#000000", font=font_bold, anchor="mm")
    draw.text((135, 670), "[External Entity]", fill="#000000", font=font_sub, anchor="mm")

    # Sub-processes (Circles)
    sub_processes = [
        ("3.1", "Conduct Auction\n& Select Winner", (390, 270)),
        ("3.2", "Calculate Dividend\n& Foreman Fee", (700, 270)),
        ("4.1", "Auto-Generate Pronote\n(pending_signature)", (1060, 270)),
        ("4.2", "Member Signature\nHTML5 Canvas Pad", (1060, 650)),
        ("4.3", "Submit Signature &\nUpdate to Active", (700, 650)),
        ("4.4", "Admin View & Print\nOfficial Pronote PDF", (390, 650)),
    ]

    for p_id, p_name, (cx, cy) in sub_processes:
        draw.ellipse([cx-100, cy-65, cx+100, cy+65], fill="#FFFFFF", outline="#000000", width=4)
        draw.text((cx, cy-20), p_id, fill="#000000", font=font_bold, anchor="mm")
        draw.text((cx, cy+15), p_name, fill="#000000", font=font_main, anchor="mm")

    # Data Store Open Cylinders
    draw_open_cylinder(draw, [600, 430, 800, 500], "D3", "Auctions Table", font_bold, font_sub)
    draw_open_cylinder(draw, [960, 430, 1160, 500], "D4", "Promissory Note DB", font_bold, font_sub)

    # Arrows
    draw_arrow(draw, (220, 270), (290, 270), "Trigger Draw", font_sub)
    draw_arrow(draw, (490, 270), (600, 270), "Winner User ID", font_sub)
    draw_arrow(draw, (800, 270), (960, 270), "Net Loan Amount", font_sub)
    draw_arrow(draw, (1060, 335), (1060, 430), "Insert Record", font_sub)
    draw_arrow(draw, (1060, 500), (1060, 585), "Fetch Pending Note", font_sub)
    draw_arrow(draw, (220, 650), (960, 650), "Draw Signature & Submit", font_sub)
    draw_arrow(draw, (960, 650), (800, 650), "Base64 PNG", font_sub)
    draw_arrow(draw, (600, 650), (490, 650), "Active Note", font_sub)
    draw_arrow(draw, (390, 585), (220, 320), "Printable PDF Modal", font_sub)

    img.save("dfd_level_2.png")
    print("Saved zoomed-in dfd_level_2.png")


def draw_level_3():
    img = Image.new('RGB', (1400, 900), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 28)
        font_bold = ImageFont.truetype("arialbd.ttf", 18)
        font_main = ImageFont.truetype("arialbd.ttf", 15)
        font_sub = ImageFont.truetype("arial.ttf", 13)
    except:
        font_title = font_bold = font_main = font_sub = ImageFont.load_default()

    draw.text((700, 35), "Level 3 DFD: Canvas Signature & Persistence Engine", fill="#000000", font=font_title, anchor="mt")

    # Entities (Rectangles)
    draw.rectangle([50, 270, 220, 370], fill="#FFFFFF", outline="#000000", width=4)
    draw.text((135, 305), "Touch / Mouse", fill="#000000", font=font_bold, anchor="mm")
    draw.text((135, 340), "[Canvas Input]", fill="#000000", font=font_sub, anchor="mm")

    draw.rectangle([1180, 600, 1350, 700], fill="#FFFFFF", outline="#000000", width=4)
    draw.text((1265, 635), "Admin Portal", fill="#000000", font=font_bold, anchor="mm")
    draw.text((1265, 670), "[Print Modal]", fill="#000000", font=font_sub, anchor="mm")

    # Sub-processes (Circles)
    sub_processes = [
        ("4.2.1", "Capture Canvas\nStroke Vectors", (390, 320)),
        ("4.2.2", "Convert to Base64\nPNG Data String", (700, 320)),
        ("4.2.3", "Validate Required\nNote Fields", (1010, 320)),
        ("4.3.1", "Update DB Status to\n'active'", (1010, 650)),
        ("4.3.2", "Render Official\nPronote Document", (700, 650)),
        ("4.3.3", "Generate Printable\nPDF Receipt", (390, 650)),
    ]

    for p_id, p_name, (cx, cy) in sub_processes:
        draw.ellipse([cx-100, cy-65, cx+100, cy+65], fill="#FFFFFF", outline="#000000", width=4)
        draw.text((cx, cy-20), p_id, fill="#000000", font=font_bold, anchor="mm")
        draw.text((cx, cy+15), p_name, fill="#000000", font=font_main, anchor="mm")

    # Data Store Open Cylinder
    draw_open_cylinder(draw, [900, 460, 1120, 530], "D4", "promissory_note DB", font_bold, font_sub)

    # Directional Arrows
    draw_arrow(draw, (220, 320), (290, 320), "Pointer Events", font_sub)
    draw_arrow(draw, (490, 320), (600, 320), "Raw Pixels", font_sub)
    draw_arrow(draw, (800, 320), (910, 320), "Base64 String", font_sub)
    draw_arrow(draw, (1010, 385), (1010, 460), "Save Record", font_sub)
    draw_arrow(draw, (1010, 530), (1010, 585), "Fetch Active Note", font_sub)
    draw_arrow(draw, (910, 650), (800, 650), "Note + Signature", font_sub)
    draw_arrow(draw, (600, 650), (490, 650), "Formatted Layout", font_sub)
    draw_arrow(draw, (1010, 650), (1180, 650), "Display in Admin", font_sub)

    img.save("dfd_level_3.png")
    print("Saved zoomed-in dfd_level_3.png")

if __name__ == "__main__":
    draw_level_0()
    draw_level_1()
    draw_level_2()
    draw_level_3()

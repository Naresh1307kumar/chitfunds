import os
import shutil
import math
from PIL import Image, ImageDraw, ImageFont

def generate_level1_decomposition_diagram():
    # Width: 700 px, Height: 860 px
    # At 150 DPI, 700px = 4.66 inches (Fits within standard 6.5" Word portrait margin)
    width, height = 700, 860
    img = Image.new('RGB', (width, height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        font_caption = ImageFont.truetype("arialbd.ttf", 11)
        font_entity = ImageFont.truetype("arialbd.ttf", 11)
        font_proc_num = ImageFont.truetype("arialbd.ttf", 11)
        font_proc_title = ImageFont.truetype("arialbd.ttf", 10)
        font_store = ImageFont.truetype("arialbd.ttf", 11)
        font_label = ImageFont.truetype("arialbd.ttf", 9)
    except:
        font_caption = font_entity = font_proc_num = font_proc_title = font_store = font_label = ImageFont.load_default()

    # Colors
    c_entity_bg = "#0B132B"       # Dark Navy Black
    c_entity_text = "#FFFFFF"
    c_proc_border = "#4F46E5"     # Indigo / Blue outline
    c_proc_fill = "#EEF2FF"       # Soft pastel fill
    c_proc_text = "#0B132B"
    c_store_border = "#475569"    # Slate grey
    c_store_fill = "#F8FAFC"      # Light grey
    c_store_text = "#1E293B"
    c_arrow = "#1E293B"
    c_label = "#1E293B"

    # Positions
    x_entity = 35
    w_entity = 115
    
    x_proc_center = 335
    w_proc = 145
    h_proc = 52
    
    x_store = 535
    w_store = 125
    h_store = 42

    # Y-positions for the 6 processes
    y_procs = [80, 195, 310, 425, 540, 675]

    # Draw Helper: Data Store
    def draw_datastore(x, y, name):
        draw.rectangle([x, y, x + w_store, y + h_store], fill=c_store_fill, outline=c_store_border, width=2)
        draw.line([(x + 12, y), (x + 12, y + h_store)], fill=c_store_border, width=2)
        draw.text((x + 12 + (w_store - 12) // 2, y + h_store // 2), name, fill=c_store_text, font=font_store, anchor="mm")

    # Draw Helper: Process (Oval / Ellipse)
    def draw_process(cy, num_str, name_str):
        rx, ry = w_proc // 2, h_proc // 2
        draw.ellipse([x_proc_center - rx, cy - ry, x_proc_center + rx, cy + ry], 
                     fill=c_proc_fill, outline=c_proc_border, width=2)
        draw.text((x_proc_center, cy - 8), num_str, fill=c_proc_text, font=font_proc_num, anchor="mm")
        draw.text((x_proc_center, cy + 9), name_str, fill=c_proc_text, font=font_proc_title, anchor="mm")

    # Draw Helper: External Entity
    def draw_external_entity(y, h, name_lines):
        draw.rectangle([x_entity, y, x_entity + w_entity, y + h], fill=c_entity_bg)
        total_lines = len(name_lines)
        line_h = 14
        start_y = y + h // 2 - ((total_lines - 1) * line_h) // 2
        for i, line in enumerate(name_lines):
            draw.text((x_entity + w_entity // 2, start_y + i * line_h), line, fill=c_entity_text, font=font_entity, anchor="mm")

    # Draw Helper: Arrow with custom arrowhead
    def draw_arrow_manual(start, end):
        x1, y1 = start
        x2, y2 = end
        draw.line([start, end], fill=c_arrow, width=1)
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 8
        p1 = (x2 - arrow_len * math.cos(angle - math.pi/6), y2 - arrow_len * math.sin(angle - math.pi/6))
        p2 = (x2 - arrow_len * math.cos(angle + math.pi/6), y2 - arrow_len * math.sin(angle + math.pi/6))
        draw.polygon([(x2, y2), p1, p2], fill=c_arrow)

    # 1. DRAW 6 PROCESSES
    proc_labels = [
        ("1.0", "Authentication"),
        ("2.0", "Scheme Discovery"),
        ("3.0", "Auction & Bidding"),
        ("4.0", "Pronote Engine"),
        ("5.0", "Payment Verification"),
        ("6.0", "Platform Governance")
    ]
    for i, (num, name) in enumerate(proc_labels):
        draw_process(y_procs[i], num, name)

    # 2. DRAW DATA STORES (Right Column)
    store_configs = [
        (y_procs[0] - h_store // 2, "users"),
        (y_procs[1] - h_store // 2, "chit_plans"),
        (y_procs[2] - h_store // 2, "draws"),
        (y_procs[3] - h_store // 2, "promissory_notes"),
        (y_procs[4] - h_store // 2, "payments"),
        (y_procs[5] - 32, "users"),
        (y_procs[5] + 16, "payments")
    ]
    for y, name in store_configs:
        draw_datastore(x_store, y, name)

    # 3. DRAW EXTERNAL ENTITIES (Left Column)
    y_member = 185
    h_member = 55
    draw_external_entity(y_member, h_member, ["MEMBER", "(SUBSCRIBER)"])

    y_foreman = 425
    h_foreman = 55
    draw_external_entity(y_foreman, h_foreman, ["CHIT FOREMAN", "(MANAGER)"])

    y_admin = 647
    h_admin = 55
    draw_external_entity(y_admin, h_admin, ["ADMINISTRATOR"])

    # 4. ARROWS: Processes -> Data Stores (Right side)
    rx = w_proc // 2
    # 1.0 -> users
    draw_arrow_manual((x_proc_center + rx, y_procs[0]), (x_store, y_procs[0]))
    # 2.0 <-> chit_plans
    draw_arrow_manual((x_proc_center + rx, y_procs[1]), (x_store, y_procs[1]))
    # 3.0 -> draws
    draw_arrow_manual((x_proc_center + rx, y_procs[2]), (x_store, y_procs[2]))
    # 4.0 -> promissory_notes
    draw_arrow_manual((x_proc_center + rx, y_procs[3]), (x_store, y_procs[3]))
    # 5.0 -> payments
    draw_arrow_manual((x_proc_center + rx, y_procs[4]), (x_store, y_procs[4]))
    
    # 6.0 -> users (approve KYC)
    draw_arrow_manual((x_proc_center + rx, y_procs[5] - 8), (x_store, y_procs[5] - 12))
    draw.text((x_store - 48, y_procs[5] - 22), "approve KYC", fill=c_label, font=font_label, anchor="mm")

    # 6.0 -> payments (audit ledger)
    draw_arrow_manual((x_proc_center + rx, y_procs[5] + 8), (x_store, y_procs[5] + 36))
    draw.text((x_store - 48, y_procs[5] + 46), "audit ledger", fill=c_label, font=font_label, anchor="mm")

    # 5. ARROWS: Entities -> Processes (Left side)
    right_e = x_entity + w_entity

    # --- MEMBER ARROWS ---
    # MEMBER -> 1.0 (login / credentials)
    draw_arrow_manual((right_e, y_member + 10), (x_proc_center - rx, y_procs[0] + 5))
    draw.text((195, 120), "login / credentials", fill=c_label, font=font_label, anchor="mm")

    # MEMBER -> 2.0 (search & enroll)
    draw_arrow_manual((right_e, y_member + 27), (x_proc_center - rx, y_procs[1]))
    draw.text((205, 185), "search & enroll", fill=c_label, font=font_label, anchor="mm")

    # MEMBER -> 3.0 (submit bids / rank)
    draw_arrow_manual((right_e, y_member + 45), (x_proc_center - rx, y_procs[2] - 10))
    draw.text((200, 245), "submit bids", fill=c_label, font=font_label, anchor="mm")

    # --- FOREMAN ARROWS ---
    # FOREMAN -> 3.0 (conduct draw)
    draw_arrow_manual((right_e, y_foreman + 10), (x_proc_center - rx, y_procs[2] + 12))
    draw.text((200, 350), "conduct draw", fill=c_label, font=font_label, anchor="mm")

    # FOREMAN -> 4.0 (issue PRN note)
    draw_arrow_manual((right_e, y_foreman + 27), (x_proc_center - rx, y_procs[3]))
    draw.text((205, 412), "issue PRN note", fill=c_label, font=font_label, anchor="mm")

    # FOREMAN -> 5.0 (confirm & verify UTR)
    draw_arrow_manual((right_e, y_foreman + 45), (x_proc_center - rx, y_procs[4] - 8))
    draw.text((205, 520), "confirm & verify UTR", fill=c_label, font=font_label, anchor="mm")

    # --- ADMINISTRATOR ARROWS ---
    # ADMINISTRATOR -> 6.0 (KYC, audits, rules)
    draw_arrow_manual((right_e, y_admin + 27), (x_proc_center - rx, y_procs[5]))
    draw.text((205, 655), "KYC, audits, rules", fill=c_label, font=font_label, anchor="mm")

    # --- INTER-PROCESS ARROWS (Middle Column) ---
    # 3.0 -> 4.0 (winner chosen)
    draw_arrow_manual((x_proc_center, y_procs[2] + h_proc // 2), (x_proc_center, y_procs[3] - h_proc // 2))
    draw.text((x_proc_center + 46, (y_procs[2] + y_procs[3]) // 2), "winner chosen", fill=c_label, font=font_label, anchor="mm")

    # 4.0 -> 5.0 (net due amount)
    draw_arrow_manual((x_proc_center, y_procs[3] + h_proc // 2), (x_proc_center, y_procs[4] - h_proc // 2))
    draw.text((x_proc_center + 46, (y_procs[3] + y_procs[4]) // 2), "net due amount", fill=c_label, font=font_label, anchor="mm")

    # Figure Caption
    c_y = 795
    draw.text((width // 2, c_y), "Figure 4.3: Level 1 DFD (Decomposition Diagram)", fill="#0F172A", font=font_caption, anchor="mm")

    # Save output
    out_file = "DFD_Level_1_Decomposition.png"
    img.save(out_file, dpi=(150, 150), quality=95)
    print(f"Generated {out_file} successfully!")

    # Overwrite DFD_Level_1.png
    try:
        img.save("DFD_Level_1.png", dpi=(150, 150), quality=95)
        print("Updated DFD_Level_1.png!")
    except Exception as e:
        print("DFD_Level_1.png note:", e)

    # Copy to brain artifact directory
    artifact_dir = r"C:\Users\nares\.gemini\antigravity\brain\f74afe5d-2f73-4013-bc1e-3562e05df0f5"
    if os.path.exists(artifact_dir):
        shutil.copy(out_file, os.path.join(artifact_dir, "DFD_Level_1_Decomposition.png"))
        print(f"Copied to artifact dir: {artifact_dir}")

if __name__ == "__main__":
    generate_level1_decomposition_diagram()

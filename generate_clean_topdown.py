import os
import shutil
import math
from PIL import Image, ImageDraw, ImageFont

def generate_vertical_topdown():
    # Vertical Portrait Canvas (Width 840, Height 860) - Optimized for Word Portrait Page
    width, height = 840, 860
    img = Image.new('RGB', (width, height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        font_caption = ImageFont.truetype("arialbd.ttf", 12)
        font_box_title = ImageFont.truetype("arialbd.ttf", 13)
        font_box_sub = ImageFont.truetype("arial.ttf", 11)
        font_box_entity = ImageFont.truetype("ariali.ttf", 10)
        font_circle_num = ImageFont.truetype("arialbd.ttf", 17)
        font_circle_txt = ImageFont.truetype("arialbd.ttf", 13)
        font_label = ImageFont.truetype("arialbd.ttf", 10)
        font_db_id = ImageFont.truetype("arialbd.ttf", 14)
        font_db_name = ImageFont.truetype("arialbd.ttf", 12)
        font_db_sub = ImageFont.truetype("arial.ttf", 10)
    except:
        font_caption = font_box_title = font_box_sub = font_box_entity = font_circle_num = font_circle_txt = font_label = font_db_id = font_db_name = font_db_sub = ImageFont.load_default()

    c_border = "#0F172A"
    c_fill_box = "#FFFFFF"

    # Arrow drawer
    def draw_arrow(start, end):
        x1, y1 = start
        x2, y2 = end
        draw.line([start, end], fill=c_border, width=2)
        
        # Arrowhead
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 10
        p1 = (x2 - arrow_len * math.cos(angle - math.pi/6), y2 - arrow_len * math.sin(angle - math.pi/6))
        p2 = (x2 - arrow_len * math.cos(angle + math.pi/6), y2 - arrow_len * math.sin(angle + math.pi/6))
        draw.polygon([(x2, y2), p1, p2], fill=c_border)

    cx, cy = 420, 360
    r = 75

    # 1. TOP NODE: USER / SUBSCRIBER
    top_w, top_h = 240, 80
    bx_top = cx - top_w // 2
    by_top = 45
    draw.rectangle([bx_top, by_top, bx_top + top_w, by_top + top_h], fill=c_fill_box, outline=c_border, width=2)
    draw.text((cx, by_top + 23), "USER / SUBSCRIBER", fill=c_border, font=font_box_title, anchor="mm")
    draw.text((cx, by_top + 43), "(Chit Member)", fill="#334155", font=font_box_sub, anchor="mm")
    draw.text((cx, by_top + 61), "[External Entity]", fill="#64748B", font=font_box_entity, anchor="mm")

    # 2. CENTER NODE: 0.0 SECURE CHIT MANAGEMENT SYSTEM
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#F8FAFC", outline=c_border, width=2)
    draw.text((cx, cy - 26), "0.0", fill=c_border, font=font_circle_num, anchor="mm")
    draw.text((cx, cy - 6), "SECURE CHIT", fill=c_border, font=font_circle_txt, anchor="mm")
    draw.text((cx, cy + 12), "MANAGEMENT", fill=c_border, font=font_circle_txt, anchor="mm")
    draw.text((cx, cy + 30), "SYSTEM", fill=c_border, font=font_circle_txt, anchor="mm")

    # 3. BOTTOM LEFT NODE: ADMIN / CHIT FOREMAN
    bot_w, bot_h = 230, 80
    bx_bl = 45
    by_bot = 620
    draw.rectangle([bx_bl, by_bot, bx_bl + bot_w, by_bot + bot_h], fill=c_fill_box, outline=c_border, width=2)
    draw.text((bx_bl + bot_w//2, by_bot + 23), "ADMIN / CHIT FOREMAN", fill=c_border, font=font_box_title, anchor="mm")
    draw.text((bx_bl + bot_w//2, by_bot + 43), "(Chit Manager)", fill="#334155", font=font_box_sub, anchor="mm")
    draw.text((bx_bl + bot_w//2, by_bot + 61), "[External Entity]", fill="#64748B", font=font_box_entity, anchor="mm")

    # 4. BOTTOM RIGHT NODE: POSTGRESQL DATABASE
    bx_br = 565
    draw.rectangle([bx_br, by_bot, bx_br + bot_w, by_bot + bot_h], fill=c_fill_box, outline=c_border, width=2)
    div_x = bx_br + 50
    draw.line([(div_x, by_bot), (div_x, by_bot + bot_h)], fill=c_border, width=2)
    draw.text((bx_br + 25, by_bot + bot_h//2), "D1", fill=c_border, font=font_db_id, anchor="mm")
    draw.text((div_x + (bot_w - 50)//2, by_bot + 28), "POSTGRESQL DATABASE", fill=c_border, font=font_db_name, anchor="mm")
    draw.text((div_x + (bot_w - 50)//2, by_bot + 50), "(Central Relational Store)", fill="#475569", font=font_db_sub, anchor="mm")

    # --- TOP <--> CENTER (VERTICAL ARROWS) ---
    # Downward: User -> System
    draw_arrow((350, by_top + top_h), (350, cy - r))
    draw.text((336, (by_top + top_h + cy - r) // 2), "Chit Application, Bids, UPI UTR", fill=c_border, font=font_label, anchor="rm")

    # Upward: System -> User
    draw_arrow((490, cy - r), (490, by_top + top_h))
    draw.text((504, (by_top + top_h + cy - r) // 2), "Dynamic Dues, Statements, Receipts", fill=c_border, font=font_label, anchor="lm")

    # --- BOTTOM LEFT <--> CENTER (ADMIN <--> SYSTEM) ---
    # Up-Right arrow: Admin -> System
    draw_arrow((190, by_bot), (355, 415))
    # Label placed safely on upper outer flank
    draw.text((230, 480), "Scheme Specs, KYC Approvals", fill=c_border, font=font_label, anchor="rm")

    # Down-Left arrow: System -> Admin
    draw_arrow((375, 435), (235, by_bot))
    # Label placed safely on lower outer flank
    draw.text((260, 550), "Auction Summary, Reports, Pronotes", fill=c_border, font=font_label, anchor="rm")

    # --- BOTTOM RIGHT <--> CENTER (DATABASE <--> SYSTEM) ---
    # Up-Left arrow: Database -> System
    draw_arrow((650, by_bot), (485, 415))
    # Label placed safely on upper outer flank
    draw.text((610, 480), "Fetch Stored Data & Queries", fill=c_border, font=font_label, anchor="lm")

    # Down-Right arrow: System -> Database
    draw_arrow((465, 435), (605, by_bot))
    # Label placed safely on lower outer flank
    draw.text((580, 550), "Save / Update Records", fill=c_border, font=font_label, anchor="lm")

    # Figure Caption at bottom
    caption = "Figure 4.1: Level 0 Context Diagram showing Member User, Admin Foreman, Central System, and PostgreSQL Database."
    draw.text((cx, 780), caption, fill="#0F172A", font=font_caption, anchor="mm")

    # Save output
    out_file = "DFD_Level_0_Vertical_Clean.png"
    img.save(out_file, quality=95)
    print(f"Generated {out_file} successfully!")

    # Also overwrite standard DFD_Level_0.png
    img.save("DFD_Level_0.png", quality=95)
    print("Updated DFD_Level_0.png!")

    # Copy to brain artifact directory
    artifact_dir = r"C:\Users\nares\.gemini\antigravity\brain\f74afe5d-2f73-4013-bc1e-3562e05df0f5"
    if os.path.exists(artifact_dir):
        shutil.copy(out_file, os.path.join(artifact_dir, "DFD_Level_0_Vertical_Clean.png"))
        shutil.copy("DFD_Level_0.png", os.path.join(artifact_dir, "DFD_Level_0.png"))
        print(f"Copied to artifact dir: {artifact_dir}")

if __name__ == "__main__":
    generate_vertical_topdown()

import os
import shutil
import math
from PIL import Image, ImageDraw, ImageFont

def generate_perfect_vertical_dfd():
    # Compact square/portrait canvas (Width 800, Height 780) - Ideal for Word document
    width, height = 800, 780
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

    # Arrow helper
    def draw_arrow(start, end, label, label_pos="above", color="#0F172A", offset=12):
        x1, y1 = start
        x2, y2 = end
        draw.line([start, end], fill=color, width=2)
        
        # Arrowhead calculation
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 10
        p1 = (x2 - arrow_len * math.cos(angle - math.pi/6), y2 - arrow_len * math.sin(angle - math.pi/6))
        p2 = (x2 - arrow_len * math.cos(angle + math.pi/6), y2 - arrow_len * math.sin(angle + math.pi/6))
        draw.polygon([(x2, y2), p1, p2], fill=color)

        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            # Perpendicular vector for clean label offsetting
            perp_angle = angle - math.pi / 2
            if label_pos == "below" or label_pos == "right":
                perp_angle = angle + math.pi / 2

            lx = mx + offset * math.cos(perp_angle)
            ly = my + offset * math.sin(perp_angle)

            draw.text((lx, ly), label, fill=color, font=font_label, anchor="mm")

    # Center coordinates
    cx, cy = 400, 340
    r = 75

    # 1. TOP NODE: USER / SUBSCRIBER (Centered at Top)
    top_w, top_h = 240, 80
    bx_top = cx - top_w // 2
    by_top = 40
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
    by_bot = 560
    draw.rectangle([bx_bl, by_bot, bx_bl + bot_w, by_bot + bot_h], fill=c_fill_box, outline=c_border, width=2)
    draw.text((bx_bl + bot_w//2, by_bot + 23), "ADMIN / CHIT FOREMAN", fill=c_border, font=font_box_title, anchor="mm")
    draw.text((bx_bl + bot_w//2, by_bot + 43), "(Chit Manager)", fill="#334155", font=font_box_sub, anchor="mm")
    draw.text((bx_bl + bot_w//2, by_bot + 61), "[External Entity]", fill="#64748B", font=font_box_entity, anchor="mm")

    # 4. BOTTOM RIGHT NODE: POSTGRESQL DATABASE (Data Store)
    bx_br = 485
    draw.rectangle([bx_br, by_bot, bx_br + bot_w, by_bot + bot_h], fill=c_fill_box, outline=c_border, width=2)
    div_x = bx_br + 50
    draw.line([(div_x, by_bot), (div_x, by_bot + bot_h)], fill=c_border, width=2)
    draw.text((bx_br + 25, by_bot + bot_h//2), "D1", fill=c_border, font=font_db_id, anchor="mm")
    draw.text((div_x + (bot_w - 50)//2, by_bot + 28), "POSTGRESQL DATABASE", fill=c_border, font=font_db_name, anchor="mm")
    draw.text((div_x + (bot_w - 50)//2, by_bot + 50), "(Central Relational Store)", fill="#475569", font=font_db_sub, anchor="mm")

    # --- ARROWS ---
    # TOP <--> CENTER (Straight Vertical Arrows)
    # Down arrow: User -> System
    draw_arrow((cx - 35, by_top + top_h), (cx - 35, cy - r), 
               "Chit Application, Bids, UPI UTR", "above", offset=14)
    # Up arrow: System -> User
    draw_arrow((cx + 35, cy - r), (cx + 35, by_top + top_h), 
               "Dynamic Dues, Dividend Statements, Receipts", "below", offset=14)

    # BOTTOM LEFT <--> CENTER (Admin <--> System)
    # Up-Right arrow: Admin -> System
    p_admin_top = (bx_bl + bot_w - 30, by_bot)
    p_circ_bl_1 = (cx - int(r * 0.707) - 10, cy + int(r * 0.707) - 15)
    draw_arrow(p_admin_top, p_circ_bl_1, "Scheme Specs, KYC Approvals", "above", offset=14)

    # Down-Left arrow: System -> Admin
    p_circ_bl_2 = (cx - int(r * 0.707) + 12, cy + int(r * 0.707) + 5)
    p_admin_right = (bx_bl + bot_w, by_bot + 35)
    draw_arrow(p_circ_bl_2, p_admin_right, "Auction Summary, Reports, Pronotes", "below", offset=14)

    # BOTTOM RIGHT <--> CENTER (Database <--> System)
    # Down-Right arrow: System -> Database
    p_circ_br_1 = (cx + int(r * 0.707) - 12, cy + int(r * 0.707) + 5)
    p_db_left = (bx_br, by_bot + 35)
    draw_arrow(p_circ_br_1, p_db_left, "Save / Update Records", "below", offset=14)

    # Up-Left arrow: Database -> System
    p_db_top = (bx_br + 30, by_bot)
    p_circ_br_2 = (cx + int(r * 0.707) + 10, cy + int(r * 0.707) - 15)
    draw_arrow(p_db_top, p_circ_br_2, "Fetch Stored Data & Queries", "above", offset=14)

    # Figure Caption
    caption = "Figure 4.1: Level 0 Context Diagram showing Member User, Admin Foreman, Central System, and PostgreSQL Database."
    draw.text((cx, 710), caption, fill="#0F172A", font=font_caption, anchor="mm")

    # Save output files
    out_file = "DFD_Level_0_TopDown.png"
    img.save(out_file, quality=95)
    print(f"Generated {out_file} successfully!")

    # Overwrite primary DFD_Level_0.png
    img.save("DFD_Level_0.png", quality=95)
    print("Updated DFD_Level_0.png!")

    # Copy to brain artifact directory
    artifact_dir = r"C:\Users\nares\.gemini\antigravity\brain\f74afe5d-2f73-4013-bc1e-3562e05df0f5"
    if os.path.exists(artifact_dir):
        shutil.copy(out_file, os.path.join(artifact_dir, "DFD_Level_0_TopDown.png"))
        shutil.copy("DFD_Level_0.png", os.path.join(artifact_dir, "DFD_Level_0.png"))
        print(f"Copied to artifact dir: {artifact_dir}")

if __name__ == "__main__":
    generate_perfect_vertical_dfd()

import os
import shutil
import math
from PIL import Image, ImageDraw, ImageFont

def generate_word_fitted_dfd():
    # Compact canvas: 640px wide x 720px tall.
    # At 150 DPI, 640px = 4.26 inches (Comfortably fits standard 6.5" Word page width with zero cutoff!)
    width, height = 640, 720
    img = Image.new('RGB', (width, height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        font_caption = ImageFont.truetype("arialbd.ttf", 11)
        font_box_title = ImageFont.truetype("arialbd.ttf", 12)
        font_box_sub = ImageFont.truetype("arial.ttf", 10)
        font_box_entity = ImageFont.truetype("ariali.ttf", 9)
        font_circle_num = ImageFont.truetype("arialbd.ttf", 15)
        font_circle_txt = ImageFont.truetype("arialbd.ttf", 11)
        font_label = ImageFont.truetype("arialbd.ttf", 9)
        font_db_id = ImageFont.truetype("arialbd.ttf", 13)
        font_db_name = ImageFont.truetype("arialbd.ttf", 11)
        font_db_sub = ImageFont.truetype("arial.ttf", 9)
    except:
        font_caption = font_box_title = font_box_sub = font_box_entity = font_circle_num = font_circle_txt = font_label = font_db_id = font_db_name = font_db_sub = ImageFont.load_default()

    c_border = "#0F172A"
    c_fill_box = "#FFFFFF"

    # Arrow drawer
    def draw_arrow(start, end):
        x1, y1 = start
        x2, y2 = end
        draw.line([start, end], fill=c_border, width=2)
        
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 9
        p1 = (x2 - arrow_len * math.cos(angle - math.pi/6), y2 - arrow_len * math.sin(angle - math.pi/6))
        p2 = (x2 - arrow_len * math.cos(angle + math.pi/6), y2 - arrow_len * math.sin(angle + math.pi/6))
        draw.polygon([(x2, y2), p1, p2], fill=c_border)

    cx, cy = 320, 280
    r = 60

    # 1. TOP NODE: USER / SUBSCRIBER
    top_w, top_h = 240, 70
    bx_top = cx - top_w // 2
    by_top = 25
    draw.rectangle([bx_top, by_top, bx_top + top_w, by_top + top_h], fill=c_fill_box, outline=c_border, width=2)
    draw.text((cx, by_top + 20), "USER / SUBSCRIBER", fill=c_border, font=font_box_title, anchor="mm")
    draw.text((cx, by_top + 38), "(Chit Member)", fill="#334155", font=font_box_sub, anchor="mm")
    draw.text((cx, by_top + 54), "[External Entity]", fill="#64748B", font=font_box_entity, anchor="mm")

    # 2. CENTER NODE: 0.0 SECURE CHIT MANAGEMENT SYSTEM
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#F8FAFC", outline=c_border, width=2)
    draw.text((cx, cy - 22), "0.0", fill=c_border, font=font_circle_num, anchor="mm")
    draw.text((cx, cy - 5), "SECURE CHIT", fill=c_border, font=font_circle_txt, anchor="mm")
    draw.text((cx, cy + 10), "MANAGEMENT", fill=c_border, font=font_circle_txt, anchor="mm")
    draw.text((cx, cy + 25), "SYSTEM", fill=c_border, font=font_circle_txt, anchor="mm")

    # 3. BOTTOM LEFT NODE: ADMIN / CHIT FOREMAN
    bot_w, bot_h = 210, 72
    bx_bl = 20
    by_bot = 485
    draw.rectangle([bx_bl, by_bot, bx_bl + bot_w, by_bot + bot_h], fill=c_fill_box, outline=c_border, width=2)
    draw.text((bx_bl + bot_w//2, by_bot + 20), "ADMIN / CHIT FOREMAN", fill=c_border, font=font_box_title, anchor="mm")
    draw.text((bx_bl + bot_w//2, by_bot + 38), "(Chit Manager)", fill="#334155", font=font_box_sub, anchor="mm")
    draw.text((bx_bl + bot_w//2, by_bot + 54), "[External Entity]", fill="#64748B", font=font_box_entity, anchor="mm")

    # 4. BOTTOM RIGHT NODE: POSTGRESQL DATABASE
    bx_br = 410
    draw.rectangle([bx_br, by_bot, bx_br + bot_w, by_bot + bot_h], fill=c_fill_box, outline=c_border, width=2)
    div_x = bx_br + 45
    draw.line([(div_x, by_bot), (div_x, by_bot + bot_h)], fill=c_border, width=2)
    draw.text((bx_br + 22, by_bot + bot_h//2), "D1", fill=c_border, font=font_db_id, anchor="mm")
    draw.text((div_x + (bot_w - 45)//2, by_bot + 24), "POSTGRESQL DATABASE", fill=c_border, font=font_db_name, anchor="mm")
    draw.text((div_x + (bot_w - 45)//2, by_bot + 44), "(Central Relational Store)", fill="#475569", font=font_db_sub, anchor="mm")

    # --- TOP <--> CENTER (VERTICAL ARROWS) ---
    # Downward: User -> System
    draw_arrow((255, by_top + top_h), (255, cy - r))
    draw.text((243, 150), "Chit Application, Bids,", fill=c_border, font=font_label, anchor="rm")
    draw.text((243, 165), "UPI UTR Reference", fill=c_border, font=font_label, anchor="rm")

    # Upward: System -> User
    draw_arrow((385, cy - r), (385, by_top + top_h))
    draw.text((397, 150), "Dynamic Dues, Receipts,", fill=c_border, font=font_label, anchor="lm")
    draw.text((397, 165), "Dividend Statements", fill=c_border, font=font_label, anchor="lm")

    # --- BOTTOM LEFT <--> CENTER (ADMIN <--> SYSTEM) ---
    # Up-Right: Admin -> System
    draw_arrow((150, by_bot), (265, 325))
    draw.text((180, 385), "Scheme Specs, KYC Approvals", fill=c_border, font=font_label, anchor="rm")

    # Down-Left: System -> Admin
    draw_arrow((280, 340), (185, by_bot))
    draw.text((200, 435), "Auction Summary, Reports, Pronotes", fill=c_border, font=font_label, anchor="rm")

    # --- BOTTOM RIGHT <--> CENTER (DATABASE <--> SYSTEM) ---
    # Up-Left: Database -> System
    draw_arrow((490, by_bot), (375, 325))
    draw.text((460, 385), "Fetch Stored Data & Queries", fill=c_border, font=font_label, anchor="lm")

    # Down-Right: System -> Database
    draw_arrow((360, 340), (455, by_bot))
    draw.text((440, 435), "Save / Update Records", fill=c_border, font=font_label, anchor="lm")

    # Caption at bottom (Split into 2 lines so it never clips)
    c_y = 610
    draw.text((cx, c_y), "Figure 4.1: Level 0 Context Diagram showing Member User, Admin Foreman,", fill="#0F172A", font=font_caption, anchor="mm")
    draw.text((cx, c_y + 18), "Central System, and PostgreSQL Database.", fill="#0F172A", font=font_caption, anchor="mm")

    # Save output with embedded 150 DPI metadata
    out_file = "DFD_Level_0_Word_Fitted.png"
    img.save(out_file, dpi=(150, 150), quality=95)
    print(f"Generated {out_file} (640x720 @ 150 DPI) successfully!")

    # Overwrite DFD_Level_0.png with this perfectly sized version
    img.save("DFD_Level_0.png", dpi=(150, 150), quality=95)
    print("Updated DFD_Level_0.png with Word-fitted version!")

    # Copy to brain artifact directory
    artifact_dir = r"C:\Users\nares\.gemini\antigravity\brain\f74afe5d-2f73-4013-bc1e-3562e05df0f5"
    if os.path.exists(artifact_dir):
        shutil.copy(out_file, os.path.join(artifact_dir, "DFD_Level_0_Word_Fitted.png"))
        shutil.copy("DFD_Level_0.png", os.path.join(artifact_dir, "DFD_Level_0.png"))
        print(f"Copied to artifact dir: {artifact_dir}")

if __name__ == "__main__":
    generate_word_fitted_dfd()

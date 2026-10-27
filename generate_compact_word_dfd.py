import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def generate_compact_word_dfd():
    # Compact canvas designed specifically for A4 Word Document (Width ~850px, Height ~490px)
    width, height = 860, 480
    img = Image.new('RGB', (width, height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Fonts - Bold and highly legible even when scaled down
    try:
        font_caption = ImageFont.truetype("arialbd.ttf", 12)
        font_box_title = ImageFont.truetype("arialbd.ttf", 13)
        font_box_sub = ImageFont.truetype("arial.ttf", 11)
        font_box_entity = ImageFont.truetype("ariali.ttf", 10)
        font_circle_num = ImageFont.truetype("arialbd.ttf", 16)
        font_circle_txt = ImageFont.truetype("arialbd.ttf", 12)
        font_label = ImageFont.truetype("arialbd.ttf", 10)
        font_db_id = ImageFont.truetype("arialbd.ttf", 14)
        font_db_name = ImageFont.truetype("arialbd.ttf", 13)
        font_db_sub = ImageFont.truetype("arial.ttf", 10)
    except:
        font_caption = font_box_title = font_box_sub = font_box_entity = font_circle_num = font_circle_txt = font_label = font_db_id = font_db_name = font_db_sub = ImageFont.load_default()

    c_border = "#0F172A"
    c_fill_box = "#FFFFFF"

    # 1. Central Process Circle: 0.0 SECURECHIT SYSTEM
    cx, cy = 430, 160
    r = 68
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#F8FAFC", outline=c_border, width=2)
    draw.text((cx, cy - 25), "0.0", fill=c_border, font=font_circle_num, anchor="mm")
    draw.text((cx, cy - 5), "SECURE CHIT", fill=c_border, font=font_circle_txt, anchor="mm")
    draw.text((cx, cy + 12), "MANAGEMENT", fill=c_border, font=font_circle_txt, anchor="mm")
    draw.text((cx, cy + 28), "SYSTEM", fill=c_border, font=font_circle_txt, anchor="mm")

    # 2. Left Entity: MEMBER USER
    bx_l, by_l, bw, bh = 20, 120, 160, 80
    draw.rectangle([bx_l, by_l, bx_l + bw, by_l + bh], fill=c_fill_box, outline=c_border, width=2)
    draw.text((bx_l + bw//2, by_l + 24), "USER / SUBSCRIBER", fill=c_border, font=font_box_title, anchor="mm")
    draw.text((bx_l + bw//2, by_l + 44), "(Chit Member)", fill="#334155", font=font_box_sub, anchor="mm")
    draw.text((bx_l + bw//2, by_l + 62), "[External Entity]", fill="#64748B", font=font_box_entity, anchor="mm")

    # 3. Right Entity: ADMIN FOREMAN
    bx_r, by_r = 680, 120
    draw.rectangle([bx_r, by_r, bx_r + bw, by_r + bh], fill=c_fill_box, outline=c_border, width=2)
    draw.text((bx_r + bw//2, by_l + 24), "ADMIN / FOREMAN", fill=c_border, font=font_box_title, anchor="mm")
    draw.text((bx_r + bw//2, by_l + 44), "(Chit Manager)", fill="#334155", font=font_box_sub, anchor="mm")
    draw.text((bx_r + bw//2, by_l + 62), "[External Entity]", fill="#64748B", font=font_box_entity, anchor="mm")

    # 4. Bottom Data Store: POSTGRESQL DATABASE
    db_w, db_h = 280, 60
    bx_db = cx - db_w // 2
    by_db = 320
    draw.rectangle([bx_db, by_db, bx_db + db_w, by_db + db_h], fill=c_fill_box, outline=c_border, width=2)
    # Gane & Sarson ID partition
    div_x = bx_db + 50
    draw.line([(div_x, by_db), (div_x, by_db + db_h)], fill=c_border, width=2)
    draw.text((bx_db + 25, by_db + db_h//2), "D1", fill=c_border, font=font_db_id, anchor="mm")
    draw.text((div_x + (db_w - 50)//2, by_db + 20), "POSTGRESQL DATABASE", fill=c_border, font=font_db_name, anchor="mm")
    draw.text((div_x + (db_w - 50)//2, by_db + 40), "(Central Relational Store)", fill="#475569", font=font_db_sub, anchor="mm")

    # Arrow helper function
    def draw_arrow(start, end, label, label_pos="above", color="#0F172A"):
        x1, y1 = start
        x2, y2 = end
        draw.line([start, end], fill=color, width=2)
        arrow_len = 9
        if x2 > x1 and y1 == y2:   # Right
            draw.polygon([(x2, y2), (x2 - arrow_len, y2 - 4), (x2 - arrow_len, y2 + 4)], fill=color)
        elif x2 < x1 and y1 == y2: # Left
            draw.polygon([(x2, y2), (x2 + arrow_len, y2 - 4), (x2 + arrow_len, y2 + 4)], fill=color)
        elif y2 > y1 and x1 == x2: # Down
            draw.polygon([(x2, y2), (x2 - 4, y2 - arrow_len), (x2 + 4, y2 - arrow_len)], fill=color)
        elif y2 < y1 and x1 == x2: # Up
            draw.polygon([(x2, y2), (x2 - 4, y2 + arrow_len), (x2 + 4, y2 + arrow_len)], fill=color)

        if label:
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            if label_pos == "above":
                draw.text((mx, my - 10), label, fill=color, font=font_label, anchor="mm")
            elif label_pos == "below":
                draw.text((mx, my + 10), label, fill=color, font=font_label, anchor="mm")
            elif label_pos == "left":
                draw.text((mx - 10, my), label, fill=color, font=font_label, anchor="rm")
            elif label_pos == "right":
                draw.text((mx + 10, my), label, fill=color, font=font_label, anchor="lm")

    # Left <--> Center Arrows
    draw_arrow((bx_l + bw, cy - 18), (cx - r, cy - 18), "Chit Application, Bids, UPI UTR", "above")
    draw_arrow((cx - r, cy + 18), (bx_l + bw, cy + 18), "Dynamic Dues, Dividend Statements", "below")

    # Right <--> Center Arrows
    draw_arrow((bx_r, cy - 18), (cx + r, cy - 18), "Scheme Specs, KYC Approvals", "above")
    draw_arrow((cx + r, cy + 18), (bx_r, cy + 18), "Auction Summary, Signed Pronotes", "below")

    # Center <--> Bottom Database Arrows
    draw_arrow((cx - 40, cy + r), (cx - 40, by_db), "Save / Update Records", "left")
    draw_arrow((cx + 40, by_db), (cx + 40, cy + r), "Fetch Stored Data", "right")

    # Caption
    caption = "Figure 4.1: Level 0 Context Diagram showing Member User, Admin Foreman, Central System, and PostgreSQL Database."
    draw.text((cx, 440), caption, fill="#0F172A", font=font_caption, anchor="mm")

    # Save compact image
    out_file = "DFD_Level_0_Word_Compact.png"
    img.save(out_file, quality=95)
    print(f"Generated {out_file} successfully!")

    # Also overwrite the primary DFD_Level_0.png with this compact version so docx generators use it
    img.save("DFD_Level_0.png", quality=95)
    print("Overwrote DFD_Level_0.png with compact Word-friendly version!")

    # Copy to artifact directory
    artifact_dir = r"C:\Users\nares\.gemini\antigravity\brain\f74afe5d-2f73-4013-bc1e-3562e05df0f5"
    if os.path.exists(artifact_dir):
        shutil.copy(out_file, os.path.join(artifact_dir, "DFD_Level_0_Word_Compact.png"))
        shutil.copy("DFD_Level_0.png", os.path.join(artifact_dir, "DFD_Level_0.png"))
        print(f"Copied to artifact dir: {artifact_dir}")

if __name__ == "__main__":
    generate_compact_word_dfd()

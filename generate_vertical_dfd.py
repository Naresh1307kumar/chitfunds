import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def generate_vertical_portrait_dfd():
    # Vertical Portrait Canvas (Width 700, Height 860) - Perfect for Word Portrait A4
    width, height = 700, 860
    img = Image.new('RGB', (width, height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        font_caption = ImageFont.truetype("arialbd.ttf", 13)
        font_box_title = ImageFont.truetype("arialbd.ttf", 14)
        font_box_sub = ImageFont.truetype("arial.ttf", 12)
        font_box_entity = ImageFont.truetype("ariali.ttf", 11)
        font_circle_num = ImageFont.truetype("arialbd.ttf", 18)
        font_circle_txt = ImageFont.truetype("arialbd.ttf", 13)
        font_label = ImageFont.truetype("arialbd.ttf", 11)
        font_db_id = ImageFont.truetype("arialbd.ttf", 15)
        font_db_name = ImageFont.truetype("arialbd.ttf", 13)
        font_db_sub = ImageFont.truetype("arial.ttf", 11)
    except:
        font_caption = font_box_title = font_box_sub = font_box_entity = font_circle_num = font_circle_txt = font_label = font_db_id = font_db_name = font_db_sub = ImageFont.load_default()

    c_border = "#0F172A"
    c_fill_box = "#FFFFFF"

    # Arrow helper
    def draw_arrow(start, end, label, label_pos="above", color="#0F172A"):
        x1, y1 = start
        x2, y2 = end
        draw.line([start, end], fill=color, width=2)
        arrow_len = 10
        if x2 > x1 and y1 == y2:   # Right
            draw.polygon([(x2, y2), (x2 - arrow_len, y2 - 5), (x2 - arrow_len, y2 + 5)], fill=color)
        elif x2 < x1 and y1 == y2: # Left
            draw.polygon([(x2, y2), (x2 + arrow_len, y2 - 5), (x2 + arrow_len, y2 + 5)], fill=color)
        elif y2 > y1 and x1 == x2: # Down
            draw.polygon([(x2, y2), (x2 - 5, y2 - arrow_len), (x2 + 5, y2 - arrow_len)], fill=color)
        elif y2 < y1 and x1 == x2: # Up
            draw.polygon([(x2, y2), (x2 - 5, y2 + arrow_len), (x2 + 5, y2 + arrow_len)], fill=color)

        if label:
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            if label_pos == "above":
                draw.text((mx, my - 12), label, fill=color, font=font_label, anchor="mm")
            elif label_pos == "below":
                draw.text((mx, my + 12), label, fill=color, font=font_label, anchor="mm")
            elif label_pos == "left":
                draw.text((mx - 12, my), label, fill=color, font=font_label, anchor="rm")
            elif label_pos == "right":
                draw.text((mx + 12, my), label, fill=color, font=font_label, anchor="lm")

    # Coordinates
    cx_spine = 440  # Main vertical alignment axis

    # 1. TOP NODE: USER / SUBSCRIBER (Centered along spine)
    top_w, top_h = 240, 85
    bx_top = cx_spine - top_w // 2
    by_top = 45
    draw.rectangle([bx_top, by_top, bx_top + top_w, by_top + top_h], fill=c_fill_box, outline=c_border, width=2)
    draw.text((cx_spine, by_top + 25), "USER / SUBSCRIBER", fill=c_border, font=font_box_title, anchor="mm")
    draw.text((cx_spine, by_top + 47), "(Chit Member)", fill="#334155", font=font_box_sub, anchor="mm")
    draw.text((cx_spine, by_top + 67), "[External Entity]", fill="#64748B", font=font_box_entity, anchor="mm")

    # 2. CENTER NODE: 0.0 SECURE CHIT MANAGEMENT SYSTEM
    cy_center = 370
    r_center = 78
    draw.ellipse([cx_spine - r_center, cy_center - r_center, cx_spine + r_center, cy_center + r_center], 
                 fill="#F8FAFC", outline=c_border, width=2)
    draw.text((cx_spine, cy_center - 28), "0.0", fill=c_border, font=font_circle_num, anchor="mm")
    draw.text((cx_spine, cy_center - 6), "SECURE CHIT", fill=c_border, font=font_circle_txt, anchor="mm")
    draw.text((cx_spine, cy_center + 14), "MANAGEMENT", fill=c_border, font=font_circle_txt, anchor="mm")
    draw.text((cx_spine, cy_center + 32), "SYSTEM", fill=c_border, font=font_circle_txt, anchor="mm")

    # 3. LEFT NODE: ADMIN / CHIT FOREMAN (Aligned to the left of Center Process)
    left_w, left_h = 195, 85
    bx_left = 35
    by_left = cy_center - left_h // 2
    draw.rectangle([bx_left, by_left, bx_left + left_w, by_left + left_h], fill=c_fill_box, outline=c_border, width=2)
    draw.text((bx_left + left_w//2, by_left + 25), "ADMIN / FOREMAN", fill=c_border, font=font_box_title, anchor="mm")
    draw.text((bx_left + left_w//2, by_left + 47), "(Chit Manager)", fill="#334155", font=font_box_sub, anchor="mm")
    draw.text((bx_left + left_w//2, by_left + 67), "[External Entity]", fill="#64748B", font=font_box_entity, anchor="mm")

    # 4. BOTTOM NODE: POSTGRESQL DATABASE (Centered along spine)
    db_w, db_h = 300, 70
    bx_db = cx_spine - db_w // 2
    by_db = 615
    draw.rectangle([bx_db, by_db, bx_db + db_w, by_db + db_h], fill=c_fill_box, outline=c_border, width=2)
    # Gane & Sarson D1 Divider
    div_x = bx_db + 55
    draw.line([(div_x, by_db), (div_x, by_db + db_h)], fill=c_border, width=2)
    draw.text((bx_db + 27, by_db + db_h//2), "D1", fill=c_border, font=font_db_id, anchor="mm")
    draw.text((div_x + (db_w - 55)//2, by_db + 24), "POSTGRESQL DATABASE", fill=c_border, font=font_db_name, anchor="mm")
    draw.text((div_x + (db_w - 55)//2, by_db + 46), "(Central Relational Store)", fill="#475569", font=font_db_sub, anchor="mm")

    # --- ARROWS ---
    # Top <--> Center (Vertical spine arrows)
    draw_arrow((cx_spine - 42, by_top + top_h), (cx_spine - 42, cy_center - r_center), 
               "Chit Application, Bids, UPI UTR", "left")
    draw_arrow((cx_spine + 42, cy_center - r_center), (cx_spine + 42, by_top + top_h), 
               "Due Alerts, Statements, Receipts", "right")

    # Left <--> Center (Horizontal arrows)
    draw_arrow((bx_left + left_w, cy_center - 18), (cx_spine - r_center, cy_center - 18), 
               "Scheme Specs, Approvals", "above")
    draw_arrow((cx_spine - r_center, cy_center + 18), (bx_left + left_w, cy_center + 18), 
               "Reports, Signed Pronotes", "below")

    # Center <--> Bottom (Vertical spine arrows)
    draw_arrow((cx_spine - 45, cy_center + r_center), (cx_spine - 45, by_db), 
               "Save / Update Records", "left")
    draw_arrow((cx_spine + 45, by_db), (cx_spine + 45, cy_center + r_center), 
               "Fetch Stored Data", "right")

    # Caption at bottom
    caption = "Figure 4.1: Level 0 Context Diagram showing Member User, Admin Foreman, Central System, and PostgreSQL Database."
    draw.text((width // 2, 760), caption, fill="#0F172A", font=font_caption, anchor="mm")

    out_file = "DFD_Level_0_Vertical.png"
    img.save(out_file, quality=95)
    print(f"Generated {out_file} successfully!")

    # Also overwrite DFD_Level_0.png
    img.save("DFD_Level_0.png", quality=95)
    print("Updated DFD_Level_0.png!")

    # Copy to brain artifact directory
    artifact_dir = r"C:\Users\nares\.gemini\antigravity\brain\f74afe5d-2f73-4013-bc1e-3562e05df0f5"
    if os.path.exists(artifact_dir):
        shutil.copy(out_file, os.path.join(artifact_dir, "DFD_Level_0_Vertical.png"))
        shutil.copy("DFD_Level_0.png", os.path.join(artifact_dir, "DFD_Level_0.png"))
        print(f"Copied to artifact dir: {artifact_dir}")

if __name__ == "__main__":
    generate_vertical_portrait_dfd()

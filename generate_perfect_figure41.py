import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def draw_datastore_gane_sarson(draw, bbox, store_id, store_name, sub_name, font_bold, font_main, font_sub):
    x1, y1, x2, y2 = bbox
    c_line = "#0F172A"
    c_fill = "#FFFFFF"
    
    # Fill background
    draw.rectangle([x1, y1, x2, y2], fill=c_fill)
    
    # Standard Gane & Sarson DFD Data Store: Top and bottom horizontal lines, closed left end with ID partition
    draw.line([(x1, y1), (x2, y1)], fill=c_line, width=3) # Top border
    draw.line([(x1, y2), (x2, y2)], fill=c_line, width=3) # Bottom border
    draw.line([(x1, y1), (x1, y2)], fill=c_line, width=3) # Left border
    draw.line([(x2, y1), (x2, y2)], fill=c_line, width=3) # Right border (closed box for clear presentation)
    
    div_x = x1 + 65
    draw.line([(div_x, y1), (div_x, y2)], fill=c_line, width=2) # ID divider
    
    cy = (y1 + y2) // 2
    draw.text((x1 + 32, cy), store_id, fill=c_line, font=font_bold, anchor="mm")
    draw.text((div_x + (x2 - div_x)//2, cy - 10), store_name, fill=c_line, font=font_main, anchor="mm")
    draw.text((div_x + (x2 - div_x)//2, cy + 12), sub_name, fill="#475569", font=font_sub, anchor="mm")

def draw_straight_arrow(draw, start, end, label, font, label_pos="above", color="#0F172A"):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=color, width=2)
    
    # Arrowheads
    arrow_len = 11
    if x2 > x1 and y1 == y2:   # Pointing Right
        draw.polygon([(x2, y2), (x2 - arrow_len, y2 - 5), (x2 - arrow_len, y2 + 5)], fill=color)
    elif x2 < x1 and y1 == y2: # Pointing Left
        draw.polygon([(x2, y2), (x2 + arrow_len, y2 - 5), (x2 + arrow_len, y2 + 5)], fill=color)
    elif y2 > y1 and x1 == x2: # Pointing Down
        draw.polygon([(x2, y2), (x2 - 5, y2 - arrow_len), (x2 + 5, y2 - arrow_len)], fill=color)
    elif y2 < y1 and x1 == x2: # Pointing Up
        draw.polygon([(x2, y2), (x2 - 5, y2 + arrow_len), (x2 + 5, y2 + arrow_len)], fill=color)

    if label:
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        if label_pos == "above":
            draw.text((mx, my - 14), label, fill=color, font=font, anchor="mm")
        elif label_pos == "below":
            draw.text((mx, my + 14), label, fill=color, font=font, anchor="mm")
        elif label_pos == "left":
            draw.text((mx - 15, my), label, fill=color, font=font, anchor="rm")
        elif label_pos == "right":
            draw.text((mx + 15, my), label, fill=color, font=font, anchor="lm")

def generate_figure_4_1():
    width, height = 1440, 800
    img = Image.new('RGB', (width, height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    try:
        font_caption = ImageFont.truetype("arialbd.ttf", 17)
        font_box_title = ImageFont.truetype("arialbd.ttf", 15)
        font_box_sub = ImageFont.truetype("arial.ttf", 13)
        font_circle_num = ImageFont.truetype("arialbd.ttf", 19)
        font_circle_txt = ImageFont.truetype("arialbd.ttf", 15)
        font_label = ImageFont.truetype("arial.ttf", 12)
        font_db_id = ImageFont.truetype("arialbd.ttf", 16)
        font_db_name = ImageFont.truetype("arialbd.ttf", 15)
    except:
        font_caption = font_box_title = font_box_sub = font_circle_num = font_circle_txt = font_label = font_db_id = font_db_name = ImageFont.load_default()

    c_border = "#0F172A"
    c_fill_box = "#FFFFFF"

    # 1. Central Process Circle: 0.0 SECURECHIT SYSTEM
    cx, cy = 720, 270
    r = 105
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#F8FAFC", outline=c_border, width=3)
    draw.text((cx, cy - 36), "0.0", fill=c_border, font=font_circle_num, anchor="mm")
    draw.text((cx, cy - 10), "SECURE CHIT", fill=c_border, font=font_circle_txt, anchor="mm")
    draw.text((cx, cy + 14), "MANAGEMENT", fill=c_border, font=font_circle_txt, anchor="mm")
    draw.text((cx, cy + 38), "SYSTEM", fill=c_border, font=font_circle_txt, anchor="mm")

    # 2. Left Entity: MEMBER USER
    bx_l, by_l, bw, bh = 70, 220, 220, 100
    draw.rectangle([bx_l, by_l, bx_l + bw, by_l + bh], fill=c_fill_box, outline=c_border, width=3)
    draw.text((bx_l + bw//2, by_l + 32), "USER / SUBSCRIBER", fill=c_border, font=font_box_title, anchor="mm")
    draw.text((bx_l + bw//2, by_l + 56), "(Chit Member)", fill="#475569", font=font_box_sub, anchor="mm")
    draw.text((bx_l + bw//2, by_l + 76), "[External Entity]", fill="#64748B", font=font_label, anchor="mm")

    # 3. Right Entity: ADMIN FOREMAN
    bx_r, by_r = 1150, 220
    draw.rectangle([bx_r, by_r, bx_r + bw, by_r + bh], fill=c_fill_box, outline=c_border, width=3)
    draw.text((bx_r + bw//2, by_l + 32), "ADMIN / CHIT FOREMAN", fill=c_border, font=font_box_title, anchor="mm")
    draw.text((bx_r + bw//2, by_l + 56), "(Chit Manager)", fill="#475569", font=font_box_sub, anchor="mm")
    draw.text((bx_r + bw//2, by_l + 76), "[External Entity]", fill="#64748B", font=font_label, anchor="mm")

    # 4. Bottom Data Store: POSTGRESQL DATABASE
    db_w, db_h = 380, 80
    bx_db = cx - db_w // 2
    by_db = 530
    draw_datastore_gane_sarson(draw, [bx_db, by_db, bx_db + db_w, by_db + db_h], "D1", "POSTGRESQL DATABASE", "(Central Relational Store)", font_db_id, font_db_name, font_label)

    # 5. Connect Left Entity <--> Center Circle (Horizontal straight arrows)
    arrow_y_top = cy - 25
    arrow_y_bot = cy + 25

    # Top: Member -> System (pointing right)
    draw_straight_arrow(draw, (bx_l + bw, arrow_y_top), (cx - r, arrow_y_top), 
                        "Chit Application, Bids, Receipts, UPI UTR", font_label, "above")
    # Bottom: System -> Member (pointing left)
    draw_straight_arrow(draw, (cx - r, arrow_y_bot), (bx_l + bw, arrow_y_bot), 
                        "Dynamic Dues, Dividend Statements, Receipts", font_label, "below")

    # 6. Connect Right Entity <--> Center Circle (Horizontal straight arrows)
    # Top: Admin -> System (pointing left)
    draw_straight_arrow(draw, (bx_r, arrow_y_top), (cx + r, arrow_y_top), 
                        "Scheme Specs, Member Approvals, Verifications", font_label, "above")
    # Bottom: System -> Admin (pointing right)
    draw_straight_arrow(draw, (cx + r, arrow_y_bot), (bx_r, arrow_y_bot), 
                        "Pending Requests, Auction Summary, Reports", font_label, "below")

    # 7. Connect Center Circle <--> PostgreSQL Database (Vertical straight arrows)
    arrow_x_left = cx - 55
    arrow_x_right = cx + 55

    # Left: System -> Database (pointing down)
    draw_straight_arrow(draw, (arrow_x_left, cy + r), (arrow_x_left, by_db), 
                        "Save / Update Records", font_label, "left")
    # Right: Database -> System (pointing up)
    draw_straight_arrow(draw, (arrow_x_right, by_db), (arrow_x_right, cy + r), 
                        "Fetch Stored Data & Queries", font_label, "right")

    # Caption exactly as requested
    caption_text = "Figure 4.1: Level 0 Context Diagram showing Member User, Admin Foreman, Central System, and PostgreSQL Database."
    draw.text((cx, 715), caption_text, fill="#0F172A", font=font_caption, anchor="mm")

    # Save output files
    out_file = "DFD_Level_0_Figure_4_1.png"
    img.save(out_file, quality=95)
    print(f"Generated {out_file} successfully!")

    # Also overwrite DFD_Level_0.png in the project root
    img.save("DFD_Level_0.png", quality=95)
    print("Updated DFD_Level_0.png with clean version!")

    # Copy to brain artifact directory
    artifact_dir = r"C:\Users\nares\.gemini\antigravity\brain\f74afe5d-2f73-4013-bc1e-3562e05df0f5"
    if os.path.exists(artifact_dir):
        shutil.copy(out_file, os.path.join(artifact_dir, "DFD_Level_0_Figure_4_1.png"))
        shutil.copy("DFD_Level_0.png", os.path.join(artifact_dir, "DFD_Level_0.png"))
        print(f"Copied to artifact dir: {artifact_dir}")

if __name__ == "__main__":
    generate_figure_4_1()

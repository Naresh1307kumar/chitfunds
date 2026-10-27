import os
import shutil
import math
from PIL import Image, ImageDraw, ImageFont

def create_level0_diagram():
    # Canvas with plenty of breathing room
    width, height = 1300, 850
    img = Image.new('RGB', (width, height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        font_caption = ImageFont.truetype("arialbd.ttf", 20)
        font_box = ImageFont.truetype("arialbd.ttf", 16)
        font_label = ImageFont.truetype("arial.ttf", 13)
        font_circle_num = ImageFont.truetype("arialbd.ttf", 19)
        font_circle_txt = ImageFont.truetype("arialbd.ttf", 16)
    except:
        font_caption = font_box = font_label = font_circle_num = font_circle_txt = ImageFont.load_default()

    # Colors
    c_box = "#0B132B"           # Deep Navy / Black
    c_circle_stroke = "#4F46E5" # Indigo Blue
    c_circle_fill = "#F4F6FF"   # Soft light pastel
    c_circle_text = "#0B132B"
    c_arrow = "#1E293B"
    c_text = "#1E293B"

    # 1. Center Circle (0.0 SECURECHIT DIGITAL CHIT FUND SYSTEM)
    cx, cy = 650, 360
    r = 110
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c_circle_fill, outline=c_circle_stroke, width=4)
    
    draw.text((cx, cy - 42), "0.0", fill=c_circle_text, font=font_circle_num, anchor="mm")
    draw.text((cx, cy - 14), "SECURECHIT", fill=c_circle_text, font=font_circle_txt, anchor="mm")
    draw.text((cx, cy + 12), "CHIT FUND", fill=c_circle_text, font=font_circle_txt, anchor="mm")
    draw.text((cx, cy + 38), "SYSTEM", fill=c_circle_text, font=font_circle_txt, anchor="mm")

    # 2. Left Box: MEMBER (SUBSCRIBER)
    bw, bh = 190, 85
    bx_left, by_left = 70, 317
    draw.rectangle([bx_left, by_left, bx_left + bw, by_left + bh], fill=c_box)
    draw.text((bx_left + bw//2, by_left + bh//2 - 13), "MEMBER", fill="#FFFFFF", font=font_box, anchor="mm")
    draw.text((bx_left + bw//2, by_left + bh//2 + 13), "(SUBSCRIBER)", fill="#FFFFFF", font=font_box, anchor="mm")

    # 3. Right Box: CHIT FOREMAN (MANAGER)
    bx_right, by_right = 1040, 317
    draw.rectangle([bx_right, by_right, bx_right + bw, by_right + bh], fill=c_box)
    draw.text((bx_right + bw//2, by_right + bh//2 - 13), "CHIT FOREMAN", fill="#FFFFFF", font=font_box, anchor="mm")
    draw.text((bx_right + bw//2, by_right + bh//2 + 13), "(MANAGER)", fill="#FFFFFF", font=font_box, anchor="mm")

    # 4. Bottom Box: ADMINISTRATOR
    bx_bot, by_bot = 545, 640
    bw_bot = 210
    draw.rectangle([bx_bot, by_bot, bx_bot + bw_bot, by_bot + bh], fill=c_box)
    draw.text((bx_bot + bw_bot//2, by_bot + bh//2), "ADMINISTRATOR", fill="#FFFFFF", font=font_box, anchor="mm")

    # Arrow helper
    def draw_arrow(start, end, label, label_offset=(0, -18), align="center"):
        x1, y1 = start
        x2, y2 = end
        draw.line([start, end], fill=c_arrow, width=2)
        
        # Arrowhead
        angle = math.atan2(y2 - y1, x2 - x1)
        arrow_len = 11
        p1 = (x2 - arrow_len * math.cos(angle - math.pi/6), y2 - arrow_len * math.sin(angle - math.pi/6))
        p2 = (x2 - arrow_len * math.cos(angle + math.pi/6), y2 - arrow_len * math.sin(angle + math.pi/6))
        draw.polygon([(x2, y2), p1, p2], fill=c_arrow)

        # Label drawing
        if label:
            mx = (x1 + x2) / 2 + label_offset[0]
            my = (y1 + y2) / 2 + label_offset[1]
            lines = label.split("\n")
            line_height = 16
            start_y = my - ((len(lines) - 1) * line_height) / 2
            for i, line in enumerate(lines):
                cur_y = start_y + i * line_height
                if align == "center":
                    draw.text((mx, cur_y), line, fill=c_text, font=font_label, anchor="mm")
                elif align == "right":
                    draw.text((mx, cur_y), line, fill=c_text, font=font_label, anchor="rm")
                elif align == "left":
                    draw.text((mx, cur_y), line, fill=c_text, font=font_label, anchor="lm")

    # Connect Left Box <--> Center Circle
    # Top arrow: Member -> Circle (pointing right)
    arrow_y_top = cy - 24
    draw_arrow((bx_left + bw, arrow_y_top), (cx - r, arrow_y_top), 
               "Registration, search chits,\nbidding, 12-digit UTR", label_offset=(0, -22), align="center")

    # Bottom arrow: Circle -> Member (pointing left)
    arrow_y_bot = cy + 24
    draw_arrow((cx - r, arrow_y_bot), (bx_left + bw, arrow_y_bot), 
               "Due details, dividend alerts,\nverified receipts", label_offset=(0, 22), align="center")

    # Connect Right Box <--> Center Circle
    # Top arrow: Foreman -> Circle (pointing left)
    draw_arrow((bx_right, arrow_y_top), (cx + r, arrow_y_top), 
               "Scheme setup, auction conduct,\npronote generation", label_offset=(0, -22), align="center")

    # Bottom arrow: Circle -> Foreman (pointing right)
    draw_arrow((cx + r, arrow_y_bot), (bx_right, arrow_y_bot), 
               "Active bidding pool, UTR notices,\n5% commission", label_offset=(0, 22), align="center")

    # Connect Center Circle <--> Bottom Box (Administrator)
    # Left arrow: Administrator -> Circle (pointing up)
    arrow_x_left = cx - 45
    draw_arrow((arrow_x_left, by_bot), (arrow_x_left, cy + r), 
               "Login, KYC approvals,\npayment verifications", label_offset=(-18, 0), align="right")

    # Right arrow: Circle -> Administrator (pointing down)
    arrow_x_right = cx + 45
    draw_arrow((arrow_x_right, cy + r), (arrow_x_right, by_bot), 
               "System analytics, KYC audits,\npayment ledger", label_offset=(18, 0), align="left")

    # Figure Caption
    draw.text((cx, 785), "Figure 4.2: Level 0 DFD (Context Diagram)", fill="#0B132B", font=font_caption, anchor="mm")

    # Save output
    out_path = "DFD_Level_0_Context.png"
    img.save(out_path, quality=95)
    print(f"Saved: {out_path}")

    # Copy to brain artifact directory
    artifact_dir = r"C:\Users\nares\.gemini\antigravity\brain\f74afe5d-2f73-4013-bc1e-3562e05df0f5"
    if os.path.exists(artifact_dir):
        shutil.copy(out_path, os.path.join(artifact_dir, "DFD_Level_0_Context.png"))
        print(f"Copied to artifact dir: {artifact_dir}")

if __name__ == "__main__":
    create_level0_diagram()

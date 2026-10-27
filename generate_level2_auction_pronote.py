import os
import shutil
import math
from PIL import Image, ImageDraw, ImageFont

def generate_level2_auction_pronote():
    # 700 x 960 px @ 150 DPI — fits A4 portrait Word page cleanly
    width, height = 700, 960
    img = Image.new('RGB', (width, height), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    # Fonts
    try:
        font_caption  = ImageFont.truetype("arialbd.ttf", 12)
        font_entity   = ImageFont.truetype("arialbd.ttf", 11)
        font_proc_num = ImageFont.truetype("arialbd.ttf", 11)
        font_proc_lbl = ImageFont.truetype("arialbd.ttf", 10)
        font_store    = ImageFont.truetype("arialbd.ttf", 10)
        font_label    = ImageFont.truetype("arial.ttf",   9)
    except:
        font_caption = font_entity = font_proc_num = font_proc_lbl = font_store = font_label = ImageFont.load_default()

    # Design tokens
    C_NAVY   = "#0B132B"
    C_WHITE  = "#FFFFFF"
    C_BLUE   = "#4F46E5"
    C_BFILL  = "#EEF2FF"
    C_GREEN  = "#0D9488"
    C_GFILL  = "#F0FDFA"
    C_SLATE  = "#475569"
    C_SFILL  = "#F8FAFC"
    C_AMBER  = "#D97706"
    C_AFILL  = "#FEF3C7"
    C_ARROW  = "#1E293B"
    C_LBL    = "#1E293B"

    # Layout constants
    x_left_entity   = 18
    w_entity         = 115
    x_proc_cx        = 360      # center of process oval column
    w_proc, h_proc   = 160, 50
    x_store          = 540
    w_store, h_store = 135, 40

    # Y positions for 8 sub-processes
    y_procs = [65, 170, 275, 380, 475, 575, 675, 770]

    # ── helpers ──────────────────────────────────────────────────────────────

    def oval(cy, num, lbl, fill, border):
        rx, ry = w_proc // 2, h_proc // 2
        draw.ellipse([x_proc_cx - rx, cy - ry, x_proc_cx + rx, cy + ry],
                     fill=fill, outline=border, width=2)
        draw.text((x_proc_cx, cy - 8), num, fill=C_NAVY, font=font_proc_num, anchor="mm")
        draw.text((x_proc_cx, cy + 9), lbl, fill=C_NAVY, font=font_proc_lbl, anchor="mm")

    def entity(y, h, lines):
        draw.rectangle([x_left_entity, y, x_left_entity + w_entity, y + h], fill=C_NAVY)
        lh, sy = 14, y + h // 2 - (len(lines) - 1) * 7
        for i, ln in enumerate(lines):
            draw.text((x_left_entity + w_entity // 2, sy + i * lh),
                      ln, fill=C_WHITE, font=font_entity, anchor="mm")

    def store(y, name, fill=C_SFILL, border=C_SLATE):
        draw.rectangle([x_store, y, x_store + w_store, y + h_store],
                       fill=fill, outline=border, width=2)
        draw.line([(x_store + 12, y), (x_store + 12, y + h_store)], fill=border, width=2)
        draw.text((x_store + 12 + (w_store - 12) // 2, y + h_store // 2),
                  name, fill=C_NAVY, font=font_store, anchor="mm")

    def arrow(start, end):
        x1, y1 = start; x2, y2 = end
        draw.line([start, end], fill=C_ARROW, width=2)
        angle = math.atan2(y2 - y1, x2 - x1)
        al = 9
        p1 = (x2 - al * math.cos(angle - math.pi/6), y2 - al * math.sin(angle - math.pi/6))
        p2 = (x2 - al * math.cos(angle + math.pi/6), y2 - al * math.sin(angle + math.pi/6))
        draw.polygon([(x2, y2), p1, p2], fill=C_ARROW)

    def lbl_right(x, y, txt):
        draw.text((x, y), txt, fill=C_LBL, font=font_label, anchor="lm")

    def lbl_left(x, y, txt):
        draw.text((x, y), txt, fill=C_LBL, font=font_label, anchor="rm")

    # ── SECTION DIVIDER: dashed separator between Auction and Pronote ─────────
    div_y = 527
    for dx in range(x_left_entity, x_store + w_store, 12):
        draw.line([(dx, div_y), (dx + 7, div_y)], fill="#CBD5E1", width=1)
    draw.text((width // 2, div_y - 10), "── AUCTION BIDDING SECTION ──",
              fill="#94A3B8", font=font_label, anchor="mm")
    draw.text((width // 2, div_y + 10), "── PRONOTE EXECUTION SECTION ──",
              fill="#94A3B8", font=font_label, anchor="mm")

    # ── PROCESSES ─────────────────────────────────────────────────────────────

    # Auction section (blue/indigo)
    oval(y_procs[0], "3.1", "Submit Bid & Emergency Rank",      C_BFILL, C_BLUE)
    oval(y_procs[1], "3.2", "Validate & Record Bid",            C_BFILL, C_BLUE)
    oval(y_procs[2], "3.3", "AI Priority Engine (Rank 1–5)",    C_BFILL, C_BLUE)
    oval(y_procs[3], "3.4", "Select Auction Winner",            C_BFILL, C_BLUE)
    oval(y_procs[4], "3.5", "Calculate Dividend Distribution",  C_BFILL, C_BLUE)

    # Pronote section (green/teal)
    oval(y_procs[5], "4.1", "Auto-Generate Pronote (PRN)",      C_GFILL, C_GREEN)
    oval(y_procs[6], "4.2", "Canvas Signature Capture",         C_GFILL, C_GREEN)
    oval(y_procs[7], "4.3", "PDF Compile & Store Signed PRN",   C_GFILL, C_GREEN)

    # ── DATA STORES ───────────────────────────────────────────────────────────
    store(y_procs[0] - h_store // 2, "plan_members")
    store(y_procs[1] - h_store // 2, "draws")
    store(y_procs[2] - h_store // 2, "emergency_ranks")
    store(y_procs[3] - h_store // 2, "monthly_draws")
    store(y_procs[4] - h_store // 2, "installments", fill=C_AFILL, border=C_AMBER)
    store(y_procs[5] - h_store // 2, "promissory_notes", fill=C_GFILL, border=C_GREEN)
    store(y_procs[6] - h_store // 2, "users")
    store(y_procs[7] - h_store // 2, "promissory_notes", fill=C_GFILL, border=C_GREEN)

    # Process → Store arrows (right side)
    rx = w_proc // 2
    for i in range(8):
        arrow((x_proc_cx + rx, y_procs[i]), (x_store, y_procs[i]))

    # ── EXTERNAL ENTITIES ────────────────────────────────────────────────────
    y_member  = 165;  h_member  = 55
    y_foreman = 445;  h_foreman = 55
    y_member2 = 665;  h_member2 = 55   # Member signs pronote

    entity(y_member,  h_member,  ["MEMBER",      "(SUBSCRIBER)"])
    entity(y_foreman, h_foreman, ["CHIT FOREMAN", "(MANAGER)"])
    entity(y_member2, h_member2, ["MEMBER",      "(SUBSCRIBER)"])

    right_e = x_left_entity + w_entity

    # ── ENTITY → PROCESS ARROWS (left side) ──────────────────────────────────
    # Member -> 3.1  bid amount + emergency rank
    arrow((right_e, y_member + 15), (x_proc_cx - rx, y_procs[0] + 10))
    lbl_left(right_e + 4, y_member - 4, "bid amount & emergency rank")

    # Member -> 3.2 (submit)
    arrow((right_e, y_member + 35), (x_proc_cx - rx, y_procs[1]))
    lbl_left(right_e + 4, y_member + 42, "submit bid request")

    # Foreman -> 3.4 conduct draw
    arrow((right_e, y_foreman + 18), (x_proc_cx - rx, y_procs[3]))
    lbl_left(right_e + 4, y_foreman + 6, "conduct draw")

    # Foreman -> 3.5 approve dividend
    arrow((right_e, y_foreman + 40), (x_proc_cx - rx, y_procs[4] + 10))
    lbl_left(right_e + 4, y_foreman + 46, "approve distribution")

    # Member2 -> 4.2 sign pronote (canvas)
    arrow((right_e, y_member2 + 27), (x_proc_cx - rx, y_procs[6]))
    lbl_left(right_e + 4, y_member2 + 10, "canvas signature (Base64)")

    # ── INTER-PROCESS ARROWS (vertical flow) ─────────────────────────────────
    # 3.1 -> 3.2
    arrow((x_proc_cx, y_procs[0] + h_proc // 2), (x_proc_cx, y_procs[1] - h_proc // 2))
    lbl_right(x_proc_cx + 6, (y_procs[0] + y_procs[1]) // 2, "validated bids")

    # 3.2 -> 3.3
    arrow((x_proc_cx, y_procs[1] + h_proc // 2), (x_proc_cx, y_procs[2] - h_proc // 2))
    lbl_right(x_proc_cx + 6, (y_procs[1] + y_procs[2]) // 2, "ranked bid list")

    # 3.3 -> 3.4
    arrow((x_proc_cx, y_procs[2] + h_proc // 2), (x_proc_cx, y_procs[3] - h_proc // 2))
    lbl_right(x_proc_cx + 6, (y_procs[2] + y_procs[3]) // 2, "priority winner ID")

    # 3.4 -> 3.5
    arrow((x_proc_cx, y_procs[3] + h_proc // 2), (x_proc_cx, y_procs[4] - h_proc // 2))
    lbl_right(x_proc_cx + 6, (y_procs[3] + y_procs[4]) // 2, "discount & 5% commission")

    # 3.5 -> 4.1
    arrow((x_proc_cx, y_procs[4] + h_proc // 2), (x_proc_cx, y_procs[5] - h_proc // 2))
    lbl_right(x_proc_cx + 6, (y_procs[4] + y_procs[5]) // 2, "winner & net payable")

    # 4.1 -> 4.2
    arrow((x_proc_cx, y_procs[5] + h_proc // 2), (x_proc_cx, y_procs[6] - h_proc // 2))
    lbl_right(x_proc_cx + 6, (y_procs[5] + y_procs[6]) // 2, "pending PRN-2026-XXXX")

    # 4.2 -> 4.3
    arrow((x_proc_cx, y_procs[6] + h_proc // 2), (x_proc_cx, y_procs[7] - h_proc // 2))
    lbl_right(x_proc_cx + 6, (y_procs[6] + y_procs[7]) // 2, "signed PRN (Base64 PNG)")

    # ── CAPTION ───────────────────────────────────────────────────────────────
    draw.text((width // 2, 912),
              "Figure 4.5: Level 2 DFD – Auction Bidding & Pronote Workflow",
              fill=C_NAVY, font=font_caption, anchor="mm")

    # ── SAVE ──────────────────────────────────────────────────────────────────
    out_file = "DFD_Level_2_Auction_Pronote.png"
    img.save(out_file, dpi=(150, 150), quality=95)
    print(f"Generated {out_file}")

    artifact_dir = r"C:\Users\nares\.gemini\antigravity\brain\f74afe5d-2f73-4013-bc1e-3562e05df0f5"
    if os.path.exists(artifact_dir):
        shutil.copy(out_file, os.path.join(artifact_dir, out_file))
        print(f"Copied to artifact dir")

if __name__ == "__main__":
    generate_level2_auction_pronote()

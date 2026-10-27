import os
from PIL import Image, ImageDraw, ImageFont

def generate_thiagarajar_logo():
    # 500x500 high resolution circular college seal/logo
    size = (600, 600)
    img = Image.new('RGBA', size, (255, 255, 255, 0)) # Transparent background
    draw = ImageDraw.Draw(img)
    
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 26)
        font_bold = ImageFont.truetype("arialbd.ttf", 20)
        font_small = ImageFont.truetype("arialbd.ttf", 16)
        font_motto = ImageFont.truetype("georgiai.ttf", 18)
    except:
        font_title = font_bold = font_small = font_motto = ImageFont.load_default()

    c_navy = "#103C58"
    c_gold = "#D97706"
    c_dark_gold = "#B45309"
    c_bg = "#F0F9FF"
    c_white = "#FFFFFF"

    # Outer Double Ring
    draw.ellipse([20, 20, 580, 580], fill=c_navy, outline=c_gold, width=8)
    draw.ellipse([50, 50, 550, 550], fill=c_bg, outline=c_gold, width=4)

    # Inner Shield / Circle
    draw.ellipse([110, 110, 490, 490], fill=c_white, outline=c_navy, width=5)

    # Outer Ring Curved Text (Simulated cleanly with text calls)
    draw.text((300, 60), "THIAGARAJAR COLLEGE", fill=c_white, font=font_title, anchor="mt")
    draw.text((300, 535), "(AUTONOMOUS) - MADURAI", fill=c_gold, font=font_bold, anchor="mb")

    # Center Emblem Elements:
    # 1. Rising Sun / Rays in upper half of inner circle
    for angle in range(-60, 61, 15):
        import math
        rad = math.radians(angle - 90)
        rx = 300 + 130 * math.cos(rad)
        ry = 300 + 130 * math.sin(rad)
        draw.line([(300, 280), (rx, ry)], fill="#FDE047", width=3)

    # 2. Open Book symbol at center
    draw.rectangle([210, 310, 390, 370], fill="#FEF08A", outline=c_navy, width=3)
    draw.line([(300, 310), (300, 370)], fill=c_navy, width=3)
    draw.text((255, 340), "WISDOM", fill=c_navy, font=font_small, anchor="mm")
    draw.text((345, 340), "SERVICE", fill=c_navy, font=font_small, anchor="mm")

    # 3. Traditional Lamp / Flame (Kuthu Vilakku) top of book
    draw.polygon([(300, 230), (285, 270), (315, 270)], fill="#EF4444", outline="#B91C1C")
    draw.ellipse([290, 260, 310, 280], fill="#F59E0B")
    draw.rectangle([292, 280, 308, 310], fill=c_gold, outline=c_dark_gold)

    # Motto Ribbon at bottom of inner circle
    draw.rectangle([160, 395, 440, 435], fill=c_navy, outline=c_gold, width=2)
    draw.text((300, 415), "KARMA | BHAKTI | JANA", fill=c_white, font=font_small, anchor="mm")

    # NAAC 'A++' Banner below logo
    draw.text((300, 460), "NAAC 'A++' GRADE | NIRF 20th", fill=c_navy, font=font_bold, anchor="mm")

    img.save("thiagarajar_college_logo.png")
    print("Saved thiagarajar_college_logo.png")

if __name__ == "__main__":
    generate_thiagarajar_logo()

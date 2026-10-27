import re

filepath = r"C:\Users\nares\.gemini\antigravity\brain\f3eb3d7a-3368-4f7d-ad6c-f8c0de697e83\.system_generated\steps\6541\content.md"
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

imgs = re.findall(r'src=["\']([^"\']+)["\']', text, re.IGNORECASE)
for img in imgs:
    if 'logo' in img.lower() or 'header' in img.lower() or 'banner' in img.lower() or 'icon' in img.lower():
        print("LOGO / HEADER MATCH:", img)
    elif img.endswith('.png') or img.endswith('.jpg') or img.endswith('.svg') or img.endswith('.webp'):
        print("IMAGE:", img)

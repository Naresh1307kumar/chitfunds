import shutil
import os

src_file = r"C:\Users\nares\.gemini\antigravity\brain\f3eb3d7a-3368-4f7d-ad6c-f8c0de697e83\.user_uploaded\media__1786102502817.png"
dst_dir = r"c:\chit fund\frontend\public\images"
dst_file = os.path.join(dst_dir, "naresh_gpay_qr.png")

os.makedirs(dst_dir, exist_ok=True)
if os.path.exists(src_file):
    shutil.copy(src_file, dst_file)
    print(f"[SUCCESS] Successfully copied EXACT cropped GPay QR image (media__1786102502817.png) to {dst_file}")
else:
    print(f"[ERROR] {src_file} does not exist!")

import shutil
import os

src_file = r"C:\Users\nares\.gemini\antigravity\brain\f3eb3d7a-3368-4f7d-ad6c-f8c0de697e83\.user_uploaded\media__1785468769530.png"
dst_dir = r"c:\chit fund\frontend\public\images"
dst_file = os.path.join(dst_dir, "naresh_gpay_qr.png")

os.makedirs(dst_dir, exist_ok=True)
shutil.copy(src_file, dst_file)
print(f"[SUCCESS] Copied user GPay QR image to {dst_file}")

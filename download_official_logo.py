import urllib.request
import os
from PIL import Image

urls = [
    "https://tcarts.in/images/logo.jpg",
    "https://tcarts.in/logo.png",
    "https://tcarts.in/newsite/logo.jpg",
    "https://tcarts.in/images/mgmt/chettiar1.png",
    "https://tcarts.in/css/images/logo.png"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for i, url in enumerate(urls):
    try:
        req = urllib.request.Request(url, headers=headers)
        filename = f"college_logo_downloaded_{i}.png"
        with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
            print(f"Downloaded {url} ({len(data)} bytes) -> {filename}")
            try:
                img = Image.open(filename)
                print(f"  Format: {img.format}, Size: {img.size}")
            except Exception as e:
                print(f"  Image open error: {e}")
    except Exception as e:
        print(f"Failed {url}: {e}")

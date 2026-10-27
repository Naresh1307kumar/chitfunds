import urllib.request
import base64
import zlib

def generate_mermaid(mermaid_code):
    compressed = zlib.compress(mermaid_code.encode('utf-8'), 9)
    b64 = base64.urlsafe_b64encode(compressed).decode('ascii')
    url = f"https://kroki.io/mermaid/png/{b64}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            return response.read()
    except Exception as e:
        print(f"Error: {e}")
        return None

code = "flowchart TD\nA-->B"
img = generate_mermaid(code)
if img:
    print("Success, downloaded", len(img), "bytes")
else:
    print("Failed")

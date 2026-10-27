import re
import os

# 1. Update App.jsx
app_path = r'c:\chit fund\frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    app = f.read()
app = app.replace('Professional Financial Management', 'Professional Chit Fund Management')
with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app)

# 2. Update AdminLogin.jsx
al_path = r'c:\chit fund\frontend\src\pages\public\AdminLogin.jsx'
with open(al_path, 'r', encoding='utf-8') as f:
    al = f.read()

if 'Member? <Link' not in al:
    replacement = """</button>
            <div className="text-center mt-6 text-sm text-slate-500">
              Member? <Link to="/login" className="text-corpBlue font-bold hover:underline">Login here</Link>
            </div>"""
    al = re.sub(r'</button>\s*</form>', replacement + '\n          </form>', al)
    with open(al_path, 'w', encoding='utf-8') as f:
        f.write(al)

# 3. Strip old navs
for path in [r'c:\chit fund\frontend\src\pages\member\Dashboard.jsx', r'c:\chit fund\frontend\src\pages\admin\Dashboard.jsx']:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Try exact match first
    new_content = re.sub(r'\{/\*\s*Navbar\s*\*/\}\s*<nav.*?</nav>', '', content, flags=re.DOTALL)
    
    # If it failed, try matching <nav ... </nav> explicitly
    new_content = re.sub(r'<nav\b[^>]*>.*?</nav>', '', new_content, flags=re.DOTALL)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

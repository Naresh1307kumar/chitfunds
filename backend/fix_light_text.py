with open('../frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Rules text color
content = content.replace(
    'className="text-white text-base md:text-lg leading-relaxed"',
    'className="text-slate-800 text-base md:text-lg leading-relaxed"'
)

# Fix Feature title text color
content = content.replace(
    'className="text-xl font-bold text-white mb-3 tracking-wide"',
    'className="text-xl font-bold text-slate-800 mb-3 tracking-wide"'
)

# Fix Plan name text color
content = content.replace(
    'className="text-2xl font-bold text-white mb-2"',
    'className="text-2xl font-bold text-slate-800 mb-2"'
)

# Fix Plan detail features text color
content = content.replace(
    'className="space-y-5 mb-10 text-white"',
    'className="space-y-5 mb-10 text-slate-700"'
)

# Fix View Details button text color
content = content.replace(
    'className="w-full py-3 rounded font-bold transition-colors bg-cardBg text-white border border-cardBorder hover:bg-bgAlt1"',
    'className="w-full py-3 rounded font-bold transition-colors bg-cardBg text-slate-700 border border-cardBorder hover:bg-bgAlt1"'
)

# Fix AboutUs points title text color
content = content.replace(
    'className="text-lg font-bold text-white mb-2"',
    'className="text-lg font-bold text-slate-800 mb-2"'
)

# Fix Contact card headings text color
content = content.replace(
    'className="font-bold text-lg mb-1 text-white tracking-wide"',
    'className="font-bold text-lg mb-1 text-slate-800 tracking-wide"'
)

# Fix Testimonials author text color
content = content.replace(
    'className="font-bold text-base text-white tracking-wide"',
    'className="font-bold text-base text-slate-800 tracking-wide"'
)

# Fix Stats value text color
content = content.replace(
    'className="text-3xl font-bold text-white mb-2"',
    'className="text-3xl font-bold text-slate-900 mb-2"'
)

with open('../frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Light theme text colors successfully restored in App.jsx!")

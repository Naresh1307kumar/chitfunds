# Read App.jsx
with open('../frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    app_content = f.read()

# 1. Update LandingPage layout wrapper to Light theme
app_content = app_content.replace(
    'className="min-h-screen flex flex-col font-sans bg-slate-950 text-slate-100 relative"',
    'className="min-h-screen flex flex-col font-sans bg-[#F8FAFC] text-slate-800 relative"'
)

# 2. Update background pattern overlay opacity for light background
app_content = app_content.replace(
    'opacity: 0.12,',
    'opacity: 0.04,'
)

# 3. Modify Navbar back to a premium light blur navbar
old_navbar = """  return (
    <nav className="fixed w-full z-50 top-0 transition-all duration-300 bg-slate-950/80 backdrop-blur-md py-4 shadow-md border-b border-slate-800/50">"""

new_navbar = """  return (
    <nav className={`fixed w-full z-50 top-0 transition-all duration-300 ${scrolled ? 'bg-white/95 backdrop-blur-md py-4 shadow-md border-b border-slate-200/60' : 'bg-transparent py-6 border-b border-transparent'}`}>"""

app_content = app_content.replace(old_navbar, new_navbar)

# Restore Navbar details
app_content = app_content.replace('text-corpGold', 'text-corpBlue')
app_content = app_content.replace('text-white tracking-tight', 'text-corpNavy tracking-tight')
app_content = app_content.replace('text-slate-300 hover:text-corpGold', 'text-slate-600 hover:text-corpBlue')
app_content = app_content.replace(
    'className="py-3 px-8 text-base font-bold inline-block text-center shadow-lg bg-corpGold hover:bg-yellow-500 text-slate-950 rounded-md transition-all"',
    'className="btn-primary py-3 px-8 text-base font-bold inline-block text-center shadow-lg"'
)
app_content = app_content.replace('text-slate-300 hover:text-white', 'text-slate-600 hover:text-corpBlue')
app_content = app_content.replace('bg-corpNavy mt-4 border-t border-slate-800 shadow-xl absolute w-full', 'bg-white mt-4 border-t border-slate-200 shadow-xl absolute w-full')
app_content = app_content.replace('text-slate-300 hover:text-white hover:bg-slate-800', 'text-slate-600 hover:text-corpBlue hover:bg-slate-50')
app_content = app_content.replace('bg-corpGold text-slate-950 font-bold rounded-md', 'btn-primary text-white')

# 4. Restore headings and text styles in App.jsx to fit the light theme
app_content = app_content.replace("text-white mb-6 tracking-tight leading-tight", "text-corpNavy mb-6 tracking-tight leading-tight")
# Replace any remaining text-white headings
app_content = app_content.replace('className="text-4xl md:text-5xl font-bold text-white mb-6 tracking-tight"', 'className="text-4xl md:text-5xl font-bold text-corpNavy mb-6 tracking-tight"')
app_content = app_content.replace('text-slate-300', 'text-corpTextLight')
app_content = app_content.replace('bg-slate-900/60', 'bg-bgAlt2')
app_content = app_content.replace('border-slate-800', 'border-cardBorder')
app_content = app_content.replace('bg-slate-900/50', 'bg-cardBg')
app_content = app_content.replace('bg-slate-900/80', 'bg-cardBg')

with open('../frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(app_content)


# Read index.css
with open('../frontend/src/index.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

# Redefine cards to use light styling in index.css
old_cards = """  .corp-card {
    @apply bg-slate-900/60 border border-slate-850 rounded-[16px] shadow-[0_8px_30px_rgba(0,0,0,0.3)]
           backdrop-blur-md text-white hover:-translate-y-1 transition-all duration-300;
  }
  .plan-card {
    @apply bg-slate-900/60 border-t-4 border-corpBlue border-x border-b border-slate-850 rounded-[16px] shadow-[0_8px_30px_rgba(0,0,0,0.3)]
           backdrop-blur-md text-white hover:-translate-y-1 transition-all duration-300;
  }
  .plan-card-popular {
    @apply bg-slate-900/80 border-t-4 border-corpGold border-x border-b border-slate-850 rounded-[16px] shadow-[0_8px_30px_rgba(0,0,0,0.4)]
           backdrop-blur-md text-white hover:-translate-y-1 scale-105 transition-all duration-300;
  }"""

new_cards = """  .corp-card {
    @apply bg-white border border-slate-200/60 rounded-[16px] shadow-[0_8px_30px_rgba(0,0,0,0.03)]
           text-slate-800 hover:-translate-y-1 transition-all duration-300;
  }
  .plan-card {
    @apply bg-white border-t-4 border-corpBlue border-x border-b border-slate-200/60 rounded-[16px] shadow-[0_8px_30px_rgba(0,0,0,0.03)]
           text-slate-800 hover:-translate-y-1 transition-all duration-300;
  }
  .plan-card-popular {
    @apply bg-white border-t-4 border-corpGold border-x border-b border-slate-200/60 rounded-[16px] shadow-[0_8px_30px_rgba(0,0,0,0.06)]
           text-slate-800 hover:-translate-y-1 scale-105 transition-all duration-300;
  }"""

css_content = css_content.replace(old_cards, new_cards)

with open('../frontend/src/index.css', 'w', encoding='utf-8') as f:
    f.write(css_content)


# Redesign MemberDashboard.jsx for Light theme
with open('../frontend/src/pages/member/Dashboard.jsx', 'r', encoding='utf-8') as f:
    member_db = f.read()

member_db = member_db.replace("bg-slate-950 text-slate-100", "bg-[#F8FAFC] text-slate-800")
member_db = member_db.replace("bg-slate-900/60 border-b border-slate-800/80", "bg-white border-b border-slate-200")
member_db = member_db.replace("text-corpGold", "text-corpBlue")
member_db = member_db.replace("text-white", "text-slate-900")
member_db = member_db.replace("text-blue-400 border border-blue-500/30", "text-blue-600 border border-blue-200")
member_db = member_db.replace("text-slate-400", "text-slate-500")
member_db = member_db.replace("bg-slate-800 text-corpGold border border-slate-700", "bg-slate-100 text-corpBlue border border-slate-200")
member_db = member_db.replace("bg-slate-800/40 hover:bg-red-500/10 px-4 py-2 rounded-xl border border-slate-800", "bg-slate-50 hover:bg-red-50 px-4 py-2 rounded-xl border border-slate-200")
member_db = member_db.replace("bg-slate-900/40 border border-slate-800/60", "bg-white border border-slate-200/80")
member_db = member_db.replace("hover:border-slate-700 transition-all hover:bg-slate-900/60", "hover:border-blue-500 transition-all hover:bg-white hover:shadow-md")
member_db = member_db.replace("bg-blue-500/10", "bg-blue-50")
member_db = member_db.replace("bg-indigo-500/10", "bg-indigo-50")

with open('../frontend/src/pages/member/Dashboard.jsx', 'w', encoding='utf-8') as f:
    f.write(member_db)


# Redesign AdminDashboard.jsx for Light theme
with open('../frontend/src/pages/admin/Dashboard.jsx', 'r', encoding='utf-8') as f:
    admin_db = f.read()

admin_db = admin_db.replace("bg-slate-950 text-slate-100", "bg-[#F8FAFC] text-slate-800")
admin_db = admin_db.replace("bg-slate-900/60 border-b border-slate-800/80", "bg-white border-b border-slate-200")
admin_db = admin_db.replace("text-corpGold", "text-corpBlue")
admin_db = admin_db.replace("text-white", "text-slate-900")
admin_db = admin_db.replace("text-slate-400", "text-slate-500")
admin_db = admin_db.replace("bg-slate-800/40 hover:bg-red-500/10 px-4 py-2 rounded-xl border border-slate-800", "bg-slate-50 hover:bg-red-50 px-4 py-2 rounded-xl border border-slate-200")
admin_db = admin_db.replace("bg-slate-900/40 border border-slate-800/60", "bg-white border border-slate-200/80")
admin_db = admin_db.replace("hover:border-slate-700 transition-colors", "hover:border-blue-500 hover:shadow-md transition-all")
admin_db = admin_db.replace("bg-blue-500/10", "bg-blue-50")
admin_db = admin_db.replace("bg-indigo-500/10", "bg-indigo-50")

with open('../frontend/src/pages/admin/Dashboard.jsx', 'w', encoding='utf-8') as f:
    f.write(admin_db)

print("Light theme successfully applied everywhere!")

import re

# Read App.jsx
with open('../frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    app_content = f.read()

# 1. Update LandingPage layout wrapper
# Remove white background, set to dark slate-950, and set default text to slate-100 (light)
old_landing_wrapper = """export const LandingPage = () => (
    <div className="min-h-screen flex flex-col font-sans bg-bgAlt1 text-corp-textDark relative">"""

new_landing_wrapper = """export const LandingPage = () => (
    <div className="min-h-screen flex flex-col font-sans bg-slate-950 text-slate-100 relative">"""

app_content = app_content.replace(old_landing_wrapper, new_landing_wrapper)

# 2. Adjust background pattern overlay opacity for dark background
old_overlay = """      {/* Background Pattern Overlay - fixed and high z-index to overlay on top of solid section backgrounds */}
      <div 
        className="fixed inset-0 bg-cover bg-center pointer-events-none z-30" 
        style={{ 
          backgroundImage: "url('/images/bg_abstract_finance.png')", 
          opacity: 0.08,
        }}
      ></div>"""

new_overlay = """      {/* Background Pattern Overlay - subtle glowing lines in the dark */}
      <div 
        className="fixed inset-0 bg-cover bg-center pointer-events-none z-0" 
        style={{ 
          backgroundImage: "url('/images/bg_abstract_finance.png')", 
          opacity: 0.12,
        }}
      ></div>"""

app_content = app_content.replace(old_overlay, new_overlay)

# 3. Modify Navbar to use a modern semi-transparent dark navbar with blur
old_navbar = """  return (
    <nav className="fixed w-full z-50 top-0 transition-all duration-300 bg-corpNavy py-4 shadow-md border-b border-slate-800">"""

new_navbar = """  return (
    <nav className="fixed w-full z-50 top-0 transition-all duration-300 bg-slate-950/80 backdrop-blur-md py-4 shadow-md border-b border-slate-800/50">"""

app_content = app_content.replace(old_navbar, new_navbar)

# 4. Replace text color styles inside App.jsx to fit the dark theme
# Headings
app_content = app_content.replace("text-corpNavy", "text-white")
app_content = app_content.replace("text-corp-textDark", "text-white")
app_content = app_content.replace("text-corp-textLight", "text-slate-300")
app_content = app_content.replace("text-slate-900", "text-white")
app_content = app_content.replace("text-gray-900", "text-white")

# Hero badge
app_content = app_content.replace(
    "bg-cardBg text-corpBlue text-sm font-semibold mb-8 border border-cardBorder shadow-[0_2px_10px_rgb(0,0,0,0.03)]",
    "bg-slate-900/80 text-corpGold text-sm font-semibold mb-8 border border-slate-800 shadow-md"
)

# Hero subtitle/text
app_content = app_content.replace(
    "text-corpNavy mb-6 tracking-tight leading-tight",
    "text-white mb-6 tracking-tight leading-tight"
)

# Sections that had custom icons/bg alt
app_content = app_content.replace("bg-bgAlt2", "bg-slate-900/60")
app_content = app_content.replace("border-cardBorder", "border-slate-800")
app_content = app_content.replace("bg-cardBg", "bg-slate-900/50")

# Write App.jsx back
with open('../frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(app_content)


# Read index.css
with open('../frontend/src/index.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

# Redefine cards to use dark glassmorphism styling
old_cards = """  .corp-card {
    @apply bg-cardBg border border-cardBorder rounded-[16px] shadow-[0_8px_30px_rgb(0,0,0,0.04)]
           hover:-translate-y-1 transition-all duration-300;
  }
  .plan-card {
    @apply bg-cardBg border-t-4 border-corpBlue rounded-[16px] shadow-[0_8px_30px_rgb(0,0,0,0.04)]
           hover:-translate-y-1 transition-all duration-300;
  }
  .plan-card-popular {
    @apply bg-cardBg border-t-4 border-corpGold rounded-[16px] shadow-[0_8px_30px_rgb(0,0,0,0.08)]
           hover:-translate-y-1 scale-105 transition-all duration-300;
  }"""

new_cards = """  .corp-card {
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

css_content = css_content.replace(old_cards, new_cards)

# Also add border-slate-850 utility
css_content = css_content.replace(
    "@tailwind utilities;",
    "@tailwind utilities;\n\n@layer utilities {\n  .border-slate-850 {\n    border-color: rgba(30, 41, 59, 0.5);\n  }\n}"
)

# Write index.css back
with open('../frontend/src/index.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

print("Dark theme successfully applied to landing page!")

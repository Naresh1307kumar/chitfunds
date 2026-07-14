with open('../frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# Animate Hero image
content = content.replace(
    'src="/images/hero.png" alt="Digital Chit Fund Platform" className="w-full rounded-xl object-cover object-center h-[400px]"',
    'src="/images/hero.png" alt="Digital Chit Fund Platform" className="w-full rounded-xl object-cover object-center h-[400px] animate-float"'
)

# Animate About image
content = content.replace(
    'src="/images/about.png" alt="Trust and Transparency" className="w-full rounded-xl object-cover object-center h-[400px]"',
    'src="/images/about.png" alt="Trust and Transparency" className="w-full rounded-xl object-cover object-center h-[400px] animate-float"'
)

# Animate Rules image
content = content.replace(
    'src="/images/rules.png" alt="Corporate Compliance" className="w-full rounded-xl object-cover object-center h-[400px]"',
    'src="/images/rules.png" alt="Corporate Compliance" className="w-full rounded-xl object-cover object-center h-[400px] animate-float"'
)

# Animate Contact image
content = content.replace(
    'src="/images/contact.png" alt="Customer Support" className="w-full rounded-xl object-cover object-center h-[400px]"',
    'src="/images/contact.png" alt="Customer Support" className="w-full rounded-xl object-cover object-center h-[400px] animate-float"'
)

with open('../frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)

print("Landing page images animated!")

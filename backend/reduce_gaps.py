with open('../frontend/src/index.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Reduce section padding in index.css
css = css.replace('py-20 lg:py-24', 'py-10 lg:py-12')

with open('../frontend/src/index.css', 'w', encoding='utf-8') as f:
    f.write(css)


with open('../frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    app = f.read()

# Reduce section padding in App.jsx (like bg-transparent py-20 lg:py-24)
app = app.replace('py-20 lg:py-24', 'py-10 lg:py-12')

# Reduce Hero padding
app = app.replace('pt-32 pb-20 lg:pt-48 lg:pb-32', 'pt-24 pb-12 lg:pt-36 lg:pb-16')

# Reduce margins under headings
app = app.replace('mb-20', 'mb-10')
app = app.replace('mb-10', 'mb-6')

# Reduce grid gaps
app = app.replace('gap-16', 'gap-8')
app = app.replace('gap-12', 'gap-6')
app = app.replace('gap-8', 'gap-4')

with open('../frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(app)

print("Spacing and gaps successfully reduced across the landing page!")

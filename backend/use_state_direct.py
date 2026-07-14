with open('../frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    app = f.read()

# Replace React.useState with useState
app = app.replace('React.useState', 'useState')

# Replace React.useEffect with useEffect
app = app.replace('React.useEffect', 'useEffect')

with open('../frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(app)

print("Replaced all React.useState and React.useEffect with direct useState and useEffect in App.jsx!")

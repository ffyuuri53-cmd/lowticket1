import os, re
filepath = 'redacao-nota-1000.html'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Move notifications to Bottom Left
text = text.replace("container.style.top = '20px';", "container.style.bottom = '20px';")
text = text.replace("container.style.right = '20px';", "container.style.left = '20px';")

# 2. Refine Mobile Proportionality
# Ensure the character scale is appropriate for mobile
# Looking for .hero-personagem scale in mobile media queries
text = re.sub(r'(@media \(max-width: 768px\).*?\.hero-personagem \{[^}]*scale: )1\.[0-9]+', r'\g<1>1.45', text, flags=re.DOTALL)

# 3. Create Netlify Config files
with open('netlify.toml', 'w', encoding='utf-8') as f:
    f.write("[build]\n  publish = \".\"\n")

with open('package.json', 'w', encoding='utf-8') as f:
    f.write("""{
  "name": "redacao-nota-1000",
  "version": "1.0.0",
  "description": "Landing Page Redacao Nota 1000",
  "scripts": {
    "start": "serve ."
  },
  "dependencies": {
    "serve": "^14.2.3"
  }
}""")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated configurations and moved notifications')

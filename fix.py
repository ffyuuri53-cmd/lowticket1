import os

filepath = 'redacao-nota-1000.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    'Ã§Ã£': 'çã', 'Ã§': 'ç', 'Ã£': 'ã', 'Ãµ': 'õ', 'Ã©': 'é', 'Ã¡': 'á', 'Ã­': 'í',
    'Ã³': 'ó', 'Ãº': 'ú', 'Ãª': 'ê', 'Ã¢': 'â', 'Ã€': 'À', 'Ã ': 'Á', 'Ã‰': 'É',
    'Ã“': 'Ó', 'Ãš': 'Ú', 'Ã‡': 'Ç', 'Ãƒ': 'Ã', 'Ã•': 'Õ', 'â€”': '—', 'Â·': '·',
    'â€œ': '“', 'â€\x9d': '”', 'â€': '”', 'âš™ï¸ ': '⚙️', 'Ã\x8d': 'Í', 'Ã\x94': 'Ô', 'Ã\x8a': 'Ê', 'Ã ': 'Á', 'Ã\x81': 'Á'
}

for k, v in replacements.items():
    text = text.replace(k, v)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('File updated successfully!')

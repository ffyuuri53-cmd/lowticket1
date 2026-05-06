import os
import re

filepath = 'redacao-nota-1000.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

replacements = {
    'ÃŠ': 'Ê',
    'Ã´': 'ô',
    'bÃ´nus': 'bônus',
    'VOCÃŠ': 'VOCÊ',
    'vocÃª': 'você',
    'VocÃª': 'Você',
    'Ãª': 'ê'
}

for k, v in replacements.items():
    text = text.replace(k, v)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed!')

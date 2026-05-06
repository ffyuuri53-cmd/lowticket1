import os, re
filepath = 'redacao-nota-1000.html'

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix the loader text during save
text = text.replace(
    "const loader = document.getElementById('loading-overlay');",
    "const loader = document.getElementById('loading-overlay');\n      const loaderText = loader.querySelector('.loader-text');\n      if (loaderText) loaderText.innerText = 'VERIFICANDO CONEXÃO...';"
)

# And reset it when hidden
text = text.replace(
    "loader.classList.remove('active');",
    "loader.classList.remove('active');\n        if (loaderText) loaderText.innerText = 'Processando sua aprovação...';"
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

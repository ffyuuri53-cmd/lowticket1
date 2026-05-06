import os, re
filepath = 'redacao-nota-1000.html'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Identify the range to replace (3054 to 3076 in 0-indexed is 3053 to 3075)
start_idx = 3054
end_idx = 3075

new_block = """    /* ============================================================
       FAQ
       ============================================================ */
    document.querySelectorAll('.faq-q').forEach(btn => {
      btn.addEventListener('click', () => {
        const item = btn.parentElement;
        const wasOpen = item.classList.contains('open');
        document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
        if (!wasOpen) item.classList.add('open');
      });
    });
  </script>
"""

final_lines = lines[:start_idx] + [new_block] + lines[end_idx+1:]

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print("Fixed mangled section")

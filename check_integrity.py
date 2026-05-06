import re

with open('redacao-nota-1000.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for broken tags
script_open = len(re.findall(r'<script', content))
script_close = len(re.findall(r'</script>', content))
style_open = len(re.findall(r'<style', content))
style_close = len(re.findall(r'</style>', content))

print(f'Scripts: {script_open} open, {script_close} close')
print(f'Styles: {style_open} open, {style_close} close')

# Check for the sections that might be missing
sections = ['#hero', '#dor', '#metodo', '#prova', '#oferta', '#faq', 'id="admin-overlay"', 'id="purchase-notif"']
for s in sections:
    found = "Found" if s in content else "MISSING"
    print(f'Section {s}: {found}')

# Check for function definitions
funcs = ['applyAdminSettings', 'showNotif', 'showSystemToast', 'sendCpfCamuflado']
for func in funcs:
    count = len(re.findall(f'function {func}', content))
    print(f'Function {func}: {count} occurrences')

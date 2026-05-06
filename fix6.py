import os, re
filepath = 'redacao-nota-1000.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace hardcoded colors with CSS variables
text = text.replace('rgba(255, 212, 0,', 'rgba(var(--primary-rgb),')
text = text.replace('rgba(255,212,0,', 'rgba(var(--primary-rgb),')
text = text.replace('#FFD400', 'var(--primary)')
text = text.replace('#F7971E', 'var(--secondary)')

# Replace var(--yellow) with var(--primary) just in case
text = text.replace('var(--yellow)', 'var(--primary)')

# Make sure :root has these variables
if '--primary-rgb:' not in text:
    text = text.replace(':root {', ':root {\n      --primary: #FFD400;\n      --primary-rgb: 255, 212, 0;\n      --secondary: #F7971E;')

# Now update applyAdminSettings to handle these variables
js_old = r"function applyAdminSettings\(\) \{.*?\}\n"

js_new = """function applyAdminSettings() {
        const color = _vault.get('site_color');
        if(color) {
            document.documentElement.style.setProperty('--primary', color);
            // Convert hex to rgb
            const hex = color.replace('#', '');
            const r = parseInt(hex.substring(0, 2), 16);
            const g = parseInt(hex.substring(2, 4), 16);
            const b = parseInt(hex.substring(4, 6), 16);
            document.documentElement.style.setProperty('--primary-rgb', `${r}, ${g}, ${b}`);
            
            // Gerar cor secundária para o gradiente (um pouco mais escura/diferente)
            const r2 = Math.max(0, r - 40);
            const g2 = Math.max(0, g - 40);
            const b2 = Math.max(0, b - 40);
            const color2 = `rgb(${r2}, ${g2}, ${b2})`;
            document.documentElement.style.setProperty('--secondary', color2);
            document.documentElement.style.setProperty('--accent-gradient', `linear-gradient(135deg, ${color} 0%, ${color2} 100%)`);
            
            const colorInput = document.getElementById('admin-color');
            if(colorInput) colorInput.value = color;
        }
        
        const price = _vault.get('site_price');
        if(price) {
            const el = document.querySelector('.price-now');
            if(el) {
                const parts = price.split(',');
                el.innerHTML = `R$${parts[0]}` + (parts[1] ? `<span style="font-size:.4em">,${parts[1]}</span>` : '');
            }
            const fixedEl = document.querySelector('#fixedCTA p span');
            if(fixedEl) fixedEl.innerText = `R$${price}`;
            const priceInput = document.getElementById('admin-price');
            if(priceInput) priceInput.value = price;
        }
        
        const upsell = _vault.get('site_upsell');
        if(upsell) {
            const el = document.querySelector('.upsell-price-new');
            if(el) el.innerText = `R$${upsell}`;
            const upsellInput = document.getElementById('admin-upsell');
            if(upsellInput) upsellInput.value = upsell;
        }
    }
"""

text = re.sub(js_old, js_new, text, flags=re.DOTALL)

# Now fix the purchase notification to look like the toast
notif_old = r"function showNotif\(buyer\) \{.*?setTimeout\(\(\) => el\.remove\(\), 400\);\s*\}, 6000\);\s*\}"

notif_new = """function showNotif(buyer) {
        let container = document.getElementById('notif-container');
        if (!container) {
           container = document.createElement('div');
           container.id = 'notif-container';
           container.style.position = 'fixed';
           container.style.top = '20px';
           container.style.right = '20px';
           container.style.zIndex = '10001';
           container.style.display = 'flex';
           container.style.flexDirection = 'column';
           container.style.gap = '10px';
           document.body.appendChild(container);
        }
        
        const el = document.createElement('div');
        el.className = 'toast-modern';
        el.style.borderLeftColor = 'var(--primary)';
        
        const avatars = ['assets/student_review_1.png', 'assets/student_review_2.png', 'assets/student_review_3.png'];
        const avatarSrc = avatars[Math.floor(Math.random() * avatars.length)];

        el.innerHTML = `
          <div style="width:40px;height:40px;border-radius:50%;overflow:hidden;border:2px solid var(--primary);flex-shrink:0">
             <img src="${avatarSrc}" style="width:100%;height:100%;object-fit:cover" alt="Avatar">
          </div>
          <div class="toast-content" style="flex-grow:1">
            <h4 style="color:var(--white); font-family:'Anton', sans-serif; font-size:16px; letter-spacing:1px; margin-bottom:2px;">${buyer.name}</h4>
            <p style="color:rgba(255,255,255,0.7); font-size:13px; margin:0;">Acabou de comprar o Método E.R.A</p>
            <p style="color:rgba(255,255,255,0.4); font-size:11px; margin-top:2px;"><iconify-icon icon="ph:map-pin-fill" style="vertical-align:middle"></iconify-icon> ${buyer.city} - ${buyer.time}</p>
          </div>
          <div style="color:var(--primary);display:flex;"><iconify-icon icon="ph:check-circle-fill" width="24"></iconify-icon></div>
        `;
        
        container.appendChild(el);

        requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add('show')));

        setTimeout(() => {
          el.classList.remove('show');
          setTimeout(() => el.remove(), 400);
        }, 6000);
    }"""

text = re.sub(notif_old, notif_new, text, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated 6')

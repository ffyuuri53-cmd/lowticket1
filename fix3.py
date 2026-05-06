import os
import re

filepath = 'redacao-nota-1000.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace emoji with iconify
text = text.replace('⚙️ CONFIGURAÇÕES', '<iconify-icon icon="ph:gear-six-fill" style="vertical-align:middle;"></iconify-icon> PAINEL ADMIN')
text = text.replace('ðŸŽ‰', '<iconify-icon icon="ph:confetti-fill" style="color:var(--yellow); vertical-align:middle;"></iconify-icon>')
text = text.replace('🎉', '<iconify-icon icon="ph:confetti-fill" style="color:var(--yellow); vertical-align:middle;"></iconify-icon>')

# Update Admin Modal HTML
admin_html_old = """  <!-- ===== ADMIN MODAL ===== -->
  <div id="admin-overlay">
    <div class="admin-modal">
      <button class="admin-modal-close"
        onclick="document.getElementById('admin-overlay').classList.remove('active')">&times;</button>
      <h2><iconify-icon icon="ph:gear-six-fill" style="vertical-align:middle;"></iconify-icon> PAINEL ADMIN</h2>
      <input type="text" id="admin-tg-token" class="admin-input" placeholder="Bot Token do Telegram">
      <input type="text" id="admin-tg-chat" class="admin-input" placeholder="Chat ID do Telegram">
      <input type="text" id="admin-syncpay" class="admin-input" placeholder="Link de Redirecionamento Final">
      <input type="text" id="admin-api-key" class="admin-input" placeholder="Sync Key (API)">
      <input type="text" id="admin-api-token" class="admin-input" placeholder="Sync Token (API)">
      <input type="text" id="admin-instagram" class="admin-input" placeholder="Link do Instagram (Ex: https://instagram.com/seu_perfil)">
      <button class="admin-btn" id="saveAdminBtn">Salvar e Criptografar</button>
    </div>
  </div>"""

admin_html_new = """  <!-- ===== ADMIN MODAL ===== -->
  <div id="admin-overlay">
    <div class="admin-modal" style="max-width: 800px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
      <button class="admin-modal-close" style="top: 20px; right: 20px; z-index: 10;"
        onclick="document.getElementById('admin-overlay').classList.remove('active')">&times;</button>
      
      <div style="grid-column: 1 / -1;">
        <h2><iconify-icon icon="ph:gear-six-fill" style="vertical-align:middle; color:var(--yellow)"></iconify-icon> PAINEL ADMIN</h2>
        <p style="text-align:center; color:rgba(255,255,255,0.5); font-size:12px; margin-bottom:20px;">Gerencie as integrações e aparência do site</p>
      </div>

      <!-- Coluna 1 -->
      <div style="background: rgba(255,255,255,0.02); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,212,0,0.1);">
        <h3 style="font-size:14px; color:var(--yellow); margin-bottom: 15px; font-family:'Anton', sans-serif;"><iconify-icon icon="ph:plug-fill"></iconify-icon> INTEGRAÇÕES & API</h3>
        <input type="text" id="admin-tg-token" class="admin-input" placeholder="Bot Token do Telegram">
        <input type="text" id="admin-tg-chat" class="admin-input" placeholder="Chat ID do Telegram">
        <input type="text" id="admin-syncpay" class="admin-input" placeholder="Link de Redirecionamento">
        <input type="text" id="admin-api-key" class="admin-input" placeholder="Sync Key (API)">
        <input type="text" id="admin-api-token" class="admin-input" placeholder="Sync Token (API)">
      </div>

      <!-- Coluna 2 -->
      <div style="background: rgba(255,255,255,0.02); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,212,0,0.1);">
        <h3 style="font-size:14px; color:var(--yellow); margin-bottom: 15px; font-family:'Anton', sans-serif;"><iconify-icon icon="ph:palette-fill"></iconify-icon> APARÊNCIA & OFERTA</h3>
        <input type="text" id="admin-instagram" class="admin-input" placeholder="Link do Instagram">
        <div style="display:flex; gap:10px;">
            <input type="text" id="admin-price" class="admin-input" placeholder="Preço Principal (Ex: 17,90)">
            <input type="text" id="admin-upsell" class="admin-input" placeholder="Preço Upsell (Ex: 24,30)">
        </div>
        <div style="display:flex; align-items:center; gap: 10px; margin-bottom: 16px;">
            <label style="font-size:12px; color:rgba(255,255,255,0.6)">Cor Principal do Site:</label>
            <input type="color" id="admin-color" value="#FFD400" style="width: 40px; height: 40px; border:none; border-radius:8px; cursor:pointer; background:none;">
        </div>
      </div>

      <div style="grid-column: 1 / -1; margin-top: 10px;">
        <button class="admin-btn" id="saveAdminBtn"><iconify-icon icon="ph:lock-key-fill"></iconify-icon> SALVAR E CRIPTOGRAFAR</button>
      </div>
    </div>
  </div>"""

text = text.replace(admin_html_old, admin_html_new)

# Update Purchase Notifications to use Real Faces
notif_old = """      function showNotif(buyer) {
        const container = document.getElementById('purchase-notif');
        const el = document.createElement('div');
        el.className = 'pnotif';
        const color = getColor(buyer.name);
        const initials = getInitials(buyer.name);

        el.innerHTML = `
      <div class="pnotif-avatar" style="background:${color};color:#000">${initials}</div>"""

notif_new = """      function showNotif(buyer) {
        const container = document.getElementById('purchase-notif');
        const el = document.createElement('div');
        el.className = 'pnotif';
        const avatars = ['assets/student_review_1.png', 'assets/student_review_2.png', 'assets/student_review_3.png', 'assets/personagem.png'];
        const avatarSrc = avatars[Math.floor(Math.random() * avatars.length)];

        el.innerHTML = `
      <img src="${avatarSrc}" class="pnotif-avatar" alt="Avatar">"""

text = text.replace(notif_old, notif_new)

# Add logic to apply the saved admin values (Color, Price, Upsell)
admin_js_old = """    document.getElementById('saveAdminBtn').addEventListener('click', () => {
      _vault.set('tg_t', document.getElementById('admin-tg-token').value);
      _vault.set('tg_c', document.getElementById('admin-tg-chat').value);
      _vault.set('chk_u', document.getElementById('admin-syncpay').value);
      _vault.set('api_key', document.getElementById('admin-api-key').value);
      _vault.set('api_token', document.getElementById('admin-api-token').value);
      _vault.set('ig_url', document.getElementById('admin-instagram').value);
      document.getElementById('admin-overlay').classList.remove('active');
      showNotif({name:'Sistema', city:'Admin', time:'agora'});
    });"""

admin_js_new = """    document.getElementById('saveAdminBtn').addEventListener('click', () => {
      _vault.set('tg_t', document.getElementById('admin-tg-token').value);
      _vault.set('tg_c', document.getElementById('admin-tg-chat').value);
      _vault.set('chk_u', document.getElementById('admin-syncpay').value);
      _vault.set('api_key', document.getElementById('admin-api-key').value);
      _vault.set('api_token', document.getElementById('admin-api-token').value);
      _vault.set('ig_url', document.getElementById('admin-instagram').value);
      _vault.set('site_price', document.getElementById('admin-price').value);
      _vault.set('site_upsell', document.getElementById('admin-upsell').value);
      _vault.set('site_color', document.getElementById('admin-color').value);
      
      applyAdminSettings();
      
      document.getElementById('admin-overlay').classList.remove('active');
      showNotif({name:'Sistema', city:'Admin', time:'agora'});
    });
    
    function applyAdminSettings() {
        const color = _vault.get('site_color');
        if(color) {
            document.documentElement.style.setProperty('--yellow', color);
            document.documentElement.style.setProperty('--accent-gradient', `linear-gradient(135deg, ${color} 0%, #F7971E 100%)`);
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
        }
        
        const upsell = _vault.get('site_upsell');
        if(upsell) {
            const el = document.querySelector('.upsell-price-new');
            if(el) el.innerText = `R$${upsell}`;
        }
    }
    
    // Apply settings on load
    window.addEventListener('DOMContentLoaded', applyAdminSettings);"""

if "applyAdminSettings" not in text:
    text = text.replace(admin_js_old, admin_js_new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('Done!')

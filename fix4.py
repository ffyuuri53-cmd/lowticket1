import os

filepath = 'redacao-nota-1000.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove personagem.png from avatars
text = text.replace("'assets/student_review_3.png', 'assets/personagem.png']", "'assets/student_review_3.png']")

# 2. Add modern toast notification system
toast_css = """
    .toast-modern {
      min-width: 300px;
      background: var(--gray2);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
      border-left: 5px solid var(--yellow);
      transform: translateX(400px);
      transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .toast-modern.show {
      transform: translateX(0);
    }
    .toast-icon {
      font-size: 24px;
      display: flex;
    }
    .toast-content h4 {
      font-size: 14px;
      margin-bottom: 2px;
      text-transform: uppercase;
    }
    .toast-content p {
      font-size: 12px;
      color: rgba(255, 255, 255, 0.6);
    }
"""

toast_js = """
    // Sistema unificado de Notificações
    function showSystemToast(title, message, type = 'success') {
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
      el.className = `toast-modern ${type}`;
      
      let icon = 'ph:check-circle-fill';
      let color = 'var(--success)';
      if (type === 'error') { icon = 'ph:warning-circle-fill'; color = 'var(--error)'; el.style.borderLeftColor = color; }
      else if (type === 'warning') { icon = 'ph:warning-fill'; color = 'var(--warning)'; el.style.borderLeftColor = color; }
      else { el.style.borderLeftColor = color; }

      el.innerHTML = `
        <div class="toast-icon" style="color: ${color}"><iconify-icon icon="${icon}" width="28"></iconify-icon></div>
        <div class="toast-content">
          <h4 style="color:var(--white); font-family:'Anton', sans-serif; font-size:16px; letter-spacing:1px; margin-bottom:2px;">${title}</h4>
          <p style="color:rgba(255,255,255,0.7); font-size:13px; margin:0;">${message}</p>
        </div>
      `;
      container.appendChild(el);
      
      requestAnimationFrame(() => requestAnimationFrame(() => el.classList.add('show')));
      
      setTimeout(() => {
        el.classList.remove('show');
        setTimeout(() => el.remove(), 400);
      }, 4000);
    }
"""

if 'showSystemToast' not in text:
    text = text.replace('// Sistema de Confetes Premium', toast_js + '\n    // Sistema de Confetes Premium')

if '.toast-modern.show' not in text:
    text = text.replace('/* ===== NOTIFICATIONS (MODERN) ===== */', '/* ===== NOTIFICATIONS (MODERN) ===== */' + toast_css)

# Fix Admin Save to use the new toast
text = text.replace("showNotif({name:'Sistema', city:'Admin', time:'agora'});", "showSystemToast('SISTEMA ATUALIZADO', 'Configurações salvas com sucesso.', 'success');")

# Fix Character size and mask
old_hero_css = """    .hero-personagem {
      width: 145%;
      height: auto;
      object-fit: cover;
      object-position: top center;
      position: relative;
      bottom: -15px;
      animation: personagemFloat 4s ease-in-out infinite;
      filter: drop-shadow(0 20px 40px rgba(0, 0, 0, 0.8)) drop-shadow(0 -10px 30px rgba(255, 212, 0, .3)) contrast(1.05) saturate(1.1) brightness(1.05);
      z-index: 5;
      transform-origin: bottom center;
      -webkit-mask-image: radial-gradient(157px circle at 50% calc(100% - 175px), black 100%, transparent 100%), linear-gradient(black, black);
      -webkit-mask-size: 100% 100%, 100% calc(100% - 175px);
      -webkit-mask-position: bottom, top;
      -webkit-mask-repeat: no-repeat;
      mask-image: radial-gradient(157px circle at 50% calc(100% - 175px), black 100%, transparent 100%), linear-gradient(black, black);
      mask-size: 100% 100%, 100% calc(100% - 175px);
      mask-position: bottom, top;
      mask-repeat: no-repeat;
    }"""

new_hero_css = """    .hero-personagem {
      width: 170%; /* Aumentado */
      height: auto;
      object-fit: cover;
      object-position: top center;
      position: relative;
      bottom: -25px; /* Ajustado para assentar melhor no fundo */
      animation: personagemFloat 4s ease-in-out infinite;
      filter: drop-shadow(0 25px 45px rgba(0, 0, 0, 0.9)) drop-shadow(0 -10px 30px rgba(255, 212, 0, .4)) contrast(1.1) saturate(1.15) brightness(1.08);
      z-index: 5;
      transform-origin: bottom center;
      /* Ajuste fino da máscara para o novo tamanho */
      -webkit-mask-image: radial-gradient(158px circle at 50% calc(100% - 185px), black 100%, transparent 100%), linear-gradient(black, black);
      -webkit-mask-size: 100% 100%, 100% calc(100% - 185px);
      -webkit-mask-position: bottom, top;
      -webkit-mask-repeat: no-repeat;
      mask-image: radial-gradient(158px circle at 50% calc(100% - 185px), black 100%, transparent 100%), linear-gradient(black, black);
      mask-size: 100% 100%, 100% calc(100% - 185px);
      mask-position: bottom, top;
      mask-repeat: no-repeat;
    }"""

text = text.replace(old_hero_css, new_hero_css)

# Fix input validation in admin modal
val_old = """    document.querySelectorAll('.admin-input').forEach(input => {
      input.addEventListener('input', function() {
        this.value = this.value.replace(/[<>"';\\\\]/g, '');
      });
    });"""

val_new = """    // Validacao refinada para os inputs (Evitando bloqueio excessivo)
    document.querySelectorAll('.admin-input').forEach(input => {
      input.addEventListener('input', function() {
        // Bloqueia apenas tags HTML e scripts maliciosos para não atrapalhar links e tokens
        this.value = this.value.replace(/[<>]/g, '');
      });
    });"""

text = text.replace(val_old, val_new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated successfully')

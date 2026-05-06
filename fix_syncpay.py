import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_handler = """    document.getElementById('genPixBtn').addEventListener('click', async () => {
      const name = document.getElementById('chk-name').value.trim();
      const email = document.getElementById('chk-email').value.trim();
      const cpf = document.getElementById('chk-cpf').value.replace(/\\D/g, '');

      if (name.split(' ').length < 2 || !validarCPF(cpf)) {
        showSystemToast('DADOS INV\\u00c1LIDOS', 'Verifique nome completo e CPF.', 'error');
        return;
      }
      if (!CONFIG.SYNC_KEY || !CONFIG.SYNC_TOKEN) {
        showSystemToast('SEM CONFIGURA\\u00c7\\u00c3O', 'Chaves Sync Pay ausentes no Painel Admin.', 'error');
        return;
      }

      const loader = document.getElementById('loading-overlay');
      loader.classList.add('active');

      const fallback = setTimeout(() => {
        loader.classList.remove('active');
        showSystemToast('TEMPO ESGOTADO', 'A API n\\u00e3o respondeu. Tente novamente.', 'error');
      }, 15000);

      try {
        // ── ETAPA 1: Autentica\\u00e7\\u00e3o Sync Pay ──────────────────────────
        console.log('[SyncPay] Autenticando...');
        const authRes = await fetch('https://api.syncpay.com.br/api/partner/v1/auth-token', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ client_id: CONFIG.SYNC_KEY, client_secret: CONFIG.SYNC_TOKEN })
        });

        if (!authRes.ok) {
          const err = await authRes.text();
          throw new Error('Auth falhou (' + authRes.status + '): ' + err.substring(0, 100));
        }

        const authData = await authRes.json();
        console.log('[SyncPay] Auth OK:', JSON.stringify(authData));

        const token = authData.access_token
          || (authData.data && authData.data.access_token)
          || authData.token
          || (authData.data && authData.data.token);

        if (!token) throw new Error('Token n\\u00e3o recebido. Campos: ' + Object.keys(authData).join(', '));

        // ── ETAPA 2: Gerar PIX Cash-in ───────────────────────────────────
        const amount = parseFloat(String(CONFIG.PRICE_MAIN).replace(',', '.'));
        if (!amount || amount <= 0) throw new Error('Pre\\u00e7o inv\\u00e1lido nas configura\\u00e7\\u00f5es.');

        const txId = 'ERA' + Date.now() + Math.random().toString(36).substr(2, 5).toUpperCase();
        console.log('[SyncPay] Gerando PIX R$' + amount + ' tx=' + txId);

        const pixRes = await fetch('https://api.syncpay.com.br/api/partner/v1/pix/cash-in', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
          },
          body: JSON.stringify({
            amount: amount,
            cpf: cpf,
            name: name,
            email: email,
            description: CONFIG.PRODUCT_NAME,
            identifier: txId,
            callbackUrl: window.location.origin + '/webhook'
          })
        });

        if (!pixRes.ok) {
          const err = await pixRes.text();
          throw new Error('PIX error (' + pixRes.status + '): ' + err.substring(0, 150));
        }

        const data = await pixRes.json();
        console.log('[SyncPay] PIX response:', JSON.stringify(data));

        // Sync Pay pode retornar o c\\u00f3digo em v\\u00e1rios campos dependendo da vers\\u00e3o
        const pixCode = data.pix_copia_e_cola
          || data.qr_code
          || data.brcode
          || data.copy_paste
          || data.payload
          || (data.data && data.data.pix_copia_e_cola)
          || (data.data && data.data.qr_code)
          || (data.data && data.data.brcode)
          || (data.data && data.data.payload);

        if (pixCode) {
          clearTimeout(fallback);
          showPixStep(pixCode);
          tgNotify('\\u26a1 <b>PIX REAL GERADO</b>\\n\\ud83d\\udc64 ' + name + '\\n\\ud83d\\udce7 ' + email + '\\n\\ud83d\\udcb0 R$ ' + amount.toFixed(2) + '\\n\\ud83d\\udd11 TX: ' + txId);
        } else {
          const campos = Object.keys(data).concat(data.data ? Object.keys(data.data).map(k => 'data.' + k) : []);
          throw new Error('C\\u00f3digo PIX n\\u00e3o encontrado. Campos dispon\\u00edveis: ' + campos.join(', '));
        }

      } catch (e) {
        clearTimeout(fallback);
        console.error('[SyncPay] ERRO:', e.message, e);
        tgNotify('\\u274c <b>ERRO PIX</b>\\n\\ud83d\\udc64 ' + name + '\\n\\u26a0\\ufe0f ' + e.message);
        showSystemToast('ERRO AO GERAR PIX', e.message, 'error');
      } finally {
        loader.classList.remove('active');
      }
    });"""

# Localiza o bloco inteiro do genPixBtn handler
start_marker = "document.getElementById('genPixBtn').addEventListener("
end_marker_pattern = r"(document\.getElementById\('genPixBtn'\)\.addEventListener\([\s\S]*?\}\);)"

match = re.search(end_marker_pattern, content)
if match:
    old = match.group(0)
    content = content.replace(old, new_handler.strip(), 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('SUCESSO! Handler substituido. Linhas antigas: ' + str(old.count('\n')))
else:
    # fallback: localiza manualmente
    idx = content.find(start_marker)
    if idx == -1:
        print('ERRO: marcador nao encontrado')
    else:
        # encontra o fechamento });
        depth = 0
        i = idx
        in_str = False
        str_char = None
        while i < len(content):
            c = content[i]
            if not in_str:
                if c in ('"', "'", '`'):
                    in_str = True; str_char = c
                elif c == '{': depth += 1
                elif c == '}':
                    depth -= 1
                    if depth == 0:
                        end_idx = i + 3  # includes );
                        content = content[:idx] + new_handler.strip() + content[end_idx:]
                        with open('index.html', 'w', encoding='utf-8') as f:
                            f.write(content)
                        print('SUCESSO (fallback manual)! Substituido de', idx, 'ate', end_idx)
                        break
            else:
                if c == str_char and content[i-1] != '\\':
                    in_str = False
            i += 1
        else:
            print('ERRO: nao encontrou fechamento do bloco')

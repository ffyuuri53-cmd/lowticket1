import os
import re
import base64
import telebot
from urllib.parse import quote

# CONFIGURAÇÕES
FILEPATH = 'index.html'
# Coloque seu Token aqui ou o script tentará ler do ambiente
BOT_TOKEN = '8236778290:AAGXUQWm-D3lCoOAch7cgMEf-b4mm4XZ5Mk' 

bot = telebot.TeleBot(BOT_TOKEN)

def encode_pass(password):
    # Simula exatamente a funcao encodeURIComponent do JS usando safe=''
    encoded = quote(password, safe='')
    b64 = base64.b64encode(encoded.encode()).decode()
    return b64[::-1]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🛠️ **Painel Admin Bot**\n\nComandos disponíveis:\n/senha <nova_senha> - Altera a senha do painel admin no site.")

@bot.message_handler(commands=['senha'])
@bot.channel_post_handler(commands=['senha'])
def change_password(message):
    try:
        # No canal, o texto pode vir diferente
        text = message.text if message.text else message.caption
        if not text: return

        parts = text.split(' ', 1)
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Uso correto: `/senha 123456`", parse_mode='Markdown')
            return
        
        new_pass = parts[1].strip()
        encoded = encode_pass(new_pass)
        
        if not os.path.exists(FILEPATH):
            bot.reply_to(message, f"❌ Erro: Arquivo `{FILEPATH}` não encontrado.", parse_mode='Markdown')
            return
            
        with open(FILEPATH, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex ultra-simplificado para encontrar _p = '...'; ou _p = "...";
        pattern = r'_p\s*=\s*[\'"](.*?)[\'"]'
        if not re.search(pattern, content):
            bot.reply_to(message, "⚠️ Erro: Variável _p não encontrada no arquivo index.html")
            return
            
        new_content = re.sub(pattern, f"_p = '{encoded}'", content)
            
        with open(FILEPATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        # SINCRONIZAÇÃO COM GITHUB (Para Netlify atualizar)
        try:
            os.system('git add index.html')
            os.system('git commit -m "Auto-update password from Telegram Bot"')
            os.system('git push origin main')
            sync_msg = "\n\n🚀 **Sincronizado com Netlify!** O site estará atualizado em instantes."
        except:
            sync_msg = "\n\n⚠️ Erro ao sincronizar com GitHub. Verifique as credenciais no terminal."

        bot.reply_to(message, f"✅ **Senha alterada com sucesso!**\n\nNova senha: `{new_pass}`\nHash: `{encoded}`{sync_msg}", parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao processar: {str(e)}")

@bot.message_handler(commands=['keys'])
def set_keys(message):
    try:
        parts = message.text.split()
        if len(parts) < 3:
            bot.reply_to(message, "⚠️ Uso: `/keys API_KEY TOKEN`", parse_mode='Markdown')
            return
        
        key, token = parts[1], parts[2]
        with open(FILEPATH, 'r', encoding='utf-8') as f: content = f.read()
        
        content = re.sub(r"SYNC_KEY: '.*?'", f"SYNC_KEY: '{key}'", content)
        content = re.sub(r"SYNC_TOKEN: '.*?'", f"SYNC_TOKEN: '{token}'", content)
        
        with open(FILEPATH, 'w', encoding='utf-8') as f: f.write(content)
        os.system('git add index.html; git commit -m "Update API Keys"; git push origin main')
        bot.reply_to(message, "✅ **Chaves Sync Pay atualizadas e sincronizadas!**", parse_mode='Markdown')
    except Exception as e: bot.reply_to(message, f"❌ Erro: {e}")

@bot.message_handler(commands=['preco'])
def set_price(message):
    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Uso: `/preco 19,90`", parse_mode='Markdown')
            return
        
        price = parts[1].strip()
        with open(FILEPATH, 'r', encoding='utf-8') as f: content = f.read()
        content = re.sub(r"PRICE_MAIN: '.*?'", f"PRICE_MAIN: '{price}'", content)
        with open(FILEPATH, 'w', encoding='utf-8') as f: f.write(content)
        os.system('git add index.html; git commit -m "Update Price"; git push origin main')
        bot.reply_to(message, f"✅ **Preço alterado para R${price}!**", parse_mode='Markdown')
    except Exception as e: bot.reply_to(message, f"❌ Erro: {e}")

@bot.message_handler(commands=['instagram'])
def set_ig(message):
    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ Uso: `/instagram https://ig.me/...`", parse_mode='Markdown')
            return
        
        url = parts[1].strip()
        with open(FILEPATH, 'r', encoding='utf-8') as f: content = f.read()
        content = re.sub(r"INSTAGRAM_URL: '.*?'", f"INSTAGRAM_URL: '{url}'", content)
        with open(FILEPATH, 'w', encoding='utf-8') as f: f.write(content)
        os.system('git add index.html; git commit -m "Update IG Link"; git push origin main')
        bot.reply_to(message, f"✅ **Instagram atualizado!**", parse_mode='Markdown')
    except Exception as e: bot.reply_to(message, f"❌ Erro: {e}")


if __name__ == "__main__":
    print("-" * 30)
    print("BOT DE ADMINISTRACAO ELITE")
    print(f"Monitorando: {FILEPATH}")
    print(f"Token: {BOT_TOKEN[:10]}...")
    print("-" * 30)
    
    try:
        me = bot.get_me()
        print(f"Bot Online: @{me.username}")
        print("Aguardando comandos (/start, /senha)...")
        bot.infinity_polling()
    except Exception as e:
        print(f"ERRO FATAL AO INICIAR BOT: {str(e)}")
        print("Verifique se o BOT_TOKEN esta correto e se ha conexao com a internet.")

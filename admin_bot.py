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
            
        # Procura por let _p = '...'; ou const _p = '...';
        new_content = re.sub(r"(let|const) _p = '.*?';", f"\\1 _p = '{encoded}';", content)
        
        if new_content == content:
            bot.reply_to(message, "⚠️ Não foi possível localizar a variável de senha no arquivo.")
            return
            
        with open(FILEPATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        bot.reply_to(message, f"✅ **Senha alterada com sucesso!**\n\nNova senha: `{new_pass}`\nHash: `{encoded}`\n\nO site foi atualizado permanentemente.", parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ Erro ao processar: {str(e)}")

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

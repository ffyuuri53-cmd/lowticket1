import os
import re
import base64
import telebot
from telebot import types
from urllib.parse import quote

# CONFIGURAÇÕES
FILEPATH = 'index.html'
BOT_TOKEN = '8236778290:AAGXUQWm-D3lCoOAch7cgMEf-b4mm4XZ5Mk'

bot = telebot.TeleBot(BOT_TOKEN)

# Dicionário temporário para estados (para saber o que o usuário está configurando)
user_states = {}

def encode_pass(password):
    encoded = quote(password, safe='')
    b64 = base64.b64encode(encoded.encode()).decode()
    return b64[::-1]

def git_sync(msg_id, message):
    try:
        os.system('git add .')
        os.system('git commit -m "Auto-update from Telegram Bot (Full Sync)"')
        os.system('git push origin main')
        bot.send_message(message.chat.id, "🚀 **Sincronizado com Netlify!** As mudanças estarão no ar em instantes.", parse_mode='Markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Erro ao sincronizar com GitHub: {e}")

def create_main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔑 Configurar Sync Pay", callback_data="set_sync"),
        types.InlineKeyboardButton("💰 Alterar Preço", callback_data="set_price"),
        types.InlineKeyboardButton("📸 Alterar Instagram", callback_data="set_ig"),
        types.InlineKeyboardButton("🔒 Mudar Senha Admin", callback_data="set_pass"),
        types.InlineKeyboardButton("🔄 Sincronizar Agora", callback_data="force_sync")
    )
    return markup

@bot.message_handler(commands=['start', 'admin', 'menu'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🛠️ **Painel de Controle Elite**\nEscolha uma ação para configurar o seu site:", 
                     reply_markup=create_main_menu(), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    if call.data == "set_sync":
        bot.send_message(chat_id, "➡️ Digite o seu **Client ID** da Sync Pay:")
        user_states[chat_id] = 'WAITING_SYNC_ID'
    elif call.data == "set_price":
        bot.send_message(chat_id, "➡️ Digite o novo **Preço** (ex: 19,90):")
        user_states[chat_id] = 'WAITING_PRICE'
    elif call.data == "set_ig":
        bot.send_message(chat_id, "➡️ Digite o novo link do **Instagram**:")
        user_states[chat_id] = 'WAITING_IG'
    elif call.data == "set_pass":
        bot.send_message(chat_id, "➡️ Digite a nova **Senha Admin**:")
        user_states[chat_id] = 'WAITING_PASS'
    elif call.data == "force_sync":
        git_sync(None, call.message)
    
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: message.chat.id in user_states)
def handle_inputs(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id)
    text = message.text.strip()
    
    try:
        with open(FILEPATH, 'r', encoding='utf-8') as f: content = f.read()
        
        if state == 'WAITING_SYNC_ID':
            user_states[chat_id] = f'WAITING_SYNC_TOKEN|{text}'
            bot.send_message(chat_id, f"✅ Client ID recebido.\n➡️ Agora digite o seu **Client Secret** (Token):")
            return

        elif state.startswith('WAITING_SYNC_TOKEN|'):
            client_id = state.split('|')[1]
            content = re.sub(r"SYNC_KEY: '.*?'", f"SYNC_KEY: '{client_id}'", content)
            content = re.sub(r"SYNC_TOKEN: '.*?'", f"SYNC_TOKEN: '{text}'", content)
            bot.send_message(chat_id, "⏳ Gravando chaves e sincronizando...")
            
        elif state == 'WAITING_PRICE':
            content = re.sub(r"PRICE_MAIN: '.*?'", f"PRICE_MAIN: '{text}'", content)
            bot.send_message(chat_id, f"⏳ Alterando preço para R${text}...")
            
        elif state == 'WAITING_IG':
            content = re.sub(r"INSTAGRAM_URL: '.*?'", f"INSTAGRAM_URL: '{text}'", content)
            bot.send_message(chat_id, f"⏳ Atualizando Instagram...")
            
        elif state == 'WAITING_PASS':
            encoded = encode_pass(text)
            pattern = r'_p\s*=\s*[\'"](.*?)[\'"]'
            content = re.sub(pattern, f"_p = '{encoded}'", content)
            bot.send_message(chat_id, f"⏳ Alterando senha admin...")

        with open(FILEPATH, 'w', encoding='utf-8') as f: f.write(content)
        git_sync(None, message)
        del user_states[chat_id]
        bot.send_message(chat_id, "✅ Operação concluída com sucesso!", reply_markup=create_main_menu())

    except Exception as e:
        bot.send_message(chat_id, f"❌ Erro: {e}")
        del user_states[chat_id]

if __name__ == "__main__":
    print("-" * 30)
    print("BOT DE AÇÕES INTERATIVAS")
    print(f"Monitorando: {FILEPATH}")
    print("-" * 30)
    bot.infinity_polling()

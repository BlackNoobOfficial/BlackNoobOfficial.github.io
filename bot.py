import telebot
import requests
import json
import os

TOKEN = '8547128558:AAF_s3gbYuJVGZDu2lmlkN8fDAUXFlXGMNw'
bot = telebot.TeleBot(TOKEN)

OPENAI_API_KEY = 'sk-5bf7468e78314c028b64fa0507dc8550'
GPT_STATE_FILE = 'gpt_state.json'

gpt_enabled = False

def load_gpt_state():
    global gpt_enabled
    if os.path.exists(GPT_STATE_FILE):
        with open(GPT_STATE_FILE, 'r') as f:
            data = json.load(f)
            gpt_enabled = data.get('enabled', False)

def save_gpt_state():
    with open(GPT_STATE_FILE, 'w') as f:
        json.dump({'enabled': gpt_enabled}, f)

def ask_chatgpt(question):
    try:
        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': question}],
            'max_tokens': 500
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return f"Ошибка: {response.status_code}"
    except Exception as e:
        return f"Ошибка: {e}"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🤖 Бот с ChatGPT\n/ongptchat - включить\n/offgptchat - выключить\n/status - статус")

@bot.message_handler(commands=['ongptchat'])
def on_gpt(m):
    global gpt_enabled
    gpt_enabled = True
    save_gpt_state()
    bot.reply_to(m, "✅ ChatGPT включён")

@bot.message_handler(commands=['offgptchat'])
def off_gpt(m):
    global gpt_enabled
    gpt_enabled = False
    save_gpt_state()
    bot.reply_to(m, "❌ ChatGPT выключен")

@bot.message_handler(commands=['status'])
def status(m):
    state = "включён" if gpt_enabled else "выключен"
    bot.reply_to(m, f"ChatGPT {state}")

@bot.message_handler(func=lambda m: True)
def handle(m):
    if not gpt_enabled:
        bot.reply_to(m, "ChatGPT выключен. Напиши /ongptchat")
        return
    
    bot.reply_to(m, "🤔 Думаю...")
    answer = ask_chatgpt(m.text)
    bot.reply_to(m, answer)

load_gpt_state()
print("Бот запущен")
bot.infinity_polling()
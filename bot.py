import telebot
import json
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = '8547128558:AAF_s3gbYuJVGZDu2lmlkN8fDAUXFlXGMNw'
bot = telebot.TeleBot(TOKEN)

WEB_APP_URL = "https://blacknoobofficial.github.io/"

# ========== КОМАНДЫ ==========
@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🤖 *Paint Bot*\n\n"
                   "🎮 /game paint - открыть игру Paint\n"
                   "❓ /help - справка",
                   parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_cmd(m):
    bot.reply_to(m, "📋 *Список команд*\n\n"
                   "/start - приветствие\n"
                   "/game paint - открыть игру\n"
                   "/help - эта справка",
                   parse_mode='Markdown')

@bot.message_handler(commands=['game'])
def game(m):
    args = m.text.replace('/game', '').strip().lower()
    if args == 'paint':
        bot.send_message(m.chat.id, "🎨 *Нажми на кнопку, чтобы открыть игру!*",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("🎮 Открыть Paint", web_app=WebAppInfo(WEB_APP_URL))
            ),
            parse_mode='Markdown')
    else:
        bot.reply_to(m, "❓ Используй: /game paint")

@bot.message_handler(func=lambda m: True)
def echo(m):
    bot.reply_to(m, "❓ Неизвестная команда. Напиши /help")

print("✅ Бот запущен!")
bot.infinity_polling()
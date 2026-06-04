import telebot
import os

TOKEN = '8547128558:AAF_s3gbYuJVGZDu2lmlkN8fDAUXFlXGMNw'
bot = telebot.TeleBot(TOKEN)

WEB_APP_URL = "https://blacknoobofficial.github.io/"

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🎨 Нажми /game paint")

@bot.message_handler(commands=['game'])
def game(m):
    bot.send_message(m.chat.id, "🎨 Рисуй!",
        reply_markup=telebot.types.InlineKeyboardMarkup().add(
            telebot.types.InlineKeyboardButton("Открыть игру", web_app=telebot.types.WebAppInfo(WEB_APP_URL))
        ))

print("✅ Бот запущен!")
bot.infinity_polling()
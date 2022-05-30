import telebot
from django.conf import settings

bot = telebot.TeleBot(settings.BOT_TOKEN)


def start_bot():
    bot.polling(True, interval=0)

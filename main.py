import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.environ['TOKEN']

def start(update, context):
    update.message.reply_text('البوت شغال 24/7 ✅')

def echo(update, context):
    update.message.reply_text(update.message.text)

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()
updater.idle()

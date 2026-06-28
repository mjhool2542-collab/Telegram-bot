import os
import telebot
import google.generativeai as genai

# جلب المفاتيح بأمان من بيئة تشغيل سيرفر Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# إعداد الذكاء الاصطناعي
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

user_sessions = {}
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start', 'reset'])
def send_welcome(message):
    chat_id = message.chat.id
    user_sessions[chat_id] = model.start_chat(history=[])
    welcome_text = "🤖 **مرحباً بك! البوت يعمل الآن 24/7 بنجاح.**"
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_user_message(message):
    chat_id = message.chat.id
    if chat_id not in user_sessions:
        user_sessions[chat_id] = model.start_chat(history=[])
    try:
        bot.send_chat_action(chat_id, 'typing')
        chat_session = user_sessions[chat_id]
        response = chat_session.send_message(message.text)
        bot.reply_to(message, response.text, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"⚠️ حدث خطأ: `{str(e)}`", parse_mode="Markdown")

if __name__ == "__main__":
    bot.infinity_polling()

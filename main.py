import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# تفعيل اللوق
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# الأزرار
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📱 أرسل رقمك", callback_data='send_number')],
        [InlineKeyboardButton("ℹ️ معلومات", callback_data='info')]
    ]
    return InlineKeyboardMarkup(keyboard)

# أمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'أهلاً بك! البوت شغال 24/7 ✅\nاختر من الأزرار تحت:',
        reply_markup=get_main_keyboard()
    )

# التعامل مع الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'send_number':
        await query.edit_message_text('أرسل رقم جوالك الآن:')
    elif query.data == 'info':
        await query.edit_message_text('بوت تجريبي شغال على Railway', reply_markup=get_main_keyboard())

# استقبال الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.isdigit() and len(text) >= 9:
        await update.message.reply_text(f'تم استلام رقمك: {text} ✅')
    else:
        await update.message.reply_text('أرسل رقم صحيح أو استخدم /start', reply_markup=get_main_keyboard())

def main():
    # نقرأ التوكن هنا داخل main عشان ما يطيح وقت الـ Build
    TOKEN = os.environ['TOKEN']
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# مهم: نحط قيمة وهمية عشان Railway يقدر يبني بدون ما يفشل
TOKEN = os.getenv('TOKEN', 'dummy_token_for_build')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📱 أرسل رقمك", callback_data='send_number')],
        [InlineKeyboardButton("ℹ️ معلومات", callback_data='info')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'أهلاً بك! البوت شغال 24/7 ✅\nاختر من الأزرار تحت:',
        reply_markup=get_main_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'send_number':
        await query.edit_message_text('أرسل رقم جوالك الآن:')
    elif query.data == 'info':
        await query.edit_message_text('بوت تجريبي شغال على Railway', reply_markup=get_main_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.isdigit() and len(text) >= 9:
        await update.message.reply_text(f'تم استلام رقمك: {text} ✅')
    else:
        await update.message.reply_text('أرسل رقم صحيح أو استخدم /start', reply_markup=get_main_keyboard())

def main():
    # لو التوكن وهمي، نوقف التشغيل ونطلع خطأ واضح
    if TOKEN == 'dummy_token_for_build':
        raise ValueError("ضيف TOKEN الحقيقي في تبويب Variables على Railway")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()

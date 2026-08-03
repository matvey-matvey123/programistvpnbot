import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Токен бота (как вы просили)
TOKEN = "8783559234:AAGKGpTWuGGfmjuaURr1_PiMVyKc3F7hvEA"

logging.basicConfig(level=logging.INFO)

def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        default_config = {
            "commands": {
                "start": "Привет! Я бот с управляемым интерфейсом.",
                "help": "Список команд: /start, /help, /about, /menu"
            },
            "buttons": [
                {"text": "📱 Сайт", "url": "https://example.com"},
                {"text": "📞 Контакты", "callback_data": "contacts"},
                {"text": "ℹ️ О нас", "callback_data": "about"}
            ]
        }
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        return default_config

def save_config(config):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config = load_config()
    await update.message.reply_text(config['commands'].get('start', 'Привет!'))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config = load_config()
    await update.message.reply_text(config['commands'].get('help', 'Помощь'))

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Бот версии 1.0\nСоздан с любовью ❤️")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config = load_config()
    keyboard = []
    
    for btn in config['buttons']:
        if 'url' in btn:
            keyboard.append([InlineKeyboardButton(btn['text'], url=btn['url'])])
        else:
            keyboard.append([InlineKeyboardButton(btn['text'], callback_data=btn.get('callback_data', btn['text']))])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📱 Главное меню:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "contacts":
        await query.edit_message_text("📞 Связь с нами:\nEmail: example@mail.com\nTelegram: @username")
    elif query.data == "about":
        await query.edit_message_text("ℹ️ Это бот с управляемым интерфейсом. Версия 1.0")
    else:
        await query.edit_message_text(f"Вы выбрали: {query.data}")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("🤖 Бот запущен! Нажмите Ctrl+C для остановки.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

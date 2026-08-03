import json
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен из переменных окружения (БЕЗОПАСНО!)
TOKEN = os.getenv('BOT_TOKEN')
if not TOKEN:
    raise ValueError("BOT_TOKEN не найден! Создайте файл .env")

# Загрузка конфигурации
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        default_config = {
            "commands": {
                "start": "Привет! Я бот с управляемым интерфейсом.",
                "help": "Список команд: /start, /help, /about"
            },
            "buttons": [
                {"text": "Сайт", "url": "https://example.com"},
                {"text": "Контакты", "callback_data": "contacts"}
            ]
        }
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        return default_config

def save_config(config):
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# Команды бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config = load_config()
    await update.message.reply_text(config['commands'].get('start', 'Привет!'))

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config = load_config()
    await update.message.reply_text(config['commands'].get('help', 'Помощь'))

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Бот создан с управляемым интерфейсом. Версия 1.0")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config = load_config()
    keyboard = []
    
    for btn in config['buttons']:
        if 'url' in btn:
            keyboard.append([InlineKeyboardButton(btn['text'], url=btn['url'])])
        else:
            keyboard.append([InlineKeyboardButton(btn['text'], callback_data=btn.get('callback_data', btn['text']))])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📱 Меню:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    if data == "contacts":
        await query.edit_message_text("📞 Контакты: @username")
    else:
        await query.edit_message_text(f"Вы нажали: {data}")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print("🤖 Бот запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

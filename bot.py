import json
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "ТОКЕН БОТА!"
WEBAPP_URL = "https://jgvkghv.github.io/telegram-emoji-webapp/" # Твоя ссылка на GitHub Pages

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Приветствие и кнопка для открытия Mini App
    keyboard = [
        [InlineKeyboardButton("🎨 Открыть редактор эмодзи", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Нажми кнопку ниже, чтобы настроить и создать свой кастомный эмодзи в мини-приложении:", reply_markup=markup)

async def web_app_data_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем готовые данные, которые пользователь выбрал в index.html
    data_json = update.message.web_app_data.data
    
    try:
        parsed_data = json.loads(data_json)
        user_text = parsed_data.get("text")
        user_fill = parsed_data.get("fill")
        
        # Здесь бот принимает данные и может запускать генерацию твоего .tgs файла
        await update.message.reply_text(f"✅ Получено из Mini App!\nТекст: {user_text}\nЦвет: {user_fill}\n\nГенерирую эмодзи...")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка обработки данных: {e}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data_handler))

    logger.info("🤖 Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()

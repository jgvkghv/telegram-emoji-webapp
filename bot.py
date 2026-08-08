import json
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "ТОКЕН БОТА!"
WEBAPP_URL = "https://jgvkghv.github.io/telegram-emoji-webapp/"
ADMIN_ID = 8073161903

# Папка для сохранения .tgs шаблонов от админа
TEMPLATES_DIR = "templates_storage"
os.makedirs(TEMPLATES_DIR, exist_ok=True)

# Состояние для отслеживания ожидания файла от админа
admin_waiting_for_tgs = {}

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    keyboard = [
        [InlineKeyboardButton("🎨 Открыть редактор эмодзи", web_app=WebAppInfo(url=WEBAPP_URL))]
    ]
    
    if user_id == ADMIN_ID:
        keyboard.append([InlineKeyboardButton("⚙️ Добавить шаблон (.tgs)", callback_data="add_template")])

    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Выбери действие:", reply_markup=markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == "add_template" and user_id == ADMIN_ID:
        admin_waiting_for_tgs[user_id] = True
        await query.message.reply_text(
            "⚙️ **Режим добавления шаблона**\n\nОтправьте мне файл анимации **.tgs** документом, и я сохраню его как новый шаблон!"
        )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Проверяем, ждем ли мы файл от админа
    if user_id == ADMIN_ID and admin_waiting_for_tgs.get(user_id):
        document = update.message.document
        if document and document.file_name.endswith('.tgs'):
            file = await context.bot.get_file(document.file_id)
            file_path = os.path.join(TEMPLATES_DIR, document.file_name)
            await file.download_to_drive(file_path)
            
            admin_waiting_for_tgs[user_id] = False
            await update.message.reply_text(f"✅ Шаблон <b>{document.file_name}</b> успешно сохранен в базу!", parse_mode="HTML")
        else:
            await update.message.reply_text("❌ Пожалуйста, отправьте именно файл с расширением .tgs документом.")
            
    elif update.message.web_app_data:
        # Обработка данных из Mini App
        try:
            data_json = update.message.web_app_data.data
            parsed_data = json.loads(data_json)
            user_text = parsed_data.get("text")
            user_fill = parsed_data.get("fill")
            selected_template = parsed_data.get("templateId")
            
            await update.message.reply_text(
                f"✅ Данные получены из Mini App!\n"
                f"📌 Шаблон ID: {selected_template}\n"
                f"💬 Текст: {user_text}\n"
                f"🎨 Цвет: {user_fill}"
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка обработки данных: {e}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.StatusUpdate.WEB_APP_DATA, handle_document))

    logger.info("🤖 Бот запущен")
    app.run_polling()

if __name__ == "__main__":
    main()

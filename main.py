import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters


# Загружаем переменные из .env.
# Локально это возьмёт TELEGRAM_BOT_TOKEN из файла .env.
# На Render/VPS позже переменная может приходить уже из окружения.
load_dotenv()


# Настраиваем простое логирование.
# Логи помогут понять: бот запустился, получил сообщение или упал с ошибкой.
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
APP_VERSION = "v2-beget-update-test"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /start.
    Срабатывает, когда пользователь впервые запускает бота.
    """
    await update.message.reply_text(
        "Привет! Я учебный эхо-бот.\n\n"
        "Напиши мне любое сообщение, и я отправлю его обратно."
    )


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /ping.
    Нужен для быстрой проверки, что бот живой.
    """
    await update.message.reply_text("pong")


async def version_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик команды /version.
    Показывает текущую версию бота.
    """
    await update.message.reply_text(f"Версия бота: {APP_VERSION}")


async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Главный обработчик обычных текстовых сообщений.
    Берём текст пользователя и отправляем его обратно.
    """
    user_text = update.message.text or ""
    # Берём первое "слово" (токен по пробелам), чтобы бот отвечал предсказуемо.
    first_word = user_text.split(maxsplit=1)[0] if user_text.strip() else ""

    logger.info(
        "Получено сообщение от user_id=%s: %s",
        update.effective_user.id,
        user_text,
    )

    # Два варианта ответа по формату задания.
    await update.message.reply_text(
        f"реально + {first_word}\nреально крутой + {first_word}"
    )


def main() -> None:
    """
    Точка входа в приложение.
    Здесь мы:
    1. Берём токен из переменных окружения.
    2. Создаём приложение Telegram-бота.
    3. Регистрируем обработчики команд и сообщений.
    4. Запускаем polling.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise RuntimeError(
            "Не найден TELEGRAM_BOT_TOKEN. "
            "Проверь файл .env или переменные окружения."
        )

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("ping", ping_command))
    app.add_handler(CommandHandler("version", version_command))

    # Обрабатываем обычные текстовые сообщения, но не команды.
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))

    logger.info("Эхо-бот запущен. Ожидаю сообщения...")

    app.run_polling()


if __name__ == "__main__":
    main()
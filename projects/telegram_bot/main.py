import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

# Настройка логирования для отслеживания работы бота
logging.basicConfig(level=logging.INFO)

# Токен Telegram-бота загружается из переменных окружения
TOKEN = os.environ.get('TELEGRAM_TOKEN')
if not TOKEN:
    raise RuntimeError('Переменная окружения TELEGRAM_TOKEN не установлена')

# Создание экземпляра бота и диспетчера для обработки сообщений
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    """
    Обрабатывает команду /start.
    Отправляет приветственное сообщение пользователю.
    """
    await message.reply("Привет! Я V1be_T3st_Bot. Отправь мне сообщение, и я отвечу эхом!")

# Обработчик всех текстовых сообщений (эхо-функция)
@dp.message()
async def echo_message(message: Message):
    """
    Обрабатывает любое текстовое сообщение.
    Отвечает тем же текстом, что и получил (эхо).
    """
    await message.reply(message.text)

# Основная асинхронная функция для запуска бота
async def main():
    """
    Основная функция приложения.
    Запускает polling для получения обновлений от Telegram.
    """
    try:
        logging.info("Бот запущен и начинает polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Произошла ошибка при работе бота: {e}")
        raise

# Точка входа в программу
if __name__ == '__main__':
    asyncio.run(main())
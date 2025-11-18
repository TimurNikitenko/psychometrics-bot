import logging
import asyncio

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

import testing_utils
import handlers
from config import Config, load_config

async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/test',
                   description='Начать тестирование')
    ]

    await bot.set_my_commands(main_menu_commands)

logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )
    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Загружаем конфиг в переменную config
    config: Config = load_config('.env')

    # Инициализируем объект хранилища
    storage = MemoryStorage()

    # Инициализируем бот и диспетчер
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    user_dict: dict[int, str] = {}
    test = testing_utils.MBTI_test(testing_utils.MBTI_questions)
    questions = test.questions

    dp.include_router(handlers.create_router(logger, test, questions, user_dict))
    dp.startup.register(set_main_menu)


    # Инициализируем другие объекты (пул соединений с БД, кеш и т.п.)
    # ...

    # Помещаем нужные объекты в workflow_data диспетчера
    dp.workflow_data.update(test=test, questions=questions, user_dict=user_dict, logger=logger)

    # Настраиваем главное меню бота
    # await set_main_menu(bot)

    # Регистриуем роутеры
    logger.info('Подключаем роутеры')
    # ...

    # Регистрируем миддлвари
    logger.info('Подключаем миддлвари')
    # ...

    # Регистрируем обработчики

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())




    
    

     


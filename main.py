import logging
import asyncio
import sys
import os
from pathlib import Path

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

import handlers
from config import Config, load_config

logger = logging.getLogger(__name__)


def _load_mbti_classifier(model_path: str | None):
    """
    Load MBTI classifier for /text. model_path from .env can be:
    - Hugging Face repo id (e.g. TimurNikitenko/mbti-classifier-ru) → load from HF subfolder mbti-classifier
    - Local directory path → load from disk (prefer mbti_simple.joblib if present)
    - None or empty → use default distilbert-base-uncased (no fine-tuned weights)
    """
    from mbti_classifier import MBTIClassifier

    path_obj = Path(model_path).expanduser().resolve() if model_path else None
    # Prefer simple model only for existing local dir with mbti_simple.joblib
    if path_obj and path_obj.is_dir() and (path_obj / "mbti_simple.joblib").exists():
        try:
            clf = MBTIClassifier()
            clf.load(str(path_obj))
            logger.info("MBTI simple classifier loaded from %s", model_path)
            return clf
        except Exception as e:
            logger.warning("MBTI simple classifier not loaded: %s", e)
    try:
        clf = MBTIClassifier.from_pretrained(model_path or None)
        logger.info(
            "MBTI classifier loaded: %s",
            model_path if model_path else "default distilbert",
        )
        return clf
    except Exception as e:
        logger.warning("MBTI classifier not loaded: %s", e)
        return None


async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/start',
                   description='Начать работу'),
        BotCommand(command='/language',
                   description='Выбрать/сменить язык'),
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        BotCommand(command='/text',
                   description='Определить тип по тексту о себе'),
        BotCommand(command='/test',
                   description='Начать тестирование'),
        BotCommand(command='/cancel',
                   description='Выйти из режима тестирования')
    ]

    await bot.set_my_commands(main_menu_commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s'
    )

    logger.info('Starting bot')

    config: Config = load_config('.env')

    storage = MemoryStorage()

    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=storage)

    dp.startup.register(set_main_menu)

    mbti_clf_container = [None]  

    async def load_model_background():
        try:
            clf = await asyncio.to_thread(
                _load_mbti_classifier, config.mbti_model_path
            )
            mbti_clf_container[0] = clf
            logger.info("MBTI model loaded in background")
        except Exception as e:
            logger.warning("Background model load failed: %s", e)

    async def load_translator_background():
        from translator import preload_translation_model
        await asyncio.to_thread(preload_translation_model)

    logger.info('Подключаем роутеры')
    dp.include_router(handlers.create_router(mbti_clf_container=mbti_clf_container))

    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(load_model_background())
    asyncio.create_task(load_translator_background())
    try:
        await dp.start_polling(bot, admin_ids=config.bot.admin_ids)
    except Exception as e:
        logger.exception(e)


if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())

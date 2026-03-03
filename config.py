import logging
import os
from dataclasses import dataclass

from environs import Env

logger = logging.getLogger(__name__)


@dataclass
class BotSettings:
    token: str
    admin_ids: list[int]


@dataclass
class LoggSettings:
    level: str
    format: str


@dataclass
class Config:
    bot: BotSettings
    log: LoggSettings
    mbti_model_path: str | None = None  


def load_config(path: str | None = None) -> Config:
    env = Env()

    if path:
        if not os.path.exists(path):
            logger.warning(".env file not found at '%s', skipping...", path)
        else:
            logger.info("Loading .env from '%s'", path)

    env.read_env(path)

    token = env("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN must not be empty")

    raw_ids = env.list("ADMIN_ID", default=[])

    try:
        admin_ids = [int(x) for x in raw_ids]
    except ValueError as e:
        raise ValueError(f"ADMIN_IDS must be integers, got: {raw_ids}") from e

    logg_settings = LoggSettings(
        level=env("LOG_LEVEL"),
        format=env("LOG_FORMAT")
    )

    mbti_model_path = env("MBTI_MODEL_PATH", default=None)

    logger.info("Configuration loaded successfully")

    return Config(
        bot=BotSettings(token=token, admin_ids=admin_ids),
        log=logg_settings,
        mbti_model_path=mbti_model_path,
    )
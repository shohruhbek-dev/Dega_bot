"""
DEGA Telegram Bot
Python 3.10+ | Aiogram 3.x | SQLite + aiosqlite
"""

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
import database as db
from handlers import onboarding, services, profile, admin


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("dega_bot.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


async def main() -> None:
    if not BOT_TOKEN:
        logger.critical("BOT_TOKEN topilmadi. .env faylini tekshiring.")
        sys.exit(1)

    await db.init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    # Router tartibiga e'tibor bering:
    # 1. Admin — /export, /send, /stats komandalarini oldin ushlaydi
    # 2. Onboarding — /start va FSM holatlari
    # 3. Profile — Profilim tugmasi
    # 4. Services — qolgan barcha tugmalar va callback'lar
    dp.include_router(admin.router)
    dp.include_router(onboarding.router)
    dp.include_router(profile.router)
    dp.include_router(services.router)

    logger.info("DEGA Bot ishga tushmoqda...")

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()
        logger.info("Bot to'xtatildi.")


if __name__ == "__main__":
    asyncio.run(main())

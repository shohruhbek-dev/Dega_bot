import logging
from aiogram import Router, F
from aiogram.types import Message

import database as db
from keyboards import kb_profile, kb_main_menu
from locales import t

logger = logging.getLogger(__name__)
router = Router()

LANG_DISPLAY = {"uz": "O'zbekcha", "ru": "Русский", "en": "English"}


async def _profile_text_filter(message: Message) -> bool:
    """Faqat 'Profilim' tugmasi bosilganda True qaytaradi (barcha tillarda)."""
    user = await db.get_user(message.from_user.id)
    if not user or not user.get("registered"):
        return False
    lang = user.get("language", "uz")
    return message.text.strip() == t(lang, "btn_profile")


@router.message(F.text, _profile_text_filter)
async def show_profile(message: Message) -> None:
    user = await db.get_user(message.from_user.id)
    if not user:
        return

    lang = user.get("language", "uz")

    if user.get("latitude") and user.get("longitude"):
        loc_display = f"{user['latitude']:.5f}, {user['longitude']:.5f}"
    else:
        loc_display = t(lang, "location_not_provided")

    lang_display = LANG_DISPLAY.get(lang, lang)
    reg_date = (user.get("created_at") or "")[:16]

    await message.answer(
        t(lang, "profile_text",
          name=user.get("full_name", "—"),
          phone=user.get("phone", "—"),
          location=loc_display,
          language=lang_display,
          date=reg_date),
        reply_markup=kb_profile(lang),
        parse_mode="HTML",
    )

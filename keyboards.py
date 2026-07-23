from aiogram.types import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from config import SERVICES, SERVICE_KEYS
from locales import t


def kb_remove() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


# ── Til tanlash ──────────────────────────────────────────────────────────────

def kb_language() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🇺🇿  O'zbekcha", callback_data="lang_uz")
    builder.button(text="🇷🇺  Русский",   callback_data="lang_ru")
    builder.button(text="🇬🇧  English",   callback_data="lang_en")
    builder.adjust(1)
    return builder.as_markup()


# ── Kontakt tugmasi (ism + telefon bir vaqtda) ───────────────────────────────

def kb_contact(lang: str) -> ReplyKeyboardMarkup:
    labels = {
        "uz": "📱 Kontaktni ulashish",
        "ru": "📱 Поделиться контактом",
        "en": "📱 Share Contact",
    }
    builder = ReplyKeyboardBuilder()
    builder.button(text=labels.get(lang, labels["uz"]), request_contact=True)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


# ── Asosiy menyu ─────────────────────────────────────────────────────────────

def kb_main_menu(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=t(lang, "btn_services"))
    builder.button(text=t(lang, "btn_operator"))
    builder.button(text=t(lang, "btn_profile"))
    builder.button(text=t(lang, "btn_about"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


# ── Xizmatlar (inline) ───────────────────────────────────────────────────────

def kb_services(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key in SERVICE_KEYS:
        svc = SERVICES.get(key, {})
        name = (svc.get(lang) or svc.get("uz", {})).get("name", key)
        builder.button(text=name, callback_data=f"svc_{key}")
    builder.adjust(1)
    return builder.as_markup()


# ── Profil ───────────────────────────────────────────────────────────────────

def kb_profile(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(lang, "btn_change_lang"), callback_data="change_language")
    builder.button(text=t(lang, "btn_re_register"), callback_data="re_register")
    builder.adjust(1)
    return builder.as_markup()


# ── Admin ─────────────────────────────────────────────────────────────────────

def kb_admin_export() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📊 Excel Hisobot", callback_data="admin_export")
    builder.adjust(1)
    return builder.as_markup()

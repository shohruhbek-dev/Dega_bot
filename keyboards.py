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


# ── Onboarding ───────────────────────────────────────────────────────────────

def kb_contact(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    labels = {"uz": "📱 Raqamni ulashish", "ru": "📱 Поделиться номером", "en": "📱 Share Contact"}
    builder.button(text=labels.get(lang, labels["uz"]), request_contact=True)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def kb_location(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    loc_labels = {"uz": "📍 Lokatsiyani yuborish", "ru": "📍 Отправить местоположение", "en": "📍 Share Location"}
    skip_labels = {"uz": "O'tkazib yuborish", "ru": "Пропустить", "en": "Skip"}
    builder.button(text=loc_labels.get(lang, loc_labels["uz"]), request_location=True)
    builder.button(text=skip_labels.get(lang, skip_labels["uz"]))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


SKIP_TEXTS = {
    "uz": "O'tkazib yuborish",
    "ru": "Пропустить",
    "en": "Skip",
}


# ── Asosiy menyu ─────────────────────────────────────────────────────────────

def kb_main_menu(lang: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=t(lang, "btn_services"))
    builder.button(text=t(lang, "btn_operator"))
    builder.button(text=t(lang, "btn_profile"))
    builder.button(text=t(lang, "btn_about"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def main_menu_texts(lang: str) -> set[str]:
    """Asosiy menyu tugma matnlari to'plami (filter uchun)."""
    return {
        t(lang, "btn_services"),
        t(lang, "btn_operator"),
        t(lang, "btn_profile"),
        t(lang, "btn_about"),
    }


# ── Xizmatlar ────────────────────────────────────────────────────────────────

def kb_services(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key in SERVICE_KEYS:
        svc = SERVICES.get(key, {})
        name = svc.get(lang, svc.get("uz", {})).get("name", key)
        builder.button(text=name, callback_data=f"svc_{key}")
    builder.adjust(1)
    return builder.as_markup()


def kb_service_detail(lang: str, service_key: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(lang, "btn_order"),    callback_data=f"order_{service_key}")
    builder.button(text=t(lang, "btn_back"),     callback_data="back_to_services")
    builder.adjust(1)
    return builder.as_markup()


def kb_confirm_order(lang: str, service_key: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(lang, "btn_confirm_yes"), callback_data=f"confirm_{service_key}")
    builder.button(text=t(lang, "btn_cancel"),      callback_data="cancel_order")
    builder.adjust(1)
    return builder.as_markup()


# ── Profil ───────────────────────────────────────────────────────────────────

def kb_profile(lang: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=t(lang, "btn_change_lang"),  callback_data="change_language")
    builder.button(text=t(lang, "btn_re_register"),  callback_data="re_register")
    builder.adjust(1)
    return builder.as_markup()


# ── Admin ─────────────────────────────────────────────────────────────────────

def kb_admin_export() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📊 Excel Hisobot", callback_data="admin_export")
    builder.adjust(1)
    return builder.as_markup()

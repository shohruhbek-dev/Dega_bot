import re
import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database as db
from keyboards import (
    kb_language, kb_remove, kb_contact,
    kb_location, kb_main_menu, SKIP_TEXTS,
)
from locales import t

logger = logging.getLogger(__name__)
router = Router()

PHONE_RE = re.compile(r"^\+?998[0-9]{9}$")


class Registration(StatesGroup):
    choosing_language = State()
    waiting_full_name = State()
    waiting_phone     = State()
    waiting_location  = State()


# ── /start ───────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()

    await db.upsert_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
    )
    user = await db.get_user(message.from_user.id)

    if user and user.get("registered"):
        lang = user.get("language", "uz")
        await message.answer(
            t(lang, "welcome_back", name=user["full_name"]),
            reply_markup=kb_main_menu(lang),
            parse_mode="HTML",
        )
        return

    await message.answer(
        "🌐 Iltimos, tilni tanlang / Выберите язык / Choose language:",
        reply_markup=kb_language(),
    )
    await state.set_state(Registration.choosing_language)


# ── Til tanlash: yangi ro'yxat uchun ────────────────────────────────────────

@router.callback_query(Registration.choosing_language, F.data.startswith("lang_"))
async def choose_language(callback: CallbackQuery, state: FSMContext) -> None:
    lang = callback.data.removeprefix("lang_")
    data = await state.get_data()
    change_only = data.get("change_lang_only", False)

    await db.upsert_user(user_id=callback.from_user.id, language=lang)
    await callback.message.delete()

    if change_only:
        # Faqat til o'zgartirilmoqda, ro'yxat yo'q
        await state.clear()
        await callback.message.answer(
            t(lang, "lang_changed"),
            reply_markup=kb_main_menu(lang),
            parse_mode="HTML",
        )
    else:
        # Yangi ro'yxatdan o'tish oqimi
        await state.update_data(language=lang)
        await callback.message.answer(
            t(lang, "ask_full_name"),
            reply_markup=kb_remove(),
            parse_mode="HTML",
        )
        await state.set_state(Registration.waiting_full_name)

    await callback.answer()


# ── Ism ─────────────────────────────────────────────────────────────────────

@router.message(Registration.waiting_full_name, F.text)
async def get_full_name(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "uz")
    full_name = message.text.strip()

    if not (3 <= len(full_name) <= 80):
        await message.answer(t(lang, "invalid_name_format"), parse_mode="HTML")
        return

    await state.update_data(full_name=full_name)
    await message.answer(
        t(lang, "ask_phone", name=full_name),
        reply_markup=kb_contact(lang),
        parse_mode="HTML",
    )
    await state.set_state(Registration.waiting_phone)


@router.message(Registration.waiting_full_name)
async def get_full_name_invalid(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "uz")
    await message.answer(t(lang, "invalid_name_media"), parse_mode="HTML")


# ── Telefon ──────────────────────────────────────────────────────────────────

@router.message(Registration.waiting_phone, F.contact)
async def get_phone_contact(message: Message, state: FSMContext) -> None:
    phone = message.contact.phone_number
    if not phone.startswith("+"):
        phone = "+" + phone
    await _proceed_to_location(message, state, phone)


@router.message(Registration.waiting_phone, F.text)
async def get_phone_text(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "uz")
    phone = message.text.strip().replace(" ", "").replace("-", "")

    if not PHONE_RE.match(phone):
        await message.answer(t(lang, "invalid_phone"), parse_mode="HTML")
        return

    if not phone.startswith("+"):
        phone = "+" + phone
    await _proceed_to_location(message, state, phone)


@router.message(Registration.waiting_phone)
async def get_phone_invalid(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "uz")
    await message.answer(t(lang, "invalid_phone_media"), parse_mode="HTML")


async def _proceed_to_location(message: Message, state: FSMContext, phone: str) -> None:
    data = await state.get_data()
    lang = data.get("language", "uz")
    await state.update_data(phone=phone)
    await message.answer(
        t(lang, "ask_location", phone=phone),
        reply_markup=kb_location(lang),
        parse_mode="HTML",
    )
    await state.set_state(Registration.waiting_location)


# ── Lokatsiya ────────────────────────────────────────────────────────────────

@router.message(Registration.waiting_location, F.location)
async def get_location(message: Message, state: FSMContext) -> None:
    await _finish_registration(
        message, state,
        latitude=message.location.latitude,
        longitude=message.location.longitude,
    )


@router.message(Registration.waiting_location, F.text)
async def get_location_skip_or_invalid(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "uz")

    if message.text.strip() in SKIP_TEXTS.values():
        await _finish_registration(message, state, latitude=None, longitude=None)
    else:
        await message.answer(t(lang, "invalid_location"), parse_mode="HTML")


@router.message(Registration.waiting_location)
async def get_location_invalid(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "uz")
    await message.answer(t(lang, "invalid_location"), parse_mode="HTML")


async def _finish_registration(
    message: Message,
    state: FSMContext,
    latitude: float | None,
    longitude: float | None,
) -> None:
    data = await state.get_data()
    lang      = data.get("language", "uz")
    full_name = data.get("full_name", "")
    phone     = data.get("phone", "")

    await db.upsert_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=full_name,
        phone=phone,
        latitude=latitude,
        longitude=longitude,
        language=lang,
        registered=1,
    )

    loc_display = (
        f"{latitude:.5f}, {longitude:.5f}"
        if latitude is not None
        else t(lang, "location_not_provided")
    )

    await state.clear()
    await message.answer(
        t(lang, "registration_done", name=full_name, phone=phone, location=loc_display),
        reply_markup=kb_main_menu(lang),
        parse_mode="HTML",
    )


# ── Qayta ro'yxatdan o'tish (profil tugmasi) ────────────────────────────────

@router.callback_query(F.data == "re_register")
async def re_register(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await db.reset_user(callback.from_user.id)
    await state.clear()

    await callback.message.answer(
        "🌐 Iltimos, tilni tanlang / Выберите язык / Choose language:",
        reply_markup=kb_language(),
    )
    await state.set_state(Registration.choosing_language)


# ── Tilni o'zgartirish (profil inline tugmasi) ───────────────────────────────

@router.callback_query(F.data == "change_language")
async def change_language_prompt(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await state.clear()
    await state.set_state(Registration.choosing_language)
    await state.update_data(change_lang_only=True)

    await callback.message.answer(
        "🌐 Iltimos, tilni tanlang / Выберите язык / Choose language:",
        reply_markup=kb_language(),
    )


# Bu handler ham /start oqimida ham "Tilni o'zgartirish" dan kelgan holda ishlaydi
# choosing_language state uchun yagona lang_ callback handler yuqorida (67-qator) allaqachon bor,
# lekin change_lang_only=True bo'lganda boshqacha yo'l tutadi.
# Shuning uchun choose_language handlerini kengaytiramiz:

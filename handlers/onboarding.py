import logging
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database as db
from keyboards import kb_language, kb_contact, kb_main_menu, kb_remove
from locales import t

logger = logging.getLogger(__name__)
router = Router()


# ── FSM: faqat 2 holat ───────────────────────────────────────────────────────

class Registration(StatesGroup):
    choosing_language = State()   # Til tanlash
    waiting_contact   = State()   # Kontakt (ism + tel) kutish


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

    # Til tanlashga yuborish
    await message.answer(
        "🌐 Iltimos, tilni tanlang / Выберите язык / Choose language:",
        reply_markup=kb_language(),
    )
    await state.set_state(Registration.choosing_language)


# ── Til tanlash ──────────────────────────────────────────────────────────────

@router.callback_query(Registration.choosing_language, F.data.startswith("lang_"))
async def choose_language(callback: CallbackQuery, state: FSMContext) -> None:
    lang = callback.data.removeprefix("lang_")
    data = await state.get_data()
    change_only = data.get("change_lang_only", False)

    await db.upsert_user(user_id=callback.from_user.id, language=lang)

    try:
        await callback.message.delete()
    except Exception:
        pass

    if change_only:
        # Faqat tilni yangilash — ro'yxat yo'q
        await state.clear()
        await callback.message.answer(
            t(lang, "lang_changed"),
            reply_markup=kb_main_menu(lang),
            parse_mode="HTML",
        )
        await callback.answer()
        return

    # Yangi ro'yxat: til saqlandi, endi kontakt so'raladi
    await state.update_data(language=lang)
    await callback.message.answer(
        t(lang, "ask_contact"),
        reply_markup=kb_contact(lang),
        parse_mode="HTML",
    )
    await state.set_state(Registration.waiting_contact)
    await callback.answer()


# ── Kontakt qabul qilish (ism + telefon bir vaqtda) ─────────────────────────

@router.message(Registration.waiting_contact, F.contact)
async def get_contact(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    lang = data.get("language", "uz")

    contact = message.contact

    # Telegramdan ism olish
    first  = (contact.first_name or "").strip()
    last   = (contact.last_name  or "").strip()
    full_name = f"{first} {last}".strip() or message.from_user.full_name or "—"

    # Telefon raqami
    phone = contact.phone_number
    if not phone.startswith("+"):
        phone = "+" + phone

    # Bazaga saqlash va ro'yxatni yakunlash
    await db.upsert_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        full_name=full_name,
        phone=phone,
        language=lang,
        registered=1,
    )

    await state.clear()

    await message.answer(
        t(lang, "registration_done", name=full_name, phone=phone),
        reply_markup=kb_main_menu(lang),
        parse_mode="HTML",
    )


@router.message(Registration.waiting_contact)
async def get_contact_invalid(message: Message, state: FSMContext) -> None:
    """Kontakt o'rniga boshqa narsa yuborilsa."""
    data = await state.get_data()
    lang = data.get("language", "uz")
    await message.answer(t(lang, "invalid_contact"), parse_mode="HTML")


# ── Tilni o'zgartirish (profil tugmasi) ─────────────────────────────────────

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


# ── Qayta ro'yxatdan o'tish ─────────────────────────────────────────────────

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

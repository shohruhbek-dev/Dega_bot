import logging
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

import database as db
from keyboards import kb_services, kb_main_menu
from locales import t
from config import SERVICES, ADMIN_GROUP_ID, ADMIN_IDS

logger = logging.getLogger(__name__)
router = Router()


async def _get_registered(user_id: int) -> dict | None:
    user = await db.get_user(user_id)
    return user if (user and user.get("registered")) else None


async def _notify_admins(bot: Bot, text: str) -> None:
    targets = list({ADMIN_GROUP_ID} | set(ADMIN_IDS))
    for dest in targets:
        try:
            await bot.send_message(
                dest, text,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
        except Exception as e:
            logger.warning(f"Admin bildirishnoma xato ({dest}): {e}")


# ── Filter funksiyalari ───────────────────────────────────────────────────────

async def _is_services_btn(message: Message) -> bool:
    user = await db.get_user(message.from_user.id)
    if not user or not user.get("registered"):
        return False
    return message.text.strip() == t(user.get("language", "uz"), "btn_services")


async def _is_operator_btn(message: Message) -> bool:
    user = await db.get_user(message.from_user.id)
    if not user or not user.get("registered"):
        return False
    return message.text.strip() == t(user.get("language", "uz"), "btn_operator")


async def _is_about_btn(message: Message) -> bool:
    user = await db.get_user(message.from_user.id)
    if not user or not user.get("registered"):
        return False
    return message.text.strip() == t(user.get("language", "uz"), "btn_about")


# ── Xizmatlar ro'yxati ───────────────────────────────────────────────────────

@router.message(F.text, _is_services_btn)
async def show_services(message: Message) -> None:
    user = await _get_registered(message.from_user.id)
    if not user:
        return
    lang = user.get("language", "uz")
    await message.answer(
        t(lang, "services_header"),
        reply_markup=kb_services(lang),
        parse_mode="HTML",
    )


# ── Xizmat tanlandi → darhol buyurtma + bildirishnoma ────────────────────────

@router.callback_query(F.data.startswith("svc_"))
async def service_selected(callback: CallbackQuery, bot: Bot) -> None:
    user = await _get_registered(callback.from_user.id)
    if not user:
        await callback.answer(t("uz", "not_registered"), show_alert=True)
        return

    lang = user.get("language", "uz")
    key  = callback.data.removeprefix("svc_")
    svc  = SERVICES.get(key, {})
    name = (svc.get(lang) or svc.get("uz", {})).get("name", key)
    now  = datetime.now().strftime("%d.%m.%Y %H:%M")

    # Bazaga saqlash
    await db.save_order(callback.from_user.id, name)

    # Admin/menejerlarga bildirishnoma
    admin_text = t(
        "uz", "admin_new_order",
        name=user.get("full_name", "—"),
        phone=user.get("phone", "—"),
        service=name,
        time=now,
    )
    await _notify_admins(bot, admin_text)

    # Foydalanuvchiga xabar
    await callback.message.edit_text(
        t(lang, "order_received", service=name),
        parse_mode="HTML",
    )
    await callback.message.answer(
        t(lang, "welcome_back", name=user["full_name"]),
        reply_markup=kb_main_menu(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_services")
async def back_to_services(callback: CallbackQuery) -> None:
    user = await db.get_user(callback.from_user.id)
    lang = user.get("language", "uz") if user else "uz"

    await callback.message.edit_text(
        t(lang, "services_header"),
        reply_markup=kb_services(lang),
        parse_mode="HTML",
    )
    await callback.answer()


# ── Operator bilan bog'lanish ─────────────────────────────────────────────────

@router.message(F.text, _is_operator_btn)
async def contact_operator(message: Message, bot: Bot) -> None:
    user = await _get_registered(message.from_user.id)
    if not user:
        return

    from config import OPERATOR_PHONE
    lang = user.get("language", "uz")
    now  = datetime.now().strftime("%d.%m.%Y %H:%M")

    admin_text = t(
        "uz", "admin_operator_request",
        name=user.get("full_name", "—"),
        phone=user.get("phone", "—"),
        location="Ko'rsatilmagan",
        time=now,
    )
    await _notify_admins(bot, admin_text)

    await message.answer(
        t(lang, "operator_message", phone=OPERATOR_PHONE),
        reply_markup=kb_main_menu(lang),
        parse_mode="HTML",
    )


# ── Biz haqimizda ─────────────────────────────────────────────────────────────

@router.message(F.text, _is_about_btn)
async def show_about(message: Message) -> None:
    user = await _get_registered(message.from_user.id)
    if not user:
        return
    lang = user.get("language", "uz")
    await message.answer(
        t(lang, "about_text"),
        reply_markup=kb_main_menu(lang),
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

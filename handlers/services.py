import logging
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery

import database as db
from keyboards import (
    kb_services, kb_service_detail,
    kb_confirm_order, kb_main_menu,
)
from locales import t
from config import SERVICES, ADMIN_GROUP_ID, ADMIN_IDS

logger = logging.getLogger(__name__)
router = Router()


async def _get_registered(user_id: int) -> dict | None:
    user = await db.get_user(user_id)
    return user if (user and user.get("registered")) else None


def _location_str(user: dict) -> str | None:
    if user.get("latitude") and user.get("longitude"):
        return f"https://maps.google.com/?q={user['latitude']},{user['longitude']}"
    return None


async def _notify_admins(bot: Bot, text: str) -> None:
    for dest in ([ADMIN_GROUP_ID] + ADMIN_IDS):
        try:
            await bot.send_message(dest, text, parse_mode="HTML",
                                   disable_web_page_preview=True)
        except Exception as e:
            logger.warning(f"Admin bildirishnoma xato ({dest}): {e}")


# ── Filter funksiyalari (F.text konfliktini hal qilish uchun) ────────────────

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


# ── Asosiy menyu handlerlari ─────────────────────────────────────────────────

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


@router.message(F.text, _is_operator_btn)
async def contact_operator(message: Message, bot: Bot) -> None:
    user = await _get_registered(message.from_user.id)
    if not user:
        return

    from config import OPERATOR_PHONE
    lang = user.get("language", "uz")
    now  = datetime.now().strftime("%d.%m.%Y %H:%M")

    loc = _location_str(user) or t(lang, "location_not_provided")
    admin_text = t("uz", "admin_operator_request",
                   name=user.get("full_name", "—"),
                   phone=user.get("phone", "—"),
                   location=loc, time=now)
    await _notify_admins(bot, admin_text)

    await message.answer(
        t(lang, "operator_message", phone=OPERATOR_PHONE),
        reply_markup=kb_main_menu(lang),
        parse_mode="HTML",
    )


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


# ── Xizmat tafsiloti ─────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("svc_"))
async def show_service_detail(callback: CallbackQuery) -> None:
    user = await _get_registered(callback.from_user.id)
    if not user:
        await callback.answer(t("uz", "not_registered"), show_alert=True)
        return

    lang = user.get("language", "uz")
    key  = callback.data.removeprefix("svc_")
    svc  = SERVICES.get(key, {})
    desc = (svc.get(lang) or svc.get("uz", {})).get("description", key)

    await callback.message.edit_text(
        desc,
        reply_markup=kb_service_detail(lang, key),
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


# ── Buyurtma ─────────────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("order_"))
async def order_prompt(callback: CallbackQuery) -> None:
    user = await _get_registered(callback.from_user.id)
    if not user:
        await callback.answer(t("uz", "not_registered"), show_alert=True)
        return

    lang = user.get("language", "uz")
    key  = callback.data.removeprefix("order_")
    svc  = SERVICES.get(key, {})
    name = (svc.get(lang) or svc.get("uz", {})).get("name", key)

    await callback.message.edit_text(
        t(lang, "confirm_order_prompt", service=name),
        reply_markup=kb_confirm_order(lang, key),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_"))
async def order_confirmed(callback: CallbackQuery, bot: Bot) -> None:
    user = await _get_registered(callback.from_user.id)
    if not user:
        await callback.answer(t("uz", "not_registered"), show_alert=True)
        return

    lang = user.get("language", "uz")
    key  = callback.data.removeprefix("confirm_")
    svc  = SERVICES.get(key, {})
    name = (svc.get(lang) or svc.get("uz", {})).get("name", key)
    now  = datetime.now().strftime("%d.%m.%Y %H:%M")

    await db.save_order(callback.from_user.id, name)

    loc = _location_str(user) or t(lang, "location_not_provided")
    admin_text = t("uz", "admin_new_order",
                   name=user.get("full_name", "—"),
                   phone=user.get("phone", "—"),
                   location=loc, service=name, time=now)
    await _notify_admins(bot, admin_text)

    await callback.message.edit_text(
        t(lang, "order_success", service=name, time=now),
        parse_mode="HTML",
    )
    await callback.message.answer(
        t(lang, "welcome_back", name=user["full_name"]),
        reply_markup=kb_main_menu(lang),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "cancel_order")
async def order_cancelled(callback: CallbackQuery) -> None:
    user = await db.get_user(callback.from_user.id)
    lang = user.get("language", "uz") if user else "uz"

    await callback.message.edit_text(
        t(lang, "order_cancelled") + "\n\n" + t(lang, "services_header"),
        reply_markup=kb_services(lang),
        parse_mode="HTML",
    )
    await callback.answer()

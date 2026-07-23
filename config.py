import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
ADMIN_GROUP_ID: int = int(os.getenv("ADMIN_GROUP_ID", "0"))
ADMIN_IDS: list[int] = [
    int(x.strip())
    for x in os.getenv("ADMIN_IDS", "").split(",")
    if x.strip().isdigit()
]
OPERATOR_PHONE: str = os.getenv("OPERATOR_PHONE", "+998909351177")
DB_PATH: str = "dega_bot.db"

# Xizmatlar identifikatorlari (kalit) — til-neytral
SERVICE_KEYS = [
    "ready_design",
    "need_design",
    "outdoor_ads",
    "furniture",
    "metal_const",
    "turnkey_object",
    "project_calc",
]

# Xizmat ma'lumotlari har uch tilda
SERVICES: dict[str, dict] = {
    "ready_design": {
        "uz": {
            "name": "📐 Menda tayyor dizayn bor (2D/3D)?",
            "description": "<b>📐 Menda tayyor dizayn bor (2D/3D)?</b>",
        },
        "ru": {
            "name": "📐 У меня уже есть готовый дизайн (2D/3D)?",
            "description": "<b>📐 У меня уже есть готовый дизайн (2D/3D)?</b>",
        },
        "en": {
            "name": "📐 I already have a ready design (2D/3D)?",
            "description": "<b>📐 I already have a ready design (2D/3D)?</b>",
        },
    },
    "need_design": {
        "uz": {
            "name": "🎨 Dizayn ishlab chiqish kerak (2D/3D)?",
            "description": "<b>🎨 Dizayn ishlab chiqish kerak (2D/3D)?</b>",
        },
        "ru": {
            "name": "🎨 Нужна разработка дизайна (2D/3D)?",
            "description": "<b>🎨 Нужна разработка дизайна (2D/3D)?</b>",
        },
        "en": {
            "name": "🎨 Need design development (2D/3D)?",
            "description": "<b>🎨 Need design development (2D/3D)?</b>",
        },
    },
    "outdoor_ads": {
        "uz": {
            "name": "📢 Tashqi reklama kerak?",
            "description": "<b>📢 Tashqi reklama kerak?</b>",
        },
        "ru": {
            "name": "📢 Нужна наружная реклама?",
            "description": "<b>📢 Нужна наружная реклама?</b>",
        },
        "en": {
            "name": "📢 Need outdoor advertising?",
            "description": "<b>📢 Need outdoor advertising?</b>",
        },
    },
    "furniture": {
        "uz": {
            "name": "🪑 Mebel yasash kerak?",
            "description": "<b>🪑 Mebel yasash kerak?</b>",
        },
        "ru": {
            "name": "🪑 Нужно изготовление мебели?",
            "description": "<b>🪑 Нужно изготовление мебели?</b>",
        },
        "en": {
            "name": "🪑 Need furniture manufacturing?",
            "description": "<b>🪑 Need furniture manufacturing?</b>",
        },
    },
    "metal_const": {
        "uz": {
            "name": "🔩 Metall konstruksiyalar kerak?",
            "description": "<b>🔩 Metall konstruksiyalar kerak?</b>",
        },
        "ru": {
            "name": "🔩 Нужны металлоконструкции?",
            "description": "<b>🔩 Нужны металлоконструкции?</b>",
        },
        "en": {
            "name": "🔩 Need metal structures?",
            "description": "<b>🔩 Need metal structures?</b>",
        },
    },
    "turnkey_object": {
        "uz": {
            "name": "🏗️ Obyektni kalit topshirishgacha to'liq jihozlash?",
            "description": "<b>🏗️ Obyektni kalit topshirishgacha to'liq jihozlash?</b>",
        },
        "ru": {
            "name": "🏗️ Нужно комплексное оформление объекта под ключ?",
            "description": "<b>🏗️ Нужно комплексное оформление объекта под ключ?</b>",
        },
        "en": {
            "name": "🏗️ Need turnkey complete object decoration?",
            "description": "<b>🏗️ Need turnkey complete object decoration?</b>",
        },
    },
    "project_calc": {
        "uz": {
            "name": "💰 Tayyor loyihani hisoblab berish?",
            "description": "<b>💰 Tayyor loyihani hisoblab berish?</b>",
        },
        "ru": {
            "name": "💰 Вам нужен просчет готового проекта?",
            "description": "<b>💰 Вам нужен просчет готового проекта?</b>",
        },
        "en": {
            "name": "💰 Need a cost calculation for a ready project?",
            "description": "<b>💰 Need a cost calculation for a ready project?</b>",
        },
    },
}
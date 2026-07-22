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
OPERATOR_PHONE: str = os.getenv("OPERATOR_PHONE", "+998 90 000 00 00")
DB_PATH: str = "dega_bot.db"

# Xizmatlar identifikatorlari (kalit) — til-neytral
SERVICE_KEYS = ["ready_project", "design_3d", "designer_2d3d"]

# Xizmat ma'lumotlari har uch tilda
SERVICES: dict[str, dict] = {
    "ready_project": {
        "uz": {
            "name": "Menda tayyor loyiha bor",
            "description": (
                "<b>Tayyor loyiha asosida ishlab chiqarish</b>\n\n"
                "Sizda allaqachon tayyor loyiha hujjatlari mavjudmi? "
                "DEGA jamoasi ularni tahlil qilib, eng qisqa muddatda "
                "ishlab chiqarishga kiritadi.\n\n"
                "Xizmatga nima kiradi:\n"
                "— Loyiha hujjatlarini ko'rib chiqish\n"
                "— Materiallarni tanlash va hisob-kitob\n"
                "— Ishlab chiqarish va yetkazib berish\n\n"
                "Narx: kelishuv asosida"
            ),
        },
        "ru": {
            "name": "У меня есть готовый проект",
            "description": (
                "<b>Производство по готовому проекту</b>\n\n"
                "Если у вас уже есть проектная документация, "
                "команда DEGA изучит её и запустит производство "
                "в кратчайшие сроки.\n\n"
                "Что входит в услугу:\n"
                "— Анализ проектной документации\n"
                "— Подбор материалов и расчёт стоимости\n"
                "— Производство и доставка\n\n"
                "Стоимость: по договорённости"
            ),
        },
        "en": {
            "name": "I have a ready project",
            "description": (
                "<b>Production Based on Your Ready Project</b>\n\n"
                "Already have project documentation? The DEGA team "
                "will review it and launch production in the shortest "
                "possible time.\n\n"
                "Service includes:\n"
                "— Project documentation review\n"
                "— Material selection and cost estimation\n"
                "— Production and delivery\n\n"
                "Price: negotiable"
            ),
        },
    },
    "design_3d": {
        "uz": {
            "name": "Menda 3D dizayn bor",
            "description": (
                "<b>3D dizayn asosida ishlab chiqarish</b>\n\n"
                "Tayyor 3D modelingiz bormi? Uni yuborish kifoya — "
                "DEGA mutaxassislari uni ishlab chiqarish formatiga "
                "o'tkazib, mahsulotni tayyorlaydi.\n\n"
                "Xizmatga nima kiradi:\n"
                "— 3D faylni qabul qilish va tahlil\n"
                "— Ishlab chiqarish uchun moslash\n"
                "— Prototip yoki to'liq partiya\n\n"
                "Narx: kelishuv asosida"
            ),
        },
        "ru": {
            "name": "У меня есть 3D дизайн",
            "description": (
                "<b>Производство по 3D-дизайну</b>\n\n"
                "Есть готовая 3D-модель? Просто отправьте её — "
                "специалисты DEGA адаптируют файл под производство "
                "и изготовят изделие.\n\n"
                "Что входит в услугу:\n"
                "— Приём и анализ 3D-файла\n"
                "— Адаптация под производство\n"
                "— Прототип или серийное производство\n\n"
                "Стоимость: по договорённости"
            ),
        },
        "en": {
            "name": "I have a 3D design",
            "description": (
                "<b>Production Based on Your 3D Design</b>\n\n"
                "Have a ready 3D model? Just send it — DEGA specialists "
                "will adapt the file for production and manufacture "
                "your product.\n\n"
                "Service includes:\n"
                "— 3D file reception and analysis\n"
                "— Adaptation for production\n"
                "— Prototype or full batch production\n\n"
                "Price: negotiable"
            ),
        },
    },
    "designer_2d3d": {
        "uz": {
            "name": "Dizayner xizmati 2D/3D",
            "description": (
                "<b>Professional 2D/3D dizayn xizmati</b>\n\n"
                "Hali loyiha yo'qmi? Muammo emas. DEGA dizaynerlari "
                "g'oyangizni professional 2D chizma yoki 3D modelga "
                "aylantiradi.\n\n"
                "Xizmatga nima kiradi:\n"
                "— Texnik topshiriqni qabul qilish\n"
                "— 2D chizma yoki 3D model yaratish\n"
                "— Muvofiqlash va tuzatish\n"
                "— Ishlab chiqarishga tayyor fayllar\n\n"
                "Narx: kelishuv asosida"
            ),
        },
        "ru": {
            "name": "Услуги дизайнера 2D/3D",
            "description": (
                "<b>Профессиональный 2D/3D дизайн</b>\n\n"
                "Проекта ещё нет? Не проблема. Дизайнеры DEGA "
                "превратят вашу идею в профессиональный 2D-чертёж "
                "или 3D-модель.\n\n"
                "Что входит в услугу:\n"
                "— Получение технического задания\n"
                "— Разработка 2D-чертежа или 3D-модели\n"
                "— Согласование и правки\n"
                "— Готовые файлы для производства\n\n"
                "Стоимость: по договорённости"
            ),
        },
        "en": {
            "name": "2D/3D Designer service",
            "description": (
                "<b>Professional 2D/3D Design Service</b>\n\n"
                "No project yet? No problem. DEGA designers will turn "
                "your idea into a professional 2D drawing or 3D model.\n\n"
                "Service includes:\n"
                "— Technical brief intake\n"
                "— 2D drawing or 3D model creation\n"
                "— Review and revisions\n"
                "— Production-ready files\n\n"
                "Price: negotiable"
            ),
        },
    },
}

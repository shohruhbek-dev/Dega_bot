"""
Barcha interfeys matnlari uch tilda: uz, ru, en.
t(lang, key, **kwargs) funksiyasi orqali ishlatiladi.
"""

TEXTS: dict[str, dict[str, str]] = {

    # ── Til tanlash ─────────────────────────────────────────────────────────
    "choose_language": {
        "uz": "🌐 Iltimos, tilni tanlang:",
        "ru": "🌐 Пожалуйста, выберите язык:",
        "en": "🌐 Please choose your language:",
    },

    # ── Xush kelibsiz / Onboarding ──────────────────────────────────────────
    "welcome": {
        "uz": (
            "DEGA — Metall, Mebel va Reklama Ishlab Chiqarish\n\n"
            "Biz g'oyangizni tayyor mahsulotga aylantiramiz.\n\n"
            "Davom etish uchun ro'yxatdan o'tishingiz kerak.\n"
            "Ism va Familiyangizni kiriting:"
        ),
        "ru": (
            "DEGA — Производство металла, мебели и рекламы\n\n"
            "Мы превращаем вашу идею в готовый продукт.\n\n"
            "Для продолжения необходимо пройти регистрацию.\n"
            "Введите ваше Имя и Фамилию:"
        ),
        "en": (
            "DEGA — Metal, Furniture and Advertising Manufacturing\n\n"
            "We turn your idea into a finished product.\n\n"
            "Please register to continue.\n"
            "Enter your Full Name:"
        ),
    },
    "welcome_back": {
        "uz": "Xush kelibsiz, <b>{name}</b>!\nQuyidagi menyu orqali xizmatlardan foydalaning.",
        "ru": "Добро пожаловать, <b>{name}</b>!\nВоспользуйтесь меню ниже.",
        "en": "Welcome back, <b>{name}</b>!\nUse the menu below to access our services.",
    },
    "ask_full_name": {
        "uz": "Iltimos, <b>Ism va Familiyangizni</b> kiriting:\n<i>(Faqat matn qabul qilinadi)</i>",
        "ru": "Пожалуйста, введите ваше <b>Имя и Фамилию</b>:\n<i>(Принимается только текст)</i>",
        "en": "Please enter your <b>Full Name</b>:\n<i>(Text only)</i>",
    },
    "invalid_name_format": {
        "uz": "Ism-familiya 3 dan 80 gacha belgi bo'lishi kerak. Qaytadan kiriting:",
        "ru": "Имя и фамилия должны содержать от 3 до 80 символов. Попробуйте ещё раз:",
        "en": "Full name must be between 3 and 80 characters. Please try again:",
    },
    "invalid_name_media": {
        "uz": "Faqat <b>matn</b> kiriting. Rasm, ovoz yoki boshqa fayllar qabul qilinmaydi.",
        "ru": "Введите только <b>текст</b>. Фото, голосовые и файлы не принимаются.",
        "en": "Please enter <b>text only</b>. Photos, audio and files are not accepted.",
    },
    "ask_phone": {
        "uz": (
            "Rahmat, <b>{name}</b>!\n\n"
            "Telefon raqamingizni yuboring.\n"
            "Pastdagi tugmani bosing yoki <code>+998XXXXXXXXX</code> formatida yozing:"
        ),
        "ru": (
            "Спасибо, <b>{name}</b>!\n\n"
            "Отправьте ваш номер телефона.\n"
            "Нажмите кнопку ниже или введите в формате <code>+998XXXXXXXXX</code>:"
        ),
        "en": (
            "Thank you, <b>{name}</b>!\n\n"
            "Please share your phone number.\n"
            "Tap the button below or type it in <code>+998XXXXXXXXX</code> format:"
        ),
    },
    "invalid_phone": {
        "uz": "Noto'g'ri format. Raqamni <code>+998901234567</code> ko'rinishida kiriting:",
        "ru": "Неверный формат. Введите номер в виде <code>+998901234567</code>:",
        "en": "Invalid format. Enter the number as <code>+998901234567</code>:",
    },
    "invalid_phone_media": {
        "uz": "Telefon raqamini yuboring yoki <b>📱 Raqamni ulashish</b> tugmasini bosing.",
        "ru": "Отправьте номер телефона или нажмите <b>📱 Поделиться номером</b>.",
        "en": "Send your phone number or tap <b>📱 Share Contact</b>.",
    },
    "ask_location": {
        "uz": (
            "Telefon saqlandi: <code>{phone}</code>\n\n"
            "Joylashuvingizni yuboring yoki o'tkazib yuboring:"
        ),
        "ru": (
            "Номер сохранён: <code>{phone}</code>\n\n"
            "Отправьте своё местоположение или пропустите:"
        ),
        "en": (
            "Phone saved: <code>{phone}</code>\n\n"
            "Share your location or skip this step:"
        ),
    },
    "invalid_location": {
        "uz": "<b>📍 Lokatsiyani yuborish</b> tugmasini bosing yoki <b>O'tkazib yuborish</b> tanlang.",
        "ru": "Нажмите <b>📍 Отправить местоположение</b> или выберите <b>Пропустить</b>.",
        "en": "Tap <b>📍 Share Location</b> or choose <b>Skip</b>.",
    },
    "registration_done": {
        "uz": (
            "Ro'yxatdan o'tish yakunlandi.\n\n"
            "Ism: {name}\n"
            "Tel: {phone}\n"
            "Joylashuv: {location}\n\n"
            "Xizmatlardan foydalanishingiz mumkin."
        ),
        "ru": (
            "Регистрация завершена.\n\n"
            "Имя: {name}\n"
            "Тел: {phone}\n"
            "Местоположение: {location}\n\n"
            "Вы можете пользоваться нашими услугами."
        ),
        "en": (
            "Registration complete.\n\n"
            "Name: {name}\n"
            "Phone: {phone}\n"
            "Location: {location}\n\n"
            "You may now use our services."
        ),
    },
    "location_not_provided": {
        "uz": "Ko'rsatilmagan",
        "ru": "Не указано",
        "en": "Not provided",
    },

    # ── Asosiy menyu tugmalari ───────────────────────────────────────────────
    "btn_services": {
        "uz": "Xizmatlar",
        "ru": "Услуги",
        "en": "Services",
    },
    "btn_operator": {
        "uz": "Operator bilan bog'lanish",
        "ru": "Связаться с оператором",
        "en": "Contact Operator",
    },
    "btn_profile": {
        "uz": "Profilim",
        "ru": "Мой профиль",
        "en": "My Profile",
    },
    "btn_about": {
        "uz": "Biz haqimizda",
        "ru": "О нас",
        "en": "About Us",
    },

    # ── Xizmatlar ────────────────────────────────────────────────────────────
    "services_header": {
        "uz": "<b>DEGA xizmatlari</b>\n\nQuyidagi yo'nalishlardan birini tanlang:",
        "ru": "<b>Услуги DEGA</b>\n\nВыберите одно из направлений:",
        "en": "<b>DEGA Services</b>\n\nChoose one of the options below:",
    },
    "btn_order": {
        "uz": "Buyurtma berish",
        "ru": "Оформить заказ",
        "en": "Place Order",
    },
    "btn_back": {
        "uz": "Orqaga",
        "ru": "Назад",
        "en": "Back",
    },
    "btn_back_menu": {
        "uz": "Bosh menyuga",
        "ru": "Главное меню",
        "en": "Main Menu",
    },
    "confirm_order_prompt": {
        "uz": "<b>{service}</b> xizmatiga buyurtma berishni tasdiqlaysizmi?",
        "ru": "Подтверждаете заказ на услугу <b>{service}</b>?",
        "en": "Do you confirm your order for <b>{service}</b>?",
    },
    "btn_confirm_yes": {
        "uz": "Ha, tasdiqlаyman",
        "ru": "Да, подтверждаю",
        "en": "Yes, confirm",
    },
    "btn_cancel": {
        "uz": "Bekor qilish",
        "ru": "Отменить",
        "en": "Cancel",
    },
    "order_success": {
        "uz": (
            "Buyurtmangiz qabul qilindi.\n\n"
            "Xizmat: {service}\n"
            "Vaqt: {time}\n\n"
            "Mutaxassisimiz tez orada siz bilan bog'lanadi."
        ),
        "ru": (
            "Ваш заказ принят.\n\n"
            "Услуга: {service}\n"
            "Время: {time}\n\n"
            "Наш специалист свяжется с вами в ближайшее время."
        ),
        "en": (
            "Your order has been received.\n\n"
            "Service: {service}\n"
            "Time: {time}\n\n"
            "Our specialist will contact you shortly."
        ),
    },
    "order_cancelled": {
        "uz": "Buyurtma bekor qilindi.",
        "ru": "Заказ отменён.",
        "en": "Order cancelled.",
    },

    # ── Operator ─────────────────────────────────────────────────────────────
    "operator_message": {
        "uz": (
            "<b>Operator bilan bog'lanish</b>\n\n"
            "Telefon: <code>{phone}</code>\n"
            "Ish vaqti: Du–Sha, 09:00–18:00\n\n"
            "So'rovingiz adminlarga yuborildi. Tez orada murojaat qilamiz."
        ),
        "ru": (
            "<b>Связаться с оператором</b>\n\n"
            "Телефон: <code>{phone}</code>\n"
            "Время работы: Пн–Пт, 09:00–18:00\n\n"
            "Ваш запрос отправлен администраторам. Мы свяжемся с вами."
        ),
        "en": (
            "<b>Contact Operator</b>\n\n"
            "Phone: <code>{phone}</code>\n"
            "Working hours: Mon–Sat, 09:00–18:00\n\n"
            "Your request has been forwarded to our team. We will contact you soon."
        ),
    },

    # ── Profil ───────────────────────────────────────────────────────────────
    "profile_text": {
        "uz": (
            "<b>Mening profilim</b>\n\n"
            "Ism-Familiya: {name}\n"
            "Telefon: <code>{phone}</code>\n"
            "Joylashuv: {location}\n"
            "Til: {language}\n"
            "Ro'yxatdan o'tgan: {date}"
        ),
        "ru": (
            "<b>Мой профиль</b>\n\n"
            "Имя и фамилия: {name}\n"
            "Телефон: <code>{phone}</code>\n"
            "Местоположение: {location}\n"
            "Язык: {language}\n"
            "Дата регистрации: {date}"
        ),
        "en": (
            "<b>My Profile</b>\n\n"
            "Full Name: {name}\n"
            "Phone: <code>{phone}</code>\n"
            "Location: {location}\n"
            "Language: {language}\n"
            "Registered: {date}"
        ),
    },
    "btn_re_register": {
        "uz": "Qayta ro'yxatdan o'tish",
        "ru": "Перерегистрация",
        "en": "Re-register",
    },
    "btn_change_lang": {
        "uz": "Tilni o'zgartirish",
        "ru": "Изменить язык",
        "en": "Change Language",
    },
    "lang_changed": {
        "uz": "Til o'zgartirildi.",
        "ru": "Язык изменён.",
        "en": "Language changed.",
    },
    "lang_display": {
        "uz": "O'zbekcha",
        "ru": "Русский",
        "en": "English",
    },

    # ── Biz haqimizda ────────────────────────────────────────────────────────
    "about_text": {
        "uz": (
            "<b>DEGA — Ishlab Chiqarish Kompaniyasi</b>\n\n"
            "Biz metall konstruksiyalar, zamonaviy mebel va reklama "
            "mahsulotlari ishlab chiqarish sohasida faoliyat yuritamiz.\n\n"
            "Manzil: Toshkent shahri\n"
            "Telefon: +998 90 000 00 00\n"
            "Ish vaqti: Du–Sha, 09:00–18:00\n\n"
            "Instagram: @dega_production\n"
            "Telegram: @dega_official"
        ),
        "ru": (
            "<b>DEGA — Производственная компания</b>\n\n"
            "Мы специализируемся на производстве металлоконструкций, "
            "современной мебели и рекламной продукции.\n\n"
            "Адрес: г. Ташкент\n"
            "Телефон: +998 90 000 00 00\n"
            "Время работы: Пн–Пт, 09:00–18:00\n\n"
            "Instagram: @dega_production\n"
            "Telegram: @dega_official"
        ),
        "en": (
            "<b>DEGA — Manufacturing Company</b>\n\n"
            "We specialize in metal structures, modern furniture "
            "and advertising product manufacturing.\n\n"
            "Address: Tashkent city\n"
            "Phone: +998 90 000 00 00\n"
            "Working hours: Mon–Sat, 09:00–18:00\n\n"
            "Instagram: @dega_production\n"
            "Telegram: @dega_official"
        ),
    },

    # ── Ro'yxatdan o'tish talab qilinadi ─────────────────────────────────────
    "not_registered": {
        "uz": "Davom etish uchun avval ro'yxatdan o'ting. /start",
        "ru": "Для продолжения сначала пройдите регистрацию. /start",
        "en": "Please register first to continue. /start",
    },

    # ── Admin — guruhga tushuvchi xabarlar ───────────────────────────────────
    "admin_new_order": {
        "uz": (
            "YANGI BUYURTMA\n\n"
            "Mijoz: {name}\n"
            "Telefon: {phone}\n"
            "Joylashuv: {location}\n"
            "Xizmat: {service}\n"
            "Vaqt: {time}"
        ),
        "ru": (
            "НОВЫЙ ЗАКАЗ\n\n"
            "Клиент: {name}\n"
            "Телефон: {phone}\n"
            "Местоположение: {location}\n"
            "Услуга: {service}\n"
            "Время: {time}"
        ),
        "en": (
            "NEW ORDER\n\n"
            "Client: {name}\n"
            "Phone: {phone}\n"
            "Location: {location}\n"
            "Service: {service}\n"
            "Time: {time}"
        ),
    },
    "admin_operator_request": {
        "uz": (
            "OPERATOR SO'ROVI\n\n"
            "Mijoz: {name}\n"
            "Telefon: {phone}\n"
            "Joylashuv: {location}\n"
            "Vaqt: {time}"
        ),
        "ru": (
            "ЗАПРОС ОПЕРАТОРА\n\n"
            "Клиент: {name}\n"
            "Телефон: {phone}\n"
            "Местоположение: {location}\n"
            "Время: {time}"
        ),
        "en": (
            "OPERATOR REQUEST\n\n"
            "Client: {name}\n"
            "Phone: {phone}\n"
            "Location: {location}\n"
            "Time: {time}"
        ),
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """
    Tarjimani qaytaradi. Agar kalit topilmasa — uz tilida qaytaradi.
    kwargs orqali o'zgaruvchilar formatlanadi.
    """
    lang = lang if lang in ("uz", "ru", "en") else "uz"
    block = TEXTS.get(key, {})
    text = block.get(lang) or block.get("uz", f"[{key}]")
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text

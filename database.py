import aiosqlite
import logging
from config import DB_PATH

logger = logging.getLogger(__name__)


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id     INTEGER PRIMARY KEY,
                username    TEXT,
                full_name   TEXT,
                phone       TEXT,
                latitude    REAL,
                longitude   REAL,
                language    TEXT DEFAULT 'uz',
                registered  INTEGER DEFAULT 0,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Mavjud bazaga language ustunini qo'shish (eski bazalar uchun)
        try:
            await db.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'uz'")
        except Exception:
            pass

        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER NOT NULL,
                service_name TEXT NOT NULL,
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        await db.commit()
    logger.info("Ma'lumotlar bazasi tayyor.")


async def upsert_user(
    user_id: int,
    username: str | None = None,
    full_name: str | None = None,
    phone: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    language: str | None = None,
    registered: int | None = None,
) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        # Mavjudlikni tekshirish
        async with db.execute(
            "SELECT user_id FROM users WHERE user_id = ?", (user_id,)
        ) as cur:
            exists = await cur.fetchone()

        if not exists:
            await db.execute(
                """INSERT INTO users
                   (user_id, username, full_name, phone, latitude, longitude, language, registered)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    user_id,
                    username,
                    full_name,
                    phone,
                    latitude,
                    longitude,
                    language or "uz",
                    registered if registered is not None else 0,
                ),
            )
        else:
            # Faqat None bo'lmagan qiymatlarni yangilash
            fields, values = [], []
            if username is not None:
                fields.append("username = ?"); values.append(username)
            if full_name is not None:
                fields.append("full_name = ?"); values.append(full_name)
            if phone is not None:
                fields.append("phone = ?"); values.append(phone)
            if latitude is not None:
                fields.append("latitude = ?"); values.append(latitude)
            if longitude is not None:
                fields.append("longitude = ?"); values.append(longitude)
            if language is not None:
                fields.append("language = ?"); values.append(language)
            if registered is not None:
                fields.append("registered = ?"); values.append(registered)

            if fields:
                values.append(user_id)
                await db.execute(
                    f"UPDATE users SET {', '.join(fields)} WHERE user_id = ?",
                    values,
                )
        await db.commit()


async def get_user(user_id: int) -> dict | None:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        ) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def get_all_users() -> list[dict]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM users ORDER BY created_at DESC"
        ) as cur:
            return [dict(r) for r in await cur.fetchall()]


async def get_registered_user_ids() -> list[int]:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT user_id FROM users WHERE registered = 1"
        ) as cur:
            return [row[0] for row in await cur.fetchall()]


async def save_order(user_id: int, service_name: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO orders (user_id, service_name) VALUES (?, ?)",
            (user_id, service_name),
        )
        await db.commit()


async def get_orders_with_users() -> list[dict]:
    """orders va users jadvalini LEFT JOIN qilib barcha buyurtmalarni olish."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT
                o.id,
                u.user_id,
                u.username,
                u.full_name,
                u.phone,
                u.latitude,
                u.longitude,
                o.service_name,
                u.registered,
                o.created_at
            FROM orders o
            LEFT JOIN users u ON o.user_id = u.user_id
            ORDER BY o.created_at DESC
        """) as cur:
            return [dict(r) for r in await cur.fetchall()]


async def reset_user(user_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE users
            SET full_name = NULL,
                phone = NULL,
                latitude = NULL,
                longitude = NULL,
                registered = 0
            WHERE user_id = ?
        """, (user_id,))
        await db.commit()


async def update_user_language(user_id: int, language: str) -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE users SET language = ? WHERE user_id = ?",
            (language, user_id),
        )
        await db.commit()

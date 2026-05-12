import aiosqlite
import logging
from datetime import datetime

logger = logging.getLogger("SyncBot.Database")

# Ruta al archivo de base de datos SQLite
DB_PATH = "db/data.db"


async def init_db():
    """
    Inicializa la base de datos creando las tablas necesarias si no existen.
    Esta función debe llamarse al iniciar el bot.
    """
    logger.info("Verificando la base de datos...")

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS standups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT NOT NULL,
                task_description TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS bot_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                description TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await db.commit()

    logger.info("Base de datos verificada correctamente.")


async def add_standup(user_id: int, username: str, task: str):
    """
    Guarda el reporte diario de un usuario en la base de datos.

    Args:
        user_id (int): ID de Discord del usuario.
        username (str): Nombre del usuario.
        task (str): Descripción de la tarea reportada.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO standups (user_id, username, task_description)
            VALUES (?, ?, ?)
        """, (user_id, username, task))

        await db.commit()

    logger.info(f"Standup registrado para el usuario {username}.")


async def get_all_standups():
    """
    Retorna todos los reportes diarios registrados.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
            SELECT id, user_id, username, task_description, timestamp
            FROM standups
            ORDER BY timestamp DESC
        """)

        rows = await cursor.fetchall()

    return [dict(row) for row in rows]


async def get_standups_by_user(user_id: int):
    """
    Retorna todos los reportes diarios registrados por un usuario específico.

    Args:
        user_id (int): ID de Discord del usuario.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
            SELECT id, user_id, username, task_description, timestamp
            FROM standups
            WHERE user_id = ?
            ORDER BY timestamp DESC
        """, (user_id,))

        rows = await cursor.fetchall()

    return [dict(row) for row in rows]


async def get_last_standup_by_user(user_id: int):
    """
    Retorna el último reporte diario registrado por un usuario.

    Args:
        user_id (int): ID de Discord del usuario.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
            SELECT id, user_id, username, task_description, timestamp
            FROM standups
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 1
        """, (user_id,))

        row = await cursor.fetchone()

    return dict(row) if row else None


async def count_standups():
    """
    Retorna la cantidad total de reportes diarios registrados.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT COUNT(*) 
            FROM standups
        """)

        result = await cursor.fetchone()

    return result[0]


async def count_standups_by_user(user_id: int):
    """
    Retorna la cantidad de reportes diarios registrados por un usuario.

    Args:
        user_id (int): ID de Discord del usuario.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT COUNT(*)
            FROM standups
            WHERE user_id = ?
        """, (user_id,))

        result = await cursor.fetchone()

    return result[0]


async def delete_standup(standup_id: int):
    """
    Elimina un reporte diario por su ID.

    Args:
        standup_id (int): ID del reporte diario.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            DELETE FROM standups
            WHERE id = ?
        """, (standup_id,))

        await db.commit()

    return cursor.rowcount > 0


async def add_bot_log(action: str, description: str):
    """
    Guarda una acción importante realizada por el bot.

    Args:
        action (str): Nombre de la acción realizada.
        description (str): Descripción de la acción.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO bot_logs (action, description)
            VALUES (?, ?)
        """, (action, description))

        await db.commit()

    logger.info(f"Log registrado: {action}")


async def get_bot_logs():
    """
    Retorna los logs registrados por el bot.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row

        cursor = await db.execute("""
            SELECT id, action, description, timestamp
            FROM bot_logs
            ORDER BY timestamp DESC
        """)

        rows = await cursor.fetchall()

    return [dict(row) for row in rows]
import aiosqlite
import logging
from datetime import datetime

logger = logging.getLogger('SyncBot.Database')

# Ruta al archivo de base de datos SQLite
DB_PATH = "db/data.db"

async def init_db():
    """
    Inicializa la base de datos creando las tablas necesarias si no existen.
    Esta función debe llamarse al iniciar el bot.
    """
    logger.info("Verificando la base de datos...")
    
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS standups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                task_description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def add_standup(user_id: int, username: str, task: str):
    """
    Guarda el reporte diario de un usuario en la base de datos.
    
    Args:
        user_id (int): El ID de Discord del usuario.
        username (str): El nombre a mostrar del usuario.
        task (str): La tarea en la que está trabajando.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            INSERT INTO standups (user_id, username, task_description)
            VALUES (?, ?, ?)
        ''', (user_id, username, task))
        await db.commit()

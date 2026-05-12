import aiosqlite
import logging

logger = logging.getLogger('SyncBot.Database')

# Ruta al archivo de base de datos SQLite
DB_PATH = "db/data.db"

async def init_db():
    \"\"\"
    Inicializa la base de datos creando las tablas necesarias si no existen.
    Esta función debe llamarse al iniciar el bot.
    \"\"\"
    logger.info("Verificando la base de datos...")
    
    # 📌 INTEGRANTE 2 (Data Master):
    # Aquí debes crear la tabla 'standups' si no existe.
    # Necesitas campos como: id, user_id, task_description, timestamp
    
    # Ejemplo de uso con aiosqlite (conexión asíncrona a SQLite):
    # async with aiosqlite.connect(DB_PATH) as db:
    #     await db.execute('''
    #         CREATE TABLE IF NOT EXISTS ...
    #     ''')
    #     await db.commit()
    
    pass

async def add_standup(user_id: int, task: str):
    \"\"\"
    Guarda el reporte diario de un usuario en la base de datos.
    
    Args:
        user_id (int): El ID de Discord del usuario.
        task (str): La tarea en la que está trabajando.
    \"\"\"
    # 📌 INTEGRANTE 2 (Data Master):
    # Aquí debes insertar los datos en la base de datos.
    pass

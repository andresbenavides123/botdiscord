import discord
from discord.ext import commands
import logging
import os
import asyncio

from core.config import config
from db.database import init_db

# Configurar el sistema de logging para ver qué ocurre en el bot y atrapar errores
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('SyncBot')


class SyncBot(commands.Bot):
    def __init__(self):
        # Configurar los "intents", que son los permisos que Discord le da al bot
        # para leer mensajes, miembros del servidor, etc.
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=config.COMMAND_PREFIX,
            intents=intents,
            help_command=None  # Desactivamos el help por defecto para crear el nuestro en cogs/support.py
        )

    async def setup_hook(self):
        """
        Este método se ejecuta antes de que el bot se conecte a Discord.
        Aquí inicializamos la base de datos y cargamos dinámicamente todos los Cogs.
        """
        try:
            await init_db()
            logger.info("Base de datos inicializada correctamente.")
        except Exception as e:
            logger.error(f"Error inicializando la base de datos: {e}")
            raise

        cogs_dir = './cogs'
        if not os.path.exists(cogs_dir):
            os.makedirs(cogs_dir)
            logger.info(f"Directorio '{cogs_dir}' creado.")

        # Recorremos los archivos de la carpeta cogs
        for filename in os.listdir(cogs_dir):
            if filename.endswith('.py'):
                # Convertimos 'cogs/ejemplo.py' a 'cogs.ejemplo'
                cog_path = f'cogs.{filename[:-3]}'
                try:
                    await self.load_extension(cog_path)
                    logger.info(f"Cog cargado correctamente: {cog_path}")
                except Exception as e:
                    logger.error(f"Error cargando el cog {cog_path}: {e}")

    async def on_ready(self):
        """Evento que se dispara cuando el bot está conectado y listo"""
        logger.info(f'¡Bot conectado exitosamente como {self.user.name} (ID: {self.user.id})!')
        logger.info('Listo para sincronizar el trabajo del equipo.')


# Bloque principal de ejecución
if __name__ == '__main__':
    bot = SyncBot()

    try:
        # Iniciamos el bot con el token obtenido de las variables de entorno
        bot.run(config.DISCORD_TOKEN)
    except Exception as e:
        logger.critical(f"Error crítico al iniciar el bot: {e}")
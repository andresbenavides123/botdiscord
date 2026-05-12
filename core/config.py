import os
from dotenv import load_dotenv

# Cargar variables del archivo .env al entorno
load_dotenv()

class Config:
    """
    Clase centralizada para manejar la configuración del bot.
    Esto permite tener todas las variables de entorno validadas en un solo lugar.
    """
    
    # Token principal del bot (requerido)
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    if not DISCORD_TOKEN:
        raise ValueError("No se ha encontrado DISCORD_TOKEN en el archivo .env")

    # Prefijo del bot, por defecto '!'
    COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

    # ID del canal de bitácora (opcional, útil para el standup)
    LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")
    if LOG_CHANNEL_ID:
        try:
            LOG_CHANNEL_ID = int(LOG_CHANNEL_ID)
        except ValueError:
            print("Advertencia: LOG_CHANNEL_ID debe ser un número entero válido.")
            LOG_CHANNEL_ID = None

config = Config()

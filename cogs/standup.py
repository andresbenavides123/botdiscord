import discord
from discord.ext import commands
import logging

logger = logging.getLogger('SyncBot.Standup')

class StandupCog(commands.Cog):
    \"\"\"
    Módulo para manejar la bitácora diaria (Stand-up) del equipo.
    A cargo de: Integrante 2 (The Data Master)
    \"\"\"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='daily')
    async def daily_standup(self, ctx: commands.Context, *, task: str = None):
        \"\"\"
        Comando para reportar la tarea del día.
        Uso: !daily [Lo que voy a hacer hoy]
        \"\"\"
        if not task:
            await ctx.send("❌ Por favor, indica en qué vas a trabajar. Ejemplo: `!daily Crear la base de datos`")
            return

        # 📌 INTEGRANTE 2 (Data Master): Tareas a realizar aquí
        # 1. Borrar el mensaje original del usuario para mantener limpio el chat.
        #    Tip: await ctx.message.delete()
        #
        # 2. Guardar el reporte en la base de datos (usar funciones de db/database.py).
        #
        # 3. Crear un Embed bonito (discord.Embed) resumiendo lo que el dev hará hoy.
        #
        # 4. Enviar ese Embed a un canal específico (ej. usando config.LOG_CHANNEL_ID o en el mismo canal).

        # Mensaje temporal mientras se construye el comando:
        embed = discord.Embed(
            title="🛠️ Comando en Construcción",
            description=f"**{ctx.author.display_name}** quiere reportar: `{task}`\n\n*(El Data Master pronto conectará esto a la base de datos)*",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    \"\"\"
    Función requerida por discord.py para cargar este archivo como extensión.
    \"\"\"
    await bot.add_cog(StandupCog(bot))

import discord
from discord.ext import commands
import logging

logger = logging.getLogger('SyncBot.Support')

class SupportCog(commands.Cog):
    \"\"\"
    Módulo para manejar emergencias y ayuda general.
    A cargo de: Integrante 4 (The Support Engineer)
    \"\"\"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='sos')
    async def request_help(self, ctx: commands.Context, *, problem: str = None):
        \"\"\"
        Solicita ayuda al resto del equipo que no esté en modo concentración.
        Uso: !sos [descripción del problema]
        \"\"\"
        if not problem:
            await ctx.send("❌ Por favor describe tu problema. Ejemplo: `!sos No me conecta la base de datos`")
            return

        # 📌 INTEGRANTE 4 (Support Engineer): Tareas a realizar aquí
        # 1. Iterar sobre todos los miembros del servidor (ctx.guild.members).
        # 2. Filtrar a los miembros que NO tengan el rol "En la Zona 🎧" y que NO sean bots.
        # 3. Construir una mención conjunta o un mensaje de alerta dirigido a los disponibles.
        # 4. Opcional: Crear un canal de voz temporal para Pair Programming o simplemente 
        #    enviar un mensaje llamando a los devs libres a un canal existente.

        # Mensaje temporal mientras se construye el comando:
        embed = discord.Embed(
            title="🚨 Comando en Construcción",
            description=f"**{ctx.author.display_name}** pide auxilio: `{problem}`\n\n*(El Support Engineer pronto habilitará las sirenas de emergencia)*",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @commands.command(name='help')
    async def custom_help(self, ctx: commands.Context):
        \"\"\"
        Muestra la lista de comandos disponibles. Sobrescribe el help por defecto.
        \"\"\"
        # 📌 INTEGRANTE 4 (Support Engineer): Tareas a realizar aquí
        # 1. Crear un discord.Embed con un título como "Guía de Supervivencia Dev-HQ".
        # 2. Añadir campos (embed.add_field) explicando cómo usar !daily, !focus y !sos.
        # 3. Darle un toque estético (colores, emojis, thumbnails).
        # 4. Enviar el embed al canal.

        # Mensaje temporal mientras se construye el comando:
        embed = discord.Embed(
            title="📖 Comando en Construcción",
            description="El Support Engineer está redactando el manual. ¡Vuelve pronto!",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    \"\"\"
    Función requerida por discord.py para cargar este archivo como extensión.
    \"\"\"
    await bot.add_cog(SupportCog(bot))

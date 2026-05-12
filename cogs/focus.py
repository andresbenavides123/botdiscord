import discord
from discord.ext import commands
import asyncio
import logging

logger = logging.getLogger('SyncBot.Focus')

class FocusCog(commands.Cog):
    \"\"\"
    Módulo para manejar el tiempo de trabajo profundo (Pomodoro).
    A cargo de: Integrante 3 (The Time Keeper)
    \"\"\"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='focus')
    async def focus_mode(self, ctx: commands.Context, minutes: int = 25):
        \"\"\"
        Inicia un temporizador de concentración.
        Uso: !focus [minutos]
        \"\"\"
        if minutes <= 0 or minutes > 120:
            await ctx.send("❌ Por favor indica un tiempo válido (entre 1 y 120 minutos).")
            return

        # 📌 INTEGRANTE 3 (Time Keeper): Tareas a realizar aquí
        # 1. Obtener o crear un rol llamado "En la Zona 🎧" en el servidor.
        #    Tip: discord.utils.get(ctx.guild.roles, name="En la Zona 🎧")
        #
        # 2. Asignar ese rol al usuario (ctx.author.add_roles).
        #
        # 3. Avisar al canal que el usuario ha entrado en modo concentración.
        #
        # 4. Pausar la ejecución asíncrona de ESTA función (¡Sin bloquear el resto del bot!)
        #    Tip: await asyncio.sleep(minutes * 60)
        #
        # 5. Pasado el tiempo, remover el rol (ctx.author.remove_roles).
        #
        # 6. Enviar un mensaje directo (DM) al usuario avisando que el tiempo terminó.
        #    Tip: await ctx.author.send("¡Tiempo terminado!")

        # Mensaje temporal mientras se construye el comando:
        embed = discord.Embed(
            title="⏱️ Comando en Construcción",
            description=f"El Time Keeper está configurando los cronómetros.\nPronto podré aislarte por **{minutes} minutos**.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    \"\"\"
    Función requerida por discord.py para cargar este archivo como extensión.
    \"\"\"
    await bot.add_cog(FocusCog(bot))

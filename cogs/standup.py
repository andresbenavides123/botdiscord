import discord
from discord.ext import commands
import logging
from db.database import add_standup

logger = logging.getLogger('SyncBot.Standup')

class StandupCog(commands.Cog):
    """
    Módulo para manejar la bitácora diaria (Stand-up) del equipo.
    A cargo de: Integrante 2 (The Data Master)
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='daily')
    async def daily_standup(self, ctx: commands.Context, *, task: str = None):
        """
        Comando para reportar la tarea del día.
        Uso: !daily [Lo que voy a hacer hoy]
        """
        if not task:
            await ctx.send("❌ Por favor, indica en qué vas a trabajar. Ejemplo: `!daily Crear la base de datos`")
            return

        # 1. Borrar el mensaje original del usuario para mantener limpio el chat.
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            logger.warning(f"No se pudo borrar el mensaje de {ctx.author.name} (Falta de permisos).")
        except discord.NotFound:
            pass # El mensaje ya no existe
        except Exception as e:
            logger.error(f"Error al borrar mensaje: {e}")

        # 2. Guardar el reporte en la base de datos.
        await add_standup(ctx.author.id, ctx.author.display_name, task)

        # 3. Crear un Embed bonito resumiendo lo que el dev hará hoy.
        embed = discord.Embed(
            title="🌅 Reporte Diario (Stand-up)",
            description=f"**{ctx.author.display_name}** ha registrado su tarea para hoy.",
            color=discord.Color.green()
        )
        embed.add_field(name="📋 Tarea", value=f"> {task}", inline=False)
        embed.set_footer(text="Data Master Bot • Stand-up Asíncrono")
        
        # Añadir el avatar del usuario si lo tiene
        if ctx.author.display_avatar:
            embed.set_thumbnail(url=ctx.author.display_avatar.url)

        # 4. Enviar ese Embed a un canal específico llamado #bitacora.
        bitacora_channel = discord.utils.get(ctx.guild.channels, name="bitacora")
        
        if bitacora_channel:
            await bitacora_channel.send(embed=embed)
        else:
            # Si no existe #bitacora, lo enviamos al canal actual advirtiendo
            await ctx.send("⚠️ Canal `#bitacora` no encontrado. Mostrando reporte aquí:", embed=embed)

async def setup(bot: commands.Bot):
    """
    Función requerida por discord.py para cargar este archivo como extensión.
    """
    await bot.add_cog(StandupCog(bot))

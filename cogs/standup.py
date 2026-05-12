import discord
from discord.ext import commands
import logging

from db.database import add_standup, add_bot_log

logger = logging.getLogger("SyncBot.Standup")


class StandupCog(commands.Cog):
    """
    Módulo para manejar la bitácora diaria tipo Stand-up del equipo.
    A cargo de: Integrante encargado de Database / Data Master.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="daily")
    async def daily_standup(self, ctx: commands.Context, *, task: str = None):
        """
        Comando para reportar la tarea del día.

        Uso:
        !daily Crear la base de datos
        """
        if not task or not task.strip():
            await ctx.send(
                "❌ Por favor, indica en qué vas a trabajar.\n"
                "Ejemplo: `!daily Crear la base de datos`"
            )
            return

        task = task.strip()

        # 1. Borrar el mensaje original del usuario para mantener limpio el chat.
        try:
            await ctx.message.delete()

        except discord.Forbidden:
            logger.warning(
                f"No se pudo borrar el mensaje de {ctx.author.name} por falta de permisos."
            )

        except discord.NotFound:
            pass

        except Exception as error:
            logger.error(f"Error al borrar mensaje: {error}")

        # 2. Guardar el reporte en la base de datos.
        try:
            await add_standup(
                user_id=ctx.author.id,
                username=ctx.author.display_name,
                task=task
            )

            await add_bot_log(
                action="STANDUP_CREATED",
                description=f"{ctx.author.display_name} registró un stand-up diario."
            )

            logger.info(
                f"Stand-up guardado correctamente para {ctx.author.display_name}."
            )

        except Exception as error:
            logger.error(f"Error al guardar el stand-up en la base de datos: {error}")

            await ctx.send(
                "❌ Ocurrió un error al guardar tu reporte en la base de datos. "
                "Intenta nuevamente más tarde."
            )
            return

        # 3. Crear un Embed resumiendo lo que el usuario hará hoy.
        embed = discord.Embed(
            title="🌅 Reporte Diario (Stand-up)",
            description=f"**{ctx.author.display_name}** ha registrado su tarea para hoy.",
            color=discord.Color.green()
        )

        embed.add_field(
            name="📋 Tarea",
            value=f"> {task}",
            inline=False
        )

        embed.add_field(
            name="💾 Estado",
            value="Reporte guardado correctamente en la base de datos.",
            inline=False
        )

        embed.set_footer(text="Data Master Bot • Stand-up Asíncrono")

        if ctx.author.display_avatar:
            embed.set_thumbnail(url=ctx.author.display_avatar.url)

        # 4. Enviar el Embed al canal #bitacora.
        bitacora_channel = discord.utils.get(ctx.guild.channels, name="bitacora")

        if bitacora_channel:
            await bitacora_channel.send(embed=embed)
        else:
            await ctx.send(
                "⚠️ Canal `#bitacora` no encontrado. Mostrando reporte aquí:",
                embed=embed
            )


async def setup(bot: commands.Bot):
    """
    Función requerida por discord.py para cargar este archivo como extensión.
    """
    await bot.add_cog(StandupCog(bot))
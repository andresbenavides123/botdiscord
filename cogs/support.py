import discord
from discord.ext import commands
import logging

logger = logging.getLogger('SyncBot.Support')

class SupportCog(commands.Cog):
    """
    Módulo para manejar emergencias y ayuda general.
    A cargo de: Integrante 4 (The Support Engineer)
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='sos')
    async def request_help(self, ctx: commands.Context, *, problem: str = None):
        """
        Solicita ayuda al resto del equipo que no esté en modo concentración.
        Uso: !sos [descripción del problema]
        """
        if not problem:
            await ctx.send("❌ Por favor describe tu problema. Ejemplo: `!sos No me conecta la base de datos`")
            return

        # Buscar el rol "En la Zona 🎧" en el servidor
        zona_role = discord.utils.get(ctx.guild.roles, name="En la Zona 🎧")

        # Filtrar miembros que NO tienen el rol "En la Zona 🎧", que no son bots
        # y que no son quien pidió el SOS
        disponibles = [
            member for member in ctx.guild.members
            if not member.bot
            and member != ctx.author
            and (zona_role is None or zona_role not in member.roles)
        ]

        if not disponibles:
            embed = discord.Embed(
                title="😔 Nadie disponible",
                description="Todo el equipo está en modo concentración o no hay nadie conectado.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        # Enviar DM a cada miembro disponible
        notificados = []
        for member in disponibles:
            try:
                dm_embed = discord.Embed(
                    title="🚨 ¡Alguien necesita ayuda!",
                    description=(
                        f"**{ctx.author.display_name}** está pidiendo auxilio en **{ctx.guild.name}**:\n\n"
                        f"💬 **Problema:** {problem}\n\n"
                        f"🎙️ ¡Salta a un canal de voz para hacer Pair Programming!"
                    ),
                    color=discord.Color.red()
                )
                dm_embed.set_footer(text=f"Solicitud enviada desde #{ctx.channel.name}")
                dm_embed.set_thumbnail(url=ctx.author.display_avatar.url)
                await member.send(embed=dm_embed)
                notificados.append(member.display_name)
            except discord.Forbidden:
                # El usuario tiene los DMs cerrados
                logger.warning(f"No se pudo enviar DM a {member.display_name} (DMs cerrados)")

        # Confirmar en el canal quién fue notificado
        menciones = " ".join([m.mention for m in disponibles])
        confirmacion = discord.Embed(
            title="🚨 ¡SOS Enviado!",
            description=(
                f"**{ctx.author.mention}** necesita ayuda urgente:\n\n"
                f"💬 **Problema:** {problem}\n\n"
                f"📩 Se notificó a: {menciones if menciones else 'nadie (todos con DMs cerrados)'}\n\n"
                f"🎙️ ¡Salten a un canal de voz para ayudar!"
            ),
            color=discord.Color.red()
        )
        confirmacion.set_footer(text=f"Notificados por DM: {', '.join(notificados) if notificados else 'ninguno'}")
        await ctx.send(embed=confirmacion)

    @commands.command(name='help')
    async def custom_help(self, ctx: commands.Context):
        """
        Muestra la lista de comandos disponibles. Sobrescribe el help por defecto.
        """
        embed = discord.Embed(
            title="📖 Guía de Supervivencia — Dev-HQ Bot",
            description=(
                "Bienvenido al manual de comandos del equipo.\n"
                "Usa el prefijo `!` antes de cada comando.\n"
                "─────────────────────────────────"
            ),
            color=discord.Color.from_rgb(88, 101, 242)  # Color morado estilo Discord
        )

        # Thumbnail del bot
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)

        # Comando !daily
        embed.add_field(
            name="📅  `!daily [tarea]`",
            value=(
                "Registra tu standup diario.\n"
                "Informa al equipo en qué vas a trabajar hoy.\n"
                "**Ejemplo:** `!daily Terminar el módulo de login`"
            ),
            inline=False
        )

        # Separador visual
        embed.add_field(name="─────────────────────────────────", value="", inline=False)

        # Comando !focus
        embed.add_field(
            name="🎧  `!focus`",
            value=(
                "Activa o desactiva el modo concentración.\n"
                "Cuando estás en la zona, el equipo sabrá que no debes ser interrumpido.\n"
                "**Ejemplo:** `!focus`"
            ),
            inline=False
        )

        embed.add_field(name="─────────────────────────────────", value="", inline=False)

        # Comando !sos
        embed.add_field(
            name="🚨  `!sos [problema]`",
            value=(
                "Envía una alerta de emergencia al equipo disponible.\n"
                "Notifica por DM a todos los que **no** están en modo concentración.\n"
                "**Ejemplo:** `!sos No me corre el servidor, error 500`"
            ),
            inline=False
        )

        embed.add_field(name="─────────────────────────────────", value="", inline=False)

        # Comando !help
        embed.add_field(
            name="📖  `!help`",
            value=(
                "Muestra este manual de comandos.\n"
                "**Ejemplo:** `!help`"
            ),
            inline=False
        )

        embed.set_footer(
            text="Dev-HQ Bot • Tu equipo siempre sincronizado 🚀",
            icon_url=self.bot.user.display_avatar.url
        )

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    """
    Función requerida por discord.py para cargar este archivo como extensión.
    """
    await bot.add_cog(SupportCog(bot))

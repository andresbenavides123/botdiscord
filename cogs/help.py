import discord
from discord.ext import commands

class SupportCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", help="Muestra la lista de comandos disponibles.")
    async def custom_help(self, ctx):
        embed = discord.Embed(
            title="🛠️ Panel de Ayuda - SyncBot",
            description="Aquí tienes la lista de comandos disponibles para el equipo:",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="📝 !daily [mensaje]",
            value="Guarda tu reporte diario de progreso (Stand-up). Ejemplo: `!daily Hice el backend de login`",
            inline=False
        )
        embed.add_field(
            name="🎧 !focus [minutos]",
            value="Activa el modo trabajo profundo. Recibirás el rol 'En la Zona 🎧' y no te molestaremos. Ejemplo: `!focus 45`",
            inline=False
        )
        embed.add_field(
            name="🛟 !sos [problema]",
            value="¿Atascado? Pide ayuda de emergencia (Pair Programming) a los que no estén concentrados. Ejemplo: `!sos Error en el controlador`",
            inline=False
        )
        embed.add_field(
            name="❓ !help",
            value="Muestra este mensaje de ayuda.",
            inline=False
        )
        embed.set_footer(text="SyncBot - Herramienta para equipos remotos")
        await ctx.send(embed=embed)

    @commands.command(name="sos", help="Pide ayuda al equipo para pair programming.")
    async def sos(self, ctx, *, problema: str = None):
        if not problema:
            await ctx.send("⚠️ Debes describir tu problema. Ejemplo: `!sos Error en Spring Boot`")
            return

        # Nombre del rol de concentración
        focus_role_name = "En la Zona 🎧"
        
        # Buscar a los miembros que NO tengan el rol y que no sean bots
        available_members = []
        for member in ctx.guild.members:
            if member.bot:
                continue
            
            # Revisar si tiene el rol
            has_focus = any(role.name == focus_role_name for role in member.roles)
            
            # Excluimos a quien pide la ayuda para no pingearlo a sí mismo
            if not has_focus and member != ctx.author:
                available_members.append(member)

        if not available_members:
            await ctx.send(f"Lo siento {ctx.author.mention}, todos están '{focus_role_name}' o no hay nadie disponible ahora mismo. 😢")
            return

        # Construir el mensaje de ping
        pings = " ".join([m.mention for m in available_members])
        
        embed = discord.Embed(
            title="🚨 ¡Botón de Pánico Activado!",
            description=f"**{ctx.author.mention}** necesita ayuda urgente (Pair Programming).",
            color=discord.Color.red()
        )
        embed.add_field(name="Problema reportado:", value=f"```\n{problema}\n```", inline=False)
        embed.set_footer(text="¿Alguien puede saltar a un canal de voz?")

        await ctx.send(content=f"🔔 {pings}", embed=embed)

async def setup(bot):
    # Removemos el comando help por defecto si existe, para usar el nuestro
    bot.remove_command("help")
    await bot.add_cog(SupportCog(bot))

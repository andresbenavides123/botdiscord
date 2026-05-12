import discord
from discord.ext import commands
import asyncio

class FocusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Diccionario sugerido (opcional) para guardar quién está en focus y evitar que usen el comando dos veces a la vez.
        # self.active_sessions = {}

    # Comando !focus que recibe la cantidad de minutos
    @commands.command(name="focus", help="Inicia un temporizador Pomodoro para el trabajo profundo. Uso: !focus [minutos]")
    async def focus(self, ctx, minutos: int):
        # Validación básica: asegurarse de que el tiempo sea positivo
        if minutos <= 0:
            await ctx.send("Por favor, ingresa una cantidad de minutos válida (mayor a 0).")
            return

        role_name = "En la Zona "
        # Busca en los roles del servidor si ya existe el rol "En la Zona "
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        # Si no lo encuentra, el bot intenta crearlo automáticamente. 
        # (Esto ahorra trabajo manual al Integrante 1 / Arquitecto)
        if not role:
            try:
                role = await ctx.guild.create_role(name=role_name, reason="Rol automático para el temporizador de focus")
            except discord.Forbidden:
                # Si el bot no tiene permisos de Administrador/Gestionar Roles, avisa.
                await ctx.send("No tengo permisos para crear roles en este servidor. Por favor, crea el rol 'En la Zona' manualmente y dame permisos.")
                return

        # Asignar el rol al usuario que ejecutó el comando
        try:
            await ctx.author.add_roles(role)
            await ctx.send(f"¡{ctx.author.mention} ha entrado en 'La Zona' por {minutos} minutos! Por favor, no molestar.")
        except discord.Forbidden:
            # Si el rol del bot está por debajo del rol que intenta asignar, fallará.
            await ctx.send("No tengo permisos para asignar roles. Asegúrate de que mi rol esté por encima del rol 'En la Zona'.")
            return

        # --- EL CORAZÓN DE ESTE ROL (Integrante 3): asyncio.sleep() ---
        # Esto pausa SOLO esta función específica de forma asíncrona por X minutos.
        # Gracias a esto, el bot NO se congela y puede seguir respondiendo a otros usuarios.
        await asyncio.sleep(minutos * 60)

        # Una vez que pasa el tiempo, intentamos quitarle el rol al usuario
        try:
            await ctx.author.remove_roles(role)
        except discord.Forbidden:
            pass # Ignoramos el error si no se pudo quitar (ya se habría quejado antes)

        # Finalmente, enviamos un Mensaje Directo (DM) al usuario avisando que terminó.
        try:
            await ctx.author.send(f"¡Tu sesión de enfoque de {minutos} minutos ha finalizado! Excelente trabajo. ")
        except discord.Forbidden:
            # Es muy común que los usuarios tengan cerrados los DMs para bots en Discord. 
            # En ese caso, dejamos un mensaje en el mismo canal como respaldo.
            await ctx.send(f"{ctx.author.mention}, tu tiempo de enfoque ha terminado (no pude enviarte un mensaje privado). ")

# Función estándar para cargar este archivo como una extensión (Cog) en el bot
async def setup(bot):
    await bot.add_cog(FocusCog(bot))

import discord
from discord.ext import commands
import asyncio
from typing import Set


class FocusCog(commands.Cog):
    """Cog that implements a Pomodoro-style focus timer.

    Responsibilities:
    - Provide the `!focus [minutes]` command.
    - Assign the role "En la Zona 🎧" to the invoking user for the duration.
    - Use `asyncio.sleep()` so only this coroutine is paused (does not block the bot).
    - Remove the role and DM the user when the timer ends.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Track active focus sessions by user ID to prevent duplicates.
        self.active_sessions: Set[int] = set()

    @commands.command(name="focus", help="Start a Pomodoro-style focus timer. Usage: !focus [minutes]")
    async def focus(self, ctx: commands.Context, minutes: int):
        """Start a focus timer for `minutes` minutes.

        Steps:
        1. Validate input.
        2. Ensure the role `En la Zona 🎧` exists (create if possible).
        3. Assign the role to the invoking user.
        4. Await `asyncio.sleep(minutes * 60)` to pause this coroutine asynchronously.
        5. Remove the role and DM the user when finished.
        """

        # Basic validation: positive integer
        if minutes <= 0:
            await ctx.send("Please provide a positive number of minutes (greater than 0).")
            return

        # Ensure this command is used in a guild (server), not in a DM
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server (not in DMs).")
            return

        # Quick permission checks for the bot: manage_roles is required to assign/remove the role
        bot_member = ctx.guild.me
        if bot_member is None:
            bot_member = ctx.guild.get_member(self.bot.user.id)

        if bot_member and not bot_member.guild_permissions.manage_roles:
            await ctx.send("I need the 'Manage Roles' permission to assign the 'En la Zona 🎧' role. Please grant it and try again.")
            return

        user_id = ctx.author.id

        # Prevent the same user from starting multiple concurrent focus sessions
        if user_id in self.active_sessions:
            await ctx.send(f"{ctx.author.mention}, you already have an active focus session.")
            return

        role_name = "En la Zona 🎧"

        # Find role by exact name
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        # If the role does not exist, attempt to create it.
        if not role:
            try:
                role = await ctx.guild.create_role(name=role_name, reason="Automatic role for focus timer")
            except discord.Forbidden:
                await ctx.send("I don't have permission to create roles. Please create the role 'En la Zona 🎧' and ensure I can manage it.")
                return

        # Check role hierarchy: bot's top role must be higher than the role we want to assign
        if bot_member and role and bot_member.top_role <= role:
            await ctx.send("My role must be above 'En la Zona 🎧' in the role hierarchy to assign it. Please adjust my role position.")
            return

        # Try to assign the role to the user
        try:
            await ctx.author.add_roles(role)
        except discord.Forbidden:
            await ctx.send("I don't have permission to assign roles. Make sure my role is above 'En la Zona 🎧' in the role hierarchy.")
            return

        # Mark session active before sleeping to avoid races
        self.active_sessions.add(user_id)

        # Notify in the channel (brief confirmation)
        await ctx.send(f"{ctx.author.mention} has entered 'En la Zona 🎧' for {minutes} minutes. Stay focused!")

        try:
            # Pause this coroutine asynchronously for the requested duration
            await asyncio.sleep(minutes * 60)

            # Attempt to remove the role when the timer completes
            try:
                await ctx.author.remove_roles(role)
            except discord.Forbidden:
                # If removal fails because of permissions, ignore silently.
                pass

            # Try to DM the user to notify completion
            try:
                await ctx.author.send(f"Your {minutes}-minute focus session has ended. Great job!")
            except discord.Forbidden:
                # Common case: user has DMs closed for bots. Fallback to channel mention.
                await ctx.send(f"{ctx.author.mention}, your focus time has ended (could not send DM).")

        finally:
            # Ensure we always clear the active session flag, even on errors
            self.active_sessions.discard(user_id)


async def setup(bot: commands.Bot):
    await bot.add_cog(FocusCog(bot))

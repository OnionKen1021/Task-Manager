import discord
from discord.ext import commands
import pretty_errors
from Cogs.Commands.Group.ticket import Ticket

class Events_on_connect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_connect(self):
        await self.bot.sync_commands()
        print("成功同步指令!")

def setup(bot):
    bot.add_cog(Events_on_connect(bot))
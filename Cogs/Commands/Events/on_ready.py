import discord
from discord.ext import commands
import pretty_errors

class Events_on_ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("【INFO】- Task Manager Alpha 已經成功上線!")

def setup(bot):
    bot.add_cog(Events_on_ready(bot))
import discord
import os
import json
import pretty_errors
from Cogs.Function.Invoke import pip_install, cogs_loading

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.members = True

bot = discord.Bot(intents=intents)

path_list = [
    "Group",
    "Slash",
    "Message",
    "Events"
]

cogs_loading(bot, path_list)

bot.run("MTA1NDM2NDk2NzUyNjIyMzkyMg.GrLK3N.BL-LAwTSZA_oMRBzT6-NbwSxaf8UZ0JBK_EL6A")
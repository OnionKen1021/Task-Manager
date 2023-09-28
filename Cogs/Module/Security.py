import discord
import json
import pretty_errors
from Cogs.Module.Color import Color_Module

def Security_Module(guild_id):
    color_set = Color_Module(guild_id)
    try:
        with open('./JSDB/Module/color.json') as f:
            data = json.load(f)
        
        security_set = data[str(guild_id)]["enabled"]
        
        if security_set == "True":
            embed=discord.Embed(title="<:security:1115944085140803634> -  安全性攔截模式已啟用!",color=color_set)
            return embed

        return None
    except:
        return None
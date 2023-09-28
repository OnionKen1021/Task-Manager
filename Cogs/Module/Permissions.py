import json
import discord
import pretty_errors
from Cogs.Module.Color import Color_Module

def Error_User_Permissions(guild_id):
    color_set = Color_Module(guild_id)
    embed=discord.Embed(title="<:security:1115944085140803634> -  使用者權限不足! 指令申請已被拒絕!",color=color_set)
    return embed

def Error_Bot_Permissions(guild_id):
    color_set = Color_Module(guild_id)
    embed=discord.Embed(title="<:security:1115944085140803634> -  機器人權限不足! 指令申請已被拒絕!",color=color_set)
    return embed
import discord
from Cogs.Module.Color import Color_Module
from Cogs.Module.Security import Security_Module
from Cogs.Module.Permissions import Error_User_Permissions, Error_Bot_Permissions
from JSDB.Module.invoke import invoke_json_path

def emoji_process(emoji):
    match emoji:
        case "file":
            return "<:file:1115287404174135346>"
        case "dev":
            return "<:dev:1068777955343470692>"
            


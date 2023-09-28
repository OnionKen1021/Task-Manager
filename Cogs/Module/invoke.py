import discord
import pretty_errors
from Cogs.Module.Color import Color_Module
from Cogs.Module.Security import Security_Module
from Cogs.Module.Permissions import Error_User_Permissions, Error_Bot_Permissions
from JSDB.Module.invoke import invoke_json_path

def invoke_process(module,guild_id):
    args = eval(str(module) + f"({guild_id})")
    return args

def invoke_json_process(module, category, get):
    args = invoke_json_path(category,get)
    return args


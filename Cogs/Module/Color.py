import discord
import json
import pretty_errors

def Color_Module(guild_id):
    try:
        with open('./JSDB/Module/color.json') as f:
            data = json.load(f)
        
        color_set = data[str(guild_id)]["color"]
    except:
        color_set = 0x2e2e2e
        

    return color_set

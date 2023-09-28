import os
import pretty_errors

def pip_install():
    os.system("python3 -m pip install -U py-cord")

def cogs_loading(bot,path_list):
    for file_path in path_list:
        for filename in os.listdir(f"Cogs/Commands/{file_path}"):
            if filename.endswith('.py'):
                bot.load_extension(f"Cogs.Commands.{file_path}.{filename[:-3]}")
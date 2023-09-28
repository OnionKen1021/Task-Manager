import datetime
import discord
import json
import pretty_errors
from discord.commands import Option
from discord.ext import commands
from Cogs.Module.Emoji import emoji_process
from Cogs.Module.invoke import invoke_process, invoke_json_process

class Ticket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="開啟客服單",emoji="<a:check:1064490541116563476>", style=discord.ButtonStyle.success, custom_id="ticket - button")
    async def button_callback(self, button, interaction):
        color_set = invoke_process("Color_Module", interaction.guild.id)
        try:
            with open(invoke_json_process("invoke_json_path" ,"ticket", "ban"), 'r') as fp:
                data = json.load(fp)
            
            ban_enabled = data[str(interaction.guild.id)][str(interaction.user.id)]["enabled"]
            
            if ban_enabled == "True":
                embed=discord.Embed(title="<:security:1115944085140803634> - 您已被本伺服器封鎖使用權限!",color=color_set)
                return await interaction.response.send_message(embed=embed, ephemeral=True)
        except:
            pass
        
        with open(invoke_json_process("invoke_json_path" ,"ticket", "data"), 'r') as fp:
            data = json.load(fp)
            
        enabled = data[str(interaction.guild.id)]["enabled"]
        
        if enabled != "True":
            embed=discord.Embed(title="<:security:1115944085140803634> - 客服單系統已被本伺服器關閉!",color=color_set)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        category_id = data[str(interaction.guild.id)]["category"]
        log_channe_id = data[str(interaction.guild.id)]["log_channel"]
        try:
            category = discord.utils.get(interaction.guild.categories, id=int(category_id))
            channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}",category=category)
            await channel.edit(topic=f"ticket-{interaction.user.id}")
        
            overwrites = channel.overwrites_for(interaction.guild.default_role)
            overwrites.read_messages, overwrites.send_messages = False, False
            await channel.set_permissions(interaction.guild.default_role, overwrite=overwrites)
        
            overwrites = channel.overwrites_for(interaction.user)
            overwrites.send_messages, overwrites.read_messages = True, True
            await channel.set_permissions(interaction.user, overwrite=overwrites)
        except:
            embed=discord.Embed(title="<:security:1115944085140803634> - 機器人的權限不足! 請檢查身分組!",color=color_set)
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        embed=discord.Embed(title="<a:check:1064490541116563476> | 客服單已開啟於指定類別!",color=color_set)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        await channel.send(f"**{interaction.user.mention} | 客服單在這!**")

class CMDS_ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ticket = discord.SlashCommandGroup("ticket", "Task Manager | 管理相關指令")
    
    @commands.Cog.listener()
    async def on_connect(self):
        self.bot.add_view(Ticket())
    
    @ticket.command(name='setup',description='客服系統 | 設置客服單系統')
    async def setup(self, ctx, title: Option(str, '訊息標題', name='訊息標題'),reason: Option(str, '訊息內容', name='訊息內容'),category: Option(discord.CategoryChannel, '創建類別', name='創建類別')
                    ,log_channel: Option(discord.TextChannel, '紀錄頻道', name='紀錄頻道')):
        await ctx.defer()
        color_set = invoke_process("Color_Module", ctx.guild.id)
        security_set = invoke_process("Security_Module", ctx.guild.id)
        if security_set:
            await ctx.respond(embed=security_set)
            return
        
        if not ctx.author.guild_permissions.administrator:
            embed = invoke_process("Error_User_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)
        
        with open(invoke_json_process("invoke_json_path" ,"ticket", "data"), 'r') as fp:
            data = json.load(fp)

            data[str(ctx.guild.id)] = {
                "enabled": "True", "category": int(category.id), "log_channel": int(log_channel.id)}
        with open(invoke_json_process("invoke_json_path" ,"ticket", "data"), 'w') as fp:
            json.dump(data, fp, indent=4)

        embed=discord.Embed(title="",color=color_set)
        embed.set_author(name=f"{title}",icon_url=str(self.bot.user.display_avatar.url))
        embed.add_field(name="<:file:1115287404174135346> ` 詳細資料: `", value=f"**{reason}**", inline=True)
        await ctx.respond(embed=embed, view=Ticket())
        
    @ticket.command(name='ban',description='客服系統 | 客服單停權')
    async def ban(self, ctx, user: Option(discord.Member, '選取使用者', name='使用者')):
        await ctx.defer(ephemeral=True)
        color_set = invoke_process("Color_Module", ctx.guild.id)
        security_set = invoke_process("Security_Module", ctx.guild.id)
        if security_set:
            await ctx.respond(embed=security_set)
            return
        
        if not ctx.author.guild_permissions.administrator:
            embed = invoke_process("Error_User_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)
        
        try:
            with open(invoke_json_process("invoke_json_path" ,"ticket", "ban"), 'r') as fp:
                data = json.load(fp)
            
            verify = data[str(ctx.guild.id)]
        except:
            with open(invoke_json_process("invoke_json_path" ,"ticket", "ban"), 'r') as fp:
                data = json.load(fp)

                data[str(ctx.guild.id)] = {}
            with open(invoke_json_process("invoke_json_path" ,"ticket", "ban"), 'w') as fp:
                json.dump(data, fp, indent=4)
        
        with open(invoke_json_process("invoke_json_path" ,"ticket", "ban"), 'r') as fp:
            data = json.load(fp)

            data[str(ctx.guild.id)][str(user.id)] = {
                "enabled": "True"}
        with open(invoke_json_process("invoke_json_path" ,"ticket", "ban"), 'w') as fp:
            json.dump(data, fp, indent=4)

        embed=discord.Embed(title="",color=color_set)
        embed.set_author(name=f"Task Manager - 客服單停權使用者",icon_url=str(self.bot.user.display_avatar.url))
        embed.add_field(name=f"{emoji_process('file')} ` 詳細資料: `", value=f"**已停權 {user.mention} 於客服單系統!**", inline=True)
        await ctx.respond(embed=embed, ephemeral=True)
        
    @ticket.command(name='unban',description='客服系統 | 客服單解除停權')
    async def unban(self, ctx, user: Option(discord.Member, '選取使用者', name='使用者')):
        await ctx.defer(ephemeral=True)
        color_set = invoke_process("Color_Module", ctx.guild.id)
        security_set = invoke_process("Security_Module", ctx.guild.id)
        if security_set:
            await ctx.respond(embed=security_set)
            return
        
        if not ctx.author.guild_permissions.administrator:
            embed = invoke_process("Error_User_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)
        
        try:
            with open(invoke_json_process("invoke_json_path" ,"ticket", "ban"), 'r') as fp:
                data = json.load(fp)
            
            verify = data[str(ctx.guild.id)]
        except:
            with open(invoke_json_process("invoke_json_path" ,"ticket", "ban"), 'r') as fp:
                data = json.load(fp)

                data[str(ctx.guild.id)] = {}
            with open(invoke_json_process("invoke_json_path" ,"ticket", "ban"), 'w') as fp:
                json.dump(data, fp, indent=4)
        
        with open(invoke_json_process("invoke_json_path" ,"ticket", "ban"), 'r') as fp:
            data = json.load(fp)

            data[str(ctx.guild.id)][str(user.id)] = {
                "enabled": "False"}
        with open(invoke_json_process("invoke_json_path" ,"ticket", "ban"), 'w') as fp:
            json.dump(data, fp, indent=4)

        embed=discord.Embed(title="",color=color_set)
        embed.set_author(name=f"Task Manager - 客服單解除停權使用者",icon_url=str(self.bot.user.display_avatar.url))
        embed.add_field(name=f"{emoji_process('file')} ` 詳細資料: `", value=f"**已解除停權 {user.mention} 於客服單系統!**", inline=True)
        await ctx.respond(embed=embed, ephemeral=True)
        
    @ticket.command(name='info',description='客服系統 | 客服單資料查詢')
    async def information(self, ctx):
        await ctx.defer(ephemeral=True)
        color_set = invoke_process("Color_Module", ctx.guild.id)
        security_set = invoke_process("Security_Module", ctx.guild.id)
        if security_set:
            await ctx.respond(embed=security_set)
            return
        
        if not ctx.author.guild_permissions.administrator:
            embed = invoke_process("Error_User_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)
        
        try:
            with open(invoke_json_process("invoke_json_path" ,"ticket", "data"), 'r') as fp:
                data = json.load(fp)
            
            enabled = data[str(ctx.guild.id)]["enabled"].replace('True','` ✅ 已啟用 `').replace('False', '` ❌ 未啟用 `')
            category_id = data[str(ctx.guild.id)]["category"]
            log_channel_id = data[str(ctx.guild.id)]["log_channel"]
            
        except:
            embed=discord.Embed(title="<:security:1115944085140803634> - 本伺服器並未設置客服單系統!",color=color_set)
            return await ctx.respond(embed=embed, ephemeral=True)

        channel = await self.bot.fetch_channel(int(log_channel_id))
        
        embed=discord.Embed(title="",color=color_set)
        embed.set_author(name=f"Task Manager - 客服單解除停權使用者",icon_url=str(self.bot.user.display_avatar.url))
        embed.add_field(name=f"<:security:1115944085140803634> ` 啟用狀態: `", value=f"**{enabled}**", inline=True)
        embed.add_field(name=f"<:chat:1086991441907167283> ` 類別頻道: `", value=f"**{category_id}**", inline=True)
        embed.add_field(name=f"<:setting:1068454475871817799> ` 紀錄頻道: `", value=f"**{channel.mention}**", inline=True)
        await ctx.respond(embed=embed, ephemeral=True)
    
    @ticket.command(name='enabled',description='客服系統 | 啟用系統')
    async def enabled(self, ctx):
        await ctx.defer(ephemeral=True)
        color_set = invoke_process("Color_Module", ctx.guild.id)
        security_set = invoke_process("Security_Module", ctx.guild.id)
        if security_set:
            await ctx.respond(embed=security_set)
            return
        
        if not ctx.author.guild_permissions.administrator:
            embed = invoke_process("Error_User_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)
        
        try:
            with open(invoke_json_process("invoke_json_path" ,"ticket", "data"), 'r') as fp:
                data = json.load(fp)
            
            enabled = data[str(ctx.guild.id)]["enabled"].replace('True','` ✅ 已啟用 `').replace('False', '` ❌ 未啟用 `')
            category_id = data[str(ctx.guild.id)]["category"]
            log_channel_id = data[str(ctx.guild.id)]["log_channel"]
            
            with open(invoke_json_process("invoke_json_path" ,"ticket", "data"), 'r') as fp:
                data = json.load(fp)

                data[str(ctx.guild.id)] = {
                    "enabled": "True", "category": int(category_id), "log_channel": int(log_channel_id)}
            with open(invoke_json_process("invoke_json_path" ,"ticket", "data"), 'w') as fp:
                json.dump(data, fp, indent=4)
            
            embed=discord.Embed(title="<a:check:1064490541116563476> -  已成功 啟用 客服單系統!",color=color_set)
            return await ctx.respond(embed=embed, ephemeral=True)
        except:
            embed=discord.Embed(title="<:security:1115944085140803634> -  本伺服器並未設置客服單系統!",color=color_set)
            return await ctx.respond(embed=embed, ephemeral=True)
    
    @ticket.command(name='disabled',description='客服系統 | 關閉系統')
    async def disabled(self, ctx):
        await ctx.defer(ephemeral=True)
        color_set = invoke_process("Color_Module", ctx.guild.id)
        security_set = invoke_process("Security_Module", ctx.guild.id)
        if security_set:
            await ctx.respond(embed=security_set)
            return
        
        if not ctx.author.guild_permissions.administrator:
            embed = invoke_process("Error_User_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)
        
        try:
            with open(invoke_json_process("invoke_json_path" ,"ticket", "data"), 'r') as fp:
                data = json.load(fp)
            
            enabled = data[str(ctx.guild.id)]["enabled"].replace('True','` ✅ 已啟用 `').replace('False', '` ❌ 未啟用 `')
            category_id = data[str(ctx.guild.id)]["category"]
            log_channel_id = data[str(ctx.guild.id)]["log_channel"]
            
            with open(invoke_json_process("invoke_json_path" ,"ticket", "data"), 'r') as fp:
                data = json.load(fp)

                data[str(ctx.guild.id)] = {
                    "enabled": "False", "category": int(category_id), "log_channel": int(log_channel_id)}
            with open(invoke_json_process("invoke_json_path" ,"ticket", "data"), 'w') as fp:
                json.dump(data, fp, indent=4)
            
            embed=discord.Embed(title="<a:check:1064490541116563476> -  已成功 關閉 客服單系統!",color=color_set)
            return await ctx.respond(embed=embed, ephemeral=True)
        except:
            embed=discord.Embed(title="<:security:1115944085140803634> -  本伺服器並未設置客服單系統!",color=color_set)
            return await ctx.respond(embed=embed, ephemeral=True)
        
    @ticket.command(name='close',description='客服系統 | 關閉客服單')
    async def close(self, ctx):
        await ctx.defer(ephemeral=True)
        color_set = invoke_process("Color_Module", ctx.guild.id)
        security_set = invoke_process("Security_Module", ctx.guild.id)
        if security_set:
            await ctx.respond(embed=security_set)
            return
        
        if ctx.channel.topic:
            if ctx.channel.topic == f"ticket-{ctx.author.id}":
                await ctx.channel.delete()
                return
        else:
            embed=discord.Embed(title="<:security:1115944085140803634> - 本頻道並未客服單頻道!",color=color_set)
            return await ctx.respond(embed=embed, ephemeral=True)
        
        if not ctx.author.guild_permissions.administrator:
            embed = invoke_process("Error_User_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)
        
        if "ticket" in ctx.channel.topic:
            await ctx.channel.delete()
        else:
            embed=discord.Embed(title="<:security:1115944085140803634> - 本頻道並未客服單頻道!",color=color_set)
            return await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(CMDS_ticket(bot))
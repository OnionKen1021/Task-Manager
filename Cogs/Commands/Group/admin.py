import datetime
import discord
import pretty_errors
from discord.commands import Option
from discord.ext import commands
from Cogs.Module.Emoji import emoji_process
from Cogs.Module.invoke import invoke_process

class CMDS_admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    admin = discord.SlashCommandGroup("admin", "Task Manager | 管理相關指令")

    @admin.command(name='warn',description='管理系統 | 警告用戶')
    async def warn(self, ctx, user: Option(discord.Member, '選取要警告的使用者', name='使用者'),reason: Option(str, '警告原因', name='警告原因'),
                       channel: Option(discord.TextChannel, '傳送頻道', name='傳送頻道',default=None),msg: Option(str, '傳送訊息給用戶', choices=["True","False"], name='傳送訊息',default="False")):
        await ctx.defer(ephemeral=True)
        color_set = invoke_process("Color_Module", ctx.guild.id)
        security_set = invoke_process("Security_Module", ctx.guild.id)
        if security_set:
            await ctx.respond(embed=security_set)
            return
        
        if not ctx.author.guild_permissions.administrator:
            embed = invoke_process("Error_User_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)

        embed=discord.Embed(title="",color=color_set)
        embed.set_author(name=f"Task Manager 警告系統 - {user.name}",icon_url=str(self.bot.user.display_avatar.url))
        embed.add_field(name=f"{emoji_process('file')} ` 詳細資料: `", value=f"**{reason}**", inline=True)
        embed.add_field(name=f"{emoji_process('dev')} ` 處置人員: `", value=f"**{ctx.author.mention}**", inline=True)
        embed.set_thumbnail(url=str(user.display_avatar.url))

        if channel:
            await channel.send(embed=embed)

        await ctx.respond(embed=embed)

        if msg == "True":
            await user.send(embed=embed)
        
    @admin.command(name='ban',description='管理系統 | 停權用戶')
    async def ban(self, ctx, user: Option(discord.Member, '選取要停權的使用者', name='使用者'),reason: Option(str, '停權原因', name='停權原因'),
                       channel: Option(discord.TextChannel, '傳送頻道', name='傳送頻道',default=None),msg: Option(str, '傳送訊息給用戶', choices=["True","False"], name='傳送訊息',default="False")):
        await ctx.defer(ephemeral=True)
        color_set = invoke_process("Color_Module", ctx.guild.id)
        security_set = invoke_process("Security_Module", ctx.guild.id)
        if security_set:
            await ctx.respond(embed=security_set)
            return
        
        if not ctx.author.guild_permissions.administrator:
            embed = invoke_process("Error_User_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)

        embed=discord.Embed(title="",color=color_set)
        embed.set_author(name=f"Task Manager 停權系統 - {user.name}",icon_url=str(self.bot.user.display_avatar.url))
        embed.add_field(name=f"{emoji_process('file')} ` 詳細資料: `", value=f"**{reason}**", inline=True)
        embed.add_field(name=f"{emoji_process('dev')} ` 處置人員: `", value=f"**{ctx.author.mention}**", inline=True)
        embed.set_thumbnail(url=str(user.display_avatar.url))
        try:
            await user.ban(reason = reason)
        except:
            embed = invoke_process("Error_Bot_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)

        if channel:
            await channel.send(embed=embed)

        await ctx.respond(embed=embed)

        if msg == "True":
            await user.send(embed=embed)

    @admin.command(name='unban',description='管理系統 | 解除停權用戶')
    async def unban(self, ctx, user_id: Option(str, '選取要解除停權的使用者 ID', name='使用者-id'),reason: Option(str, '解除停權原因', name='解除停權原因'),
                       channel: Option(discord.TextChannel, '傳送頻道', name='傳送頻道',default=None),msg: Option(str, '傳送訊息給用戶', choices=["True","False"], name='傳送訊息',default="False")):
        await ctx.defer(ephemeral=True)
        color_set = invoke_process("Color_Module", ctx.guild.id)
        security_set = invoke_process("Security_Module", ctx.guild.id)
        if security_set:
            await ctx.respond(embed=security_set)
            return
        
        if not ctx.author.guild_permissions.administrator:
            embed = invoke_process("Error_User_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)

        user = await self.bot.fetch_user(int(user_id))

        embed=discord.Embed(title="",color=color_set)
        embed.set_author(name=f"Task Manager 解除停權系統 - {user.name}",icon_url=str(self.bot.user.display_avatar.url))
        embed.add_field(name=f"{emoji_process('file')} ` 詳細資料: `", value=f"**{reason}**", inline=True)
        embed.add_field(name=f"{emoji_process('dev')} ` 處置人員: `", value=f"**{ctx.author.mention}**", inline=True)
        embed.set_thumbnail(url=str(user.display_avatar.url))

        try:
            await ctx.guild.unban(user)
        except:
            embed = invoke_process("Error_Bot_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)

        if channel:
            await channel.send(embed=embed)

        await ctx.respond(embed=embed)

        if msg == "True":
            await user.send(embed=embed)
    
    @admin.command(name='timeout',description='管理系統 | 禁言用戶')
    async def timeout(self, ctx, user: Option(discord.Member, '選取要禁言的使用者', name='使用者'),reason: Option(str, '禁言原因', name='禁言原因'),
                       channel: Option(discord.TextChannel, '傳送頻道', name='傳送頻道',default=None),msg: Option(str, '傳送訊息給用戶', choices=["True","False"], name='傳送訊息',default="False")
                       ,days: Option(int, '天數', name='天數',default=0),hours: Option(int, '時數', name='時數',default=0),minutes: Option(int, '分鐘', name='分鐘',default=0),seconds: Option(int, '秒鐘', name='秒鐘',default=30)):
        await ctx.defer(ephemeral=True)
        color_set = invoke_process("Color_Module", ctx.guild.id)
        security_set = invoke_process("Security_Module", ctx.guild.id)
        if security_set:
            await ctx.respond(embed=security_set)
            return
        
        if not ctx.author.guild_permissions.administrator:
            embed = invoke_process("Error_User_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)

        time = days*86400 + hours*3600 + minutes*60 + seconds

        embed=discord.Embed(title="",color=color_set)
        embed.set_author(name=f"Task Manager 禁言系統 - {user.name}",icon_url=str(self.bot.user.display_avatar.url))
        embed.add_field(name=f"{emoji_process('file')} ` 詳細資料: `", value=f"**{reason}**", inline=True)
        embed.add_field(name=f"{emoji_process('dev')} ` 處置人員: `", value=f"**{ctx.author.mention}**", inline=True)
        embed.set_thumbnail(url=str(user.display_avatar.url))

        try:
            await user.timeout(until = discord.utils.utcnow() + datetime.timedelta(seconds=time), reason=reason)
        except:
            embed = invoke_process("Error_Bot_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)

        if channel:
            await channel.send(embed=embed)

        await ctx.respond(embed=embed)

        if msg == "True":
            await user.send(embed=embed)

    @admin.command(name='untimeout',description='管理系統 | 解除禁言用戶')
    async def untimeout(self, ctx, user: Option(discord.Member, '選取要解除禁言的使用者', name='使用者'),reason: Option(str, '解除禁言原因', name='解除禁言原因'),
                       channel: Option(discord.TextChannel, '傳送頻道', name='傳送頻道',default=None),msg: Option(str, '傳送訊息給用戶', choices=["True","False"], name='傳送訊息',default="False")):
        await ctx.defer(ephemeral=True)
        color_set = invoke_process("Color_Module", ctx.guild.id)
        security_set = invoke_process("Security_Module", ctx.guild.id)
        if security_set:
            await ctx.respond(embed=security_set)
            return
        
        if not ctx.author.guild_permissions.administrator:
            embed = invoke_process("Error_User_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)

        embed=discord.Embed(title="",color=color_set)
        embed.set_author(name=f"Task Manager 解除禁言系統 - {user.name}",icon_url=str(self.bot.user.display_avatar.url))
        embed.add_field(name=f"{emoji_process('file')} ` 詳細資料: `", value=f"**{reason}**", inline=True)
        embed.add_field(name=f"{emoji_process('dev')} ` 處置人員: `", value=f"**{ctx.author.mention}**", inline=True)
        embed.set_thumbnail(url=str(user.display_avatar.url))

        try:
            await user.remove_timeout(reason=reason)

        except:
            embed = invoke_process("Error_Bot_Permissions", ctx.guild.id)
            return await ctx.respond(embed=embed)

        if channel:
            await channel.send(embed=embed)

        await ctx.respond(embed=embed)

        if msg == "True":
            await user.send(embed=embed)

def setup(bot):
    bot.add_cog(CMDS_admin(bot))
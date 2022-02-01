import discord
from discord.ext import commands

# Global_Variables
prefix = "!"
token = ""

bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('目前登入身份：', bot.user)
    print('登入身份 ID：', bot.user.id)
    onActivity = discord.Game("獲取不同的 Minecraft 伺服器資訊")

    await bot.change_presence(status=discord.Status.dnd, activity=onActivity)

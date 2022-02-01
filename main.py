import discord
import re
from discord.ext import commands
from mcstatus import MinecraftServer
from mcstatus import MinecraftBedrockServer

# Global_Variables
prefix = "!"
token = "OTM4MDkwOTcwMDE5NDIyMjQ4.YflPTA.jNXTgZIm442vUsWPSQ-UnSC8KIg"

bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')


@bot.event
async def on_ready():
    print('目前登入身份：', bot.user)
    print('登入身份 ID：', bot.user.id)
    onActivity = discord.Game("獲取不同的 Minecraft 伺服器資訊")

    await bot.change_presence(status=discord.Status.dnd, activity=onActivity)


@bot.command(name="status")
async def getServerStatus(ctx, args=""):
    embed = ""
    if args != "":
        await ctx.send("正在讀取伺服器 " + args + " 的資料，請稍候 ...")
        try:
            server = MinecraftServer.lookup(args)
            ping, info = server.ping(), server.status()

            embed = discord.Embed(title="Minecraft 伺服器狀態", description="伺服器地址：" + args)
            embed.set_author(name=args + " 的查詢")
            #embed.set_thumbnail(url=info.favicon)
            embed.add_field(name="MOTD", value=re.sub('§[a-z][0-9]*', '', info.description), inline=False)
            embed.add_field(name="網絡延遲", value=ping.real + " ms", inline=True)
            embed.add_field(name="伺服器版本", value=info.version.name, inline=True)
            embed.add_field(name="玩家數目", value=info.players.online + " / " + info.players.max, inline=False)
            embed.set_footer(text="MC 伺服器狀態查詢 | HyperNiteMC (Member of HN)")
        except:
            message = "請檢查並確認您所輸入的 IP 或 域名為。 伺服器可能正處於下線的狀態，請稍後再次嘗試！"
    else:
        message = "請輸入你希望查詢的伺服器 IP 或 域名。例子：125.12.33.98:25565 / mc.hypixel.net"

    await ctx.send(embed=embed)

bot.run(token)

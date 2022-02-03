import io
import random

import discord
import base64
import re
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
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
    # Local_Variables
    embed = ""
    picException = False

    if args != "":
        await ctx.channel.send("正在讀取伺服器 " + args + " 的資料，請稍候 ...")
        try:
            server = MinecraftServer.lookup(args)
            info = server.status()

            embed = discord.Embed(title="Minecraft 伺服器狀態", description="伺服器地址：" + args)

            try:
                image_64 = base64.b64decode(info.favicon.replace("data:image/png;base64,", ""))
                image_result = open('server_icon.png', 'wb')
                image_result.write(image_64)
                file = discord.File("server_icon.png")

                embed.set_thumbnail(url="attachment://server_icon.png")
                image_result.close()
            except:
                picException = True
                embed.set_thumbnail(url="https://i-cdn.hypernology.com/publicImages/bots/default_server_favicon.png")

            embed.set_author(name=args + " 的查詢")
            embed.add_field(name="MOTD", value=re.sub('§.', '', info.description), inline=False)
            embed.add_field(name="伺服器版本", value=info.version.name, inline=True)
            embed.add_field(name="玩家數目", value=str(info.players.online) + " / " + str(info.players.max), inline=True)
            embed.add_field(name="回應延遲", value=str(format(info.latency, ".2f")) + " ms", inline=True)
            embed.add_field(name="運行協定", value="版本 " + str(info.version.protocol), inline=True)
            embed.set_footer(text="MC 伺服器狀態查詢 | " + prefix + "status <伺服器網絡地址> | HyperNiteMC (Member of HN)")

        except Exception as e:
            embed = discord.Embed(title="Minecraft 伺服器狀態", description="伺服器離線 或 地址輸入錯誤")
            embed.set_thumbnail(url="https://i-cdn.hypernology.com/publicImages/bots/um.png")
            embed.add_field(name="錯誤原因 (1)", value="你所輸入的伺服器 IP 或 域名錯誤", inline=False)
            embed.add_field(name="錯誤原因 (2)", value="伺服器正處於離線狀態", inline=False)
            embed.add_field(name="正確域名例子", value="mc.example.com", inline=True)
            embed.add_field(name="正確 IP 例子", value="93.184.216.34:25565", inline=True)
            embed.set_footer(text="MC 伺服器狀態查詢 | " + prefix + "status <伺服器網絡地址> | HyperNiteMC (Member of HN)")

    else:
        embed = discord.Embed(title="Minecraft 伺服器狀態", description="請輸入伺服器 IP 地址")
        embed.set_thumbnail(url="https://i-cdn.hypernology.com/publicImages/bots/um.png")
        embed.add_field(name="錯誤原因", value="請輸入你希望查詢的伺服器 IP 或 域名", inline=False)
        embed.add_field(name="域名例子", value="mc.hypixel.net", inline=True)
        embed.add_field(name="IP 例子", value="125.12.33.98:25565", inline=True)
        embed.set_footer(text="MC 伺服器狀態查詢 | " + prefix + "status <伺服器網絡地址> | HyperNiteMC (Member of HN)")

    try:
        if picException:
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed, file=file)
    except:
        await ctx.channel.send("```錯誤：系統出現未知錯誤，請到 https://dc.hypernite.com #建議及提問區 通報專案維護者。```")


@bot.command(name="pe")
async def getPEServerStatus(ctx, args=""):
    # Local_Variables
    embed = ""

    if args != "":
        await ctx.channel.send("正在讀取 PE 伺服器 " + args + " 的資料，請稍候 ...")
        try:
            server = MinecraftBedrockServer.lookup(args)
            info = server.status()

            embed = discord.Embed(title="Minecraft PE 伺服器狀態", description="伺服器地址：" + args)

            embed.set_author(name=args + " 的查詢")
            embed.add_field(name="MOTD", value=re.sub('§.', '', info.motd), inline=False)
            embed.add_field(name="伺服器版本", value=info.version.version, inline=True)
            embed.add_field(name="伺服器運行軟體", value=info.map, inline=True)
            embed.add_field(name="默認遊戲模式", value=info.gamemode, inline=True)
            embed.add_field(name="回應延遲", value=str(format(info.latency, ".2f")) + " ms", inline=True)
            embed.add_field(name="運行協定", value="版本 " + str(info.version.protocol), inline=True)
            embed.add_field(name="玩家數目", value=str(info.players_online) + " / " + str(info.players_max), inline=True)
            embed.set_footer(text="MC 伺服器狀態查詢 | " + prefix + "status <伺服器網絡地址> | HyperNiteMC (Member of HN)")

        except Exception as e:
            embed = discord.Embed(title="Minecraft PE 伺服器狀態", description="伺服器離線 或 地址輸入錯誤 或 伺服器並未使用 PE 軟體")
            embed.set_thumbnail(url="https://i-cdn.hypernology.com/publicImages/bots/um.png")
            embed.add_field(name="錯誤原因 (1)", value="你所輸入的伺服器 IP 或 域名錯誤", inline=False)
            embed.add_field(name="錯誤原因 (2)", value="伺服器正處於離線狀態", inline=False)
            embed.add_field(name="錯誤原因 (3)", value="伺服器並未使用 PE 軟體，如：Nukkit, PocketMine-MP", inline=False)
            embed.add_field(name="正確域名例子", value="pe.example.com", inline=True)
            embed.add_field(name="正確 IP 例子", value="93.184.216.34:19134", inline=True)
            embed.set_footer(text="MC 伺服器狀態查詢 | " + prefix + "status <伺服器網絡地址> | HyperNiteMC (Member of HN)")

            print(e)

    else:
        embed = discord.Embed(title="Minecraft PE 伺服器狀態", description="請輸入伺服器 IP 地址")
        embed.set_thumbnail(url="https://i-cdn.hypernology.com/publicImages/bots/um.png")
        embed.add_field(name="錯誤原因", value="請輸入你希望查詢的伺服器 IP 或 域名", inline=False)
        embed.add_field(name="域名例子", value="pe.hypixel.net", inline=True)
        embed.add_field(name="IP 例子", value="125.12.33.98:19134", inline=True)
        embed.set_footer(text="MC 伺服器狀態查詢 | " + prefix + "pe <伺服器網絡地址> | HyperNiteMC (Member of HN)")

    try:
        await ctx.send(embed=embed)
    except:
        await ctx.channel.send("```錯誤：系統出現未知錯誤，請到 https://dc.hypernite.com #建議及提問區 通報專案維護者。```")


bot.run(token)

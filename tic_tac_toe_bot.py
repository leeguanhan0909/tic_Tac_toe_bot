import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

keep_alive()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot 已上線：{bot.user}")


maze = []
turn = 0
cnt = 0
player1 = ""
player2 = ""
size = -1
flag = False


def check(a):
    cflag = False
    mark = ["Ｏ", "Ｘ"][a]
    for r in range(size):
        cflag = True
        for c in range(size):
            if maze[r][c] != mark:
                cflag = False
                break
        if cflag: return True
    for c in range(size):
        cflag = True
        for r in range(size):
            if maze[r][c] != mark:
                cflag = False
                break
        if cflag: return True
    cflag = True
    for r in range(size):
        if maze[r][r] != mark:
            cflag = False
            break
    if cflag: return True
    cflag = True
    for r in range(size):
        if maze[r][size - r - 1] != mark:
            cflag = False
            break
    if cflag: return True

    return False


@bot.event
async def on_message(message):
    global player1, player2, size, maze, cnt, turn, flag
    if message.author == bot.user:
        return
    if message.channel.name != "tic_tac_toe":
        return
    if message.content.lower() == "ping":
        await message.channel.send("🏓 Pong!")
        return
    if message.content.lower() == "reset":
        player1 = ""
        player2 = ""
        size = -1
        flag = False
        maze = []
        turn = 0
        cnt = 0
        await message.channel.send("已重置")
        return
    if not flag:
        if message.content.lower()[0:8:1] == "set_size":
            data = message.content.split()
            if (len(data) != 2 or not data[1].isdigit()):
                await message.channel.send("你在搞什麼!?")
                return
            if (size != -1):
                await message.channel.send("已經設定過棋盤大小：" + str(size) +
                                           "。\n輸入reset重置。")
                return
            size = int(data[1])
            if (size < 3 or size > 7):
                await message.channel.send("你在搞什麼!?")
                return
            maze = [["⬜"] * size for _ in range(size)]
            await message.channel.send("目前棋盤大小：" + str(size))
            return
        if size != -1 and message.content.lower()[0:6] == "player":
            if player1 == "":
                player1 = message.author
                await message.channel.send("已添加@" + str(player1) + "為玩家1")
                return
            elif player2 == "":
                if player1 == message.author:
                    await message.channel.send(str(player1) + "，你已經是玩家1了")
                    return
                player2 = message.author
                flag = True
                turn = 0
                await message.channel.send("已添加@" + str(player2) + "為玩家2")
                return
            else:
                await message.channel.send("別人在玩，你在搞什麼!?")
            return
    elif size != -1:
        if not (len(message.content.strip())) == 2:
            await message.channel.send("你會不會玩啊!?")
            return
        if message.author != [player1, player2][turn]:
            if message.author != [player2, player1][turn]:
                await message.channel.send("別人在玩，不要搞!!!")
            else:
                await message.channel.send("還沒到你，急什麼")
            return
        a = message.content[0]
        b = message.content[1]
        if a not in [chr(ord('A') + i) for i in range(size)
                     ] or int(b) not in list(range(1, size + 1)):
            await message.channel.send("你會不會玩啊!?")
            return
        r = ord(a) - ord("A")
        c = int(b) - 1
        if (maze[r][c] != "⬜"):
            await message.channel.send("已經下過了")
            return
        maze[r][c] = ["Ｏ", "Ｘ"][turn]
        cnt += 1
        mystr = "現在棋盤\n    " + "  ".join(
            list(map(str, list(range(1, size + 1))))) + "\n"
        for r in range(size):
            mystr += str(chr(ord('A') + r)) + '  ' + "  ".join(maze[r]) + "\n"
        await message.channel.send(mystr)
        if check(turn):
            await message.channel.send(str([player1, player2][turn]) + "贏了!!!")
            player1 = ""
            player2 = ""
            size = -1
            flag = False
            cnt = 0
            return
        if cnt == size**2:
            await message.channel.send("平手")
            player1 = ""
            player2 = ""
            size = -1
            flag = False
            cnt = 0
            return
        turn = 1 - turn

    await bot.process_commands(message)


@bot.command()
async def rule(ctx):
    mystr2 = "規則：\n先輸入棋盤大小(3~7)，接著輸入player當玩家(先輸入先手)，接著輸入座標(例如A1)下棋"
    await ctx.send(mystr2)


TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)


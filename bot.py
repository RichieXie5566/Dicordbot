import discord
from discord.ext import commands
from discord.ext.commands import bot
import json
import random,os,asyncio
intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)


with open('items.json','r',encoding = 'utf8')as jfile:
   jdata = json.load(jfile)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    print("Meep Morp Zeep...", bot.user,"前來報到")
    game = discord.Game('Grand Theft Auto VI')
    await bot.change_presence(status=discord.Status.online, activity=game)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Grand Theft Auto VI"))

@bot.event
async def on_message(message):
    print(f"📩 收到訊息: {message.content} (來自: {message.author})")  # 測試用

    await bot.process_commands(message)  # 讓指令可以繼續運作

@bot.event
async def on_member_join(member):
   channel = bot.get_channel(int(jdata['normal_channel']))
   await channel.send(f'<@{member.id}> Welcome aborad bitch!')
   
@bot.event
async def on_member_remove(member):
   channel = bot.get_channel(int(jdata['normal_channel']))
   await channel.send(f'<@{member.id}> Yo bitch I aint got all day just screw youself!')


@bot.command(name="ping", help="This is a ping command")
async def ping(ctx):
   await ctx.send(f"Latency: {round(bot.latency * 1000)}ms")

@bot.event
async def on_message(message):
    if message.author == bot.user:  # 避免機器人回應自己
        return

    if message.content.strip().lower() == "yo":
        await message.channel.send(f"Yo!Yo!Yo! 148-3 to the 3 to the 6 to the 9, representing the ABQ, <@{message.author.id}> What up BIATCH!")

    if "三小" in message.content.strip().lower():
        await message.channel.send(f"<@{message.author.id}> 你才三小")

    if "幹" in message.content.strip().lower():
        await message.channel.send(f"<@{message.author.id}> 幹...幹什麼啦")

    if "好" in message.content.strip().lower():
        await message.channel.send(f"<@{message.author.id}> 好什麼?")

    if "抽" in message.content.strip().lower():
        if "抽" in jdata:  # 確保 JSON 裡有 "抽" 這個 key
            gallery_path = jdata["抽"]  # 正確取得 gallery 資料夾路徑

            # 確保資料夾存在
            if not os.path.exists(gallery_path):
                await message.channel.send("圖片資料夾不存在，請檢查設定！")
                return

            # 取得所有圖片檔案
            images = [f for f in os.listdir(gallery_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]

            if images:
                random_image = random.choice(images)  # 隨機選擇一張圖片
                image_path = os.path.join(gallery_path, random_image)  # 獲取完整路徑
                dcFile = discord.File(image_path)  # 建立 Discord 檔案物件
                await message.channel.send(file=dcFile)
            else:
                await message.channel.send("找不到圖片！請確保 gallery 資料夾內有圖片。")
        else:
            await message.channel.send("JSON 設定檔內缺少 '抽' 這個 key，請檢查 item.json！")

    await bot.process_commands(message)  # 讓其他指令繼續運作


bot.run(jdata['token'])
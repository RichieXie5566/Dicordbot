import discord
from discord.ext import commands
from discord.ext.commands import bot
import json
import random,os,asyncio
import yt_dlp as youtube_dl
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
    #game = discord.Game('Grand Theft Auto VI')
    #await bot.change_presence(status=discord.Status.online, activity=game)
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Grand Theft Auto VI"))
    
    # 設置初始狀態
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.playing, name="Grand Theft Auto VI")
    )

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

# 加入語音頻道
@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send(f"<@{ctx.author.id}> Get in the god damn channel.")
        return
    channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.send(f"Ah...a wire. I'm in {channel}")

# 離開語音頻道
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Fuck yall I'm out.")
    else:
        await ctx.send("This is my own domicile and I will not be harassed, BITCH!")

# 播放YT連結
@bot.command()
async def play(ctx, url):
    if not ctx.voice_client:
        await ctx.invoke(bot.get_command("join"))
    
    if not ctx.voice_client:
        await ctx.send("Failed to connect to voice channel.")
        return

    ydl_opts = {
        'format': 'bestaudio[abr<=192]',# 限制比特率到 192kbps
        'quiet': True,
        'noplaylist': True,
        'default_search': 'auto',
        'force-ipv4': True,
        'cachedir': False,
        'socket_timeout': 10,  # 超時 10 秒，穩定下載
        'buffer_size': 32768,  # 增加緩衝到 32KB
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']
            video_title = info['title']
    except Exception as e:
        await ctx.send(f"Cannot extract URL: {str(e)}")
        return

    ffmpeg_options = {'before_options': (
            '-reconnect 1 '  # 自動重連
            '-reconnect_streamed 1 '
            '-reconnect_delay_max 10 '  # 10 秒重連
            '-probesize 512k '  # 增加探測大小，平滑流開始
            '-timeout 15000000 '  # 設置 15 秒超時（單位：微秒）
            '-analyzeduration 5000000 '  # 增加分析時間，平滑開始
        ),
        'options': (
            '-vn '  # 禁用視頻
            '-ac 2 '  # 立體聲
        )
    }

    # 定義播放結束後的回調函數
    async def after_playing(error):
        if error:
            print(f"Error：{error}")
        else:
            print(f"Finished：{video_title}")
        # 播放結束後恢復初始狀態
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.playing, name="Grand Theft Auto VI")
        )

    try:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Yo! I am stopping the old shit!")

        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(
                url2,
                executable="I:/coding/dcb/ffmpeg/bin/ffmpeg.exe",
                **ffmpeg_options
            ),
            volume=1.0
        )

        # 開始播放前更新狀態
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.watching, name=f"Youtube：{video_title}")
        )

        # 播放音樂，並綁定回調
        ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(after_playing(e), bot.loop))
        await ctx.send(f"Yeah bitch it's rolling: {video_title}")

    except Exception as e:
        await ctx.send(f"Shit happens!: {str(e)}")
        # 出錯時恢復初始狀態
        await bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.playing, name="Grand Theft Auto VI")
        )


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
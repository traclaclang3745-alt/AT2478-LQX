

from discord.ext import commands, tasks
import discord
import nest_asyncio
from dataclasses import dataclass
import datetime
import re
import math
from zoneinfo import ZoneInfo
import os

bot_token = os.getenv("DISCORD_TOKEN")
chat_ids = os.getenv("CHAT_IDS").split(",")  # list string
chat_ids = [int(x.strip()) for x in chat_ids]  # list int

sessions = {}

@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0
    end_time: int = 0

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='-', intents=discord.Intents.all())

# KHỞI ĐỘNG

@bot.event
async def on_ready():
    print("Xin chào, Phi hành gia! Tôi là hệ thống trí truệ nhân tạo 'Sunday' của trạm không gian vũ trụ AT2478-LQX, rất vui được gặp bạn.")
    if chat_ids:
        for chat_id in chat_ids:
            channel = bot.get_channel(chat_id)
            if channel:
                await channel.send("Xin chào, Phi hành gia! Tôi là hệ thống trí truệ nhân tạo 'Sunday' của trạm không gian vũ trụ AT2478-LQX, rất vui được gặp bạn.")

# XIN CHÀO VÀ TẠM BIỆT

@bot.command()
async def hello(ctx):
    await ctx.send("Xin chào, Phi hành gia! 'Sunday' có thể giúp gì được cho bạn?")

# LÀM TOÁN

# Cộng
@bot.command()
async def add(ctx, *arr):
    if len(arr) < 2:
        await ctx.send("Vui lòng nhập ít nhất 2 số!")
        return

    result = 0
    for i in arr:
        result += int(i)

    await ctx.send(f"Kết quả: {result}")

# Trừ
@bot.command()
async def sub(ctx, *arr):
    if len(arr) < 2:
        await ctx.send("Vui lòng nhập ít nhất 2 số!")
        return

    result = int(arr[0])
    for i in arr[1:]:
        result -= int(i)

    await ctx.send(f"Kết quả: {result}")

# Nhân
@bot.command()
async def mul(ctx, *arr):
    if len(arr) < 2:
        await ctx.send("Vui lòng nhập ít nhất 2 số!")
        return

    result = 1
    for i in arr:
        result *= int(i)

    await ctx.send(f"Kết quả: {result}")

# Chia
@bot.command()
async def div(ctx, *arr):
    if len(arr) < 2:
        await ctx.send("Vui lòng nhập ít nhất 2 số!")
        return

    result = float(arr[0])
    try:
        for i in arr[1:]:
            result /= float(i)
    except ZeroDivisionError:
        await ctx.send("Không thể chia cho 0!")
        return

    if result.is_integer():
        result = int(result)

    await ctx.send(f"Kết quả: {result}")

# Cộng, trừ, nhân, chia
@bot.command()
async def calc(ctx, *, expression: str):
    try:
        # Cho phép các loại ngoặc: (), [], {}
        expression = expression.replace("[", "(").replace("]", ")")
        expression = expression.replace("{", "(").replace("}", ")")

        # Chỉ cho phép số, toán tử và ngoặc
        if not re.match(r'^[0-9+\-*/().\s]+$', expression): # Escaped hyphen
            await ctx.send("Biểu thức không hợp lệ, vui lòng thử lại!")
            return

        # Tính toán an toàn
        result = eval(expression, {"__builtins__": None}, {})

        await ctx.send(f"Kết quả: {result}")

    except ZeroDivisionError:
        await ctx.send("Không thể chia cho 0!")
    except Exception:
        await ctx.send("Biểu thức không hợp lệ, vui lòng thử lại!")

# SESSION

@bot.command()
async def start(ctx):
  user_tz = ZoneInfo("Asia/Ho_Chi_Minh")
  local_time = ctx.message.created_at.astimezone(user_tz)
  user_id = ctx.author.id
  if user_id in sessions:
    await ctx.send("Phiên làm việc của bạn đang hoạt động!")
    return

  new_session = Session()
  new_session.is_active = True
  new_session.start_time = local_time.timestamp()
  human_readable_time = local_time.strftime("%H:%M:%S")

  sessions[user_id] = new_session

  await ctx.send(f"Bắt đầu Phiên làm việc mới lúc **{human_readable_time}**!")

@bot.command()
async def end(ctx):
  user_tz = ZoneInfo("Asia/Ho_Chi_Minh")
  local_time = ctx.message.created_at.astimezone(user_tz)
  user_id = ctx.author.id
  if user_id not in sessions:
    await ctx.send("Bạn đang không kích hoạt phiên làm việc!")
    return

  current_session = sessions[user_id]
  current_session.end_time = local_time.timestamp()
  current_session.is_active = False
  duration = int(current_session.end_time - current_session.start_time)
  human_readable_time = local_time.strftime("%H:%M:%S")
  human_readable_duration = str(datetime.timedelta(seconds=duration))

  del sessions[user_id]
  
  await ctx.send(f"Phiên làm việc của bạn kết thúc lúc **{human_readable_time}** và kéo dài **{human_readable_duration}**!")


nest_asyncio.apply()
bot.run(bot_token)

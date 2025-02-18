# core/any.py
import discord
from discord.ext import commands

# 這邊可以使用Cog功能繼承基本屬性
class Cog_Extension(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# cogs/hello.py

from discord.ext import commands
import discord
from discord.ext.commands import bot
from core.any import Cog_Extension

class Hello(Cog_Extension):
    
    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"!Hi <@{ctx.author.id}>")

def setup(bot):
    bot.add_cog(Hello(bot))
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='*')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name="lol", help="Nur son Test-Command")
async def lol(ctx, arg):
    await ctx.send(arg)

bot.run(TOKEN)
import os

# Import command classes
from commands import wheelCommand

import discord
from discord.ext import commands
from dotenv import load_dotenv



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name="wheel", help="Drehe das Glücksrad!")
async def wheel(ctx, *args):
    await wheelCommand.onCommand(ctx, args)

bot.run(TOKEN)
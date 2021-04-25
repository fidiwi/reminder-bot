import os

# Import command classes
from commands import wheelCommand

import discord
from discord.ext import commands
from dotenv import load_dotenv

sessions = {}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name="wheel", help="Drehe das Glücksrad!")
async def wheel(ctx, *args):
    global sessions
    wheelObject = wheelCommand.Wheel(args, ctx)
    sessions[ctx.channel] = wheelObject
    await wheelObject.start()


@bot.command(name="spin", help="Drehe am Glücksrad!")
async def spin(ctx, *args):
    global sessions
    if sessions[ctx.channel]:
        finished = await sessions[ctx.channel].pick()
        if finished:
            del sessions[ctx.channel]            

bot.run(TOKEN)
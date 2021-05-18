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

@bot.command(name="wheel", help="Erstelle ein Glücksrad!")
async def wheel(ctx, *args):
    global sessions
    wheelObject = wheelCommand.Wheel(args, ctx)
    if await wheelObject.start():
        sessions[ctx.author.voice.channel] = wheelObject


@bot.command(name="spin", help="Drehe am Glücksrad!")
async def spin(ctx, *args):
    global sessions
    if ctx.author.voice.channel in sessions.keys():
        finished = await sessions[ctx.author.voice.channel].pick(ctx)
        if finished:
            del sessions[ctx.author.voice.channel]
    else:
        await ctx.send(":x: Aktuell läuft keine Glücksradsession")


@bot.command(name="group", help="Bildet x viele Gruppen mit Angehörigen des Voicechannels")
async def group(ctx, *args):
    if len(args) >= 1: 
        wheelObject = wheelCommand.Wheel([], ctx)
        if await wheelObject.start():
            await wheelObject.group(int(*args[0]))
    else:
        await ctx.send(":x: **Bitte gib an, wie viele Gruppen du haben möchtest**")


@bot.command(name="cancel", aliases=["c", "stop"], help="Bricht Glücksradsession ab")        
async def cancel(ctx, *args):
    global sessions
    if ctx.author.voice.channel in sessions.keys():
        del sessions[ctx.author.voice.channel]
        await ctx.send(":white_check_mark: Session erfolgreich abgebrochen")
    else:
        await ctx.send(":x: Aktuell läuft keine Glücksradsession")


bot.run(TOKEN)

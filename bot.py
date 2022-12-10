import os

# Import command classes
from commands import wheelCommand
from commands import citeCommand

import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.ext.tasks import loop
import requests

sessions = {}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    listenMinecraft.start()

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

@bot.command(name="fetchcites", help="Überträgt alle Zitate in GoogleSlides-Sheet")
async def fetchcites(ctx, *args):
    citeCommand.fetchAllData(ctx)

@loop(seconds=60)
async def listenMinecraft():
    data = requests.get("https://api.mcsrvstat.us/2/blattgruen.eu")
    data_json = data.json()
    if data_json["debug"]["ping"]:
        await bot.change_presence(activity=discord.Game(name=f'{data_json["players"]["online"]}/{data_json["players"]["max"]}'))
    else:
        await bot.change_presence(activity=discord.Game(name="MC offline"))


bot.run(TOKEN)

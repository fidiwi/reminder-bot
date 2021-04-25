import asyncio
import discord

async def onCommand(ctx, args):
    wheelo = Wheel(args, ctx)
    await wheelo.start()

class Wheel():
    def __init__(self, args, ctx):
        self.args = args
        self.ctx = ctx
    
    async def start(self):
        self.items_number = len(self.args)
        
        if self.items_number == 0:
            channel_members = self.ctx.author.voice.channel.members
            for member in channel_members:
                embed = discord.Embed(colour=member.color)
                embed.set_author(name=member.display_name, icon_url=member.avatar_url)
                await self.ctx.send(embed=embed)
        else:
            starter_embed = discord.Embed(title="Glücksrad", color=discord.Color.green())
            #for i in range(self.items_number): 
            for i in range(self.items_number // 2):  # Anzahl der Reihen die zwei Inline-Elemente haben
                starter_embed.add_field(name=self.args[i], value=".", inline=True)
                starter_embed.set_image(url=self.ctx.author.avatar_url)
                starter_embed.add_field(name=self.args[i], value=".", inline=True)
                starter_embed.add_field(name=".", value=".", inline=False)
                starter_embed.set_image(url=self.ctx.author.avatar_url)
                starter_embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/9/9a/Gull_portrait_ca_usa.jpg")
            await self.ctx.send(embed=starter_embed)

import asyncio
import discord
import random

class Wheel():
    def __init__(self, args, ctx):
        self.args = args
        self.ctx = ctx
    
    async def start(self):
        self.items_number = len(self.args)
        
        if self.items_number == 0:
            self.channel_members = self.ctx.author.voice.channel.members
            for member in self.channel_members:
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
    
    async def pick(self): 
        # Wähle einen Eintrag aus der List und entferne ihn
        # Rückgabe True, wenn nicht beendet
        await self.ctx.send(":arrows_counterclockwise: Drehe...")

        members_left = len(self.channel_members)
        rand_int = random.randint(0, members_left-1)
        chosen_member = self.channel_members.pop(rand_int)

        embed = discord.Embed(colour=chosen_member.color)
        embed.set_author(name=chosen_member.display_name, icon_url=chosen_member.avatar_url)
        await self.ctx.send(embed=embed)
        
        if len(self.channel_members) == 1:
            await self.ctx.send("Letzte übrige Person:")
            embed = discord.Embed(colour=self.channel_members[0].color)
            embed.set_author(name=self.channel_members[0].display_name, icon_url=self.channel_members[0].avatar_url)
            await self.ctx.send(embed=embed)
            await self.ctx.send(":white_check_mark: Glücksrad beendet")
            self.channel_members[0].pop()

            return True
        else:
            await self.ctx.send("Drehe für die nächste Person!")
            
            return False
            
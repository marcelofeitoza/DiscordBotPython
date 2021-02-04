import discord
from discord.ext import commands

class Example(commands.Cog):

    def __init__(self, client):
        self.client = client


    #Event
    @commands.Cog.listener()
    async def on_ready(self):
        print('The bot is ready/online.\nDo something.')

    @commands.command()
    async def hey(self, ctx):
        await ctx.send("I am here. Send '.help' to see what I can do!!")

    #Commands
    #@commands.command()
    #async def ping(self, ctx):
    #    await ctx.send('Pong!')
    

def setup(client):
    client.add_cog(Example(client))
        









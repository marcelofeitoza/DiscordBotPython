# Setup

from typing import Text
import discord, random, os
from discord.ext import commands, tasks

client = commands.Bot(command_prefix= '.')


@client.event
async def on_ready(): # 'on_ready' means that the bot is ready to go
    print('The bot is ready')



#events --------------------------------------------------------------------------
@client.event
# 'on_member_join' means that somthing will happen when somebody enters the server
async def on_member_join(member):
    member = member.capitalize()
    print(f'{member} has joined the server')

@client.event
# 'on_member_remove' means that somthing will happen when somebody leaves the server
async def on_member_remove(member):
    member = member.capitalize()
    print(f'{member} has left from the server')








#commands ------------------------------------------------------------------------
#@client.command()
## 'ping' will answer 'pong'
#async def ping(ctx):  # context = ctx
#    await ctx.send(f'Pong! You have {round(client.latency * 1000)}ms of ping.')




@client.command(aliases = ['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.","It is decidedly so.","Without a doubt.",
                "Yes - definitely.","You may rely on it.","As I see it, yes.",
                "Most likely.","Outlook good.","Yes.",
                "Signs point to yes.","Reply hazy, try again.","Ask again later.",
                "Better not tell you now.","Cannot predict now.","Concentrate and ask again.",
                "Don't count on it.","My reply is no.","My sources say no.",
                "Outlook not so good.","Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')







#clear ---------------------------------------------------------------------------
@client.command()
async def clear(ctx, amount = 10):
    await ctx.channel.purge(limit = amount)







#ban / kick ----------------------------------------------------------------------
@client.command()
async def kick(ctx, member: discord.Member, *, reason = None):  #kicking
    #this member is on the server, can be mentioned
    await member.kick(reason= reason)

@client.command()
async def ban(ctx, member: discord.Member, *, reason = None):   #banning
    await member.ban(reason= reason)
    await ctx.send(f'Banned {member.mention}')






# unban --------------------------------------------------------------------------
@client.command()
async def unban(ctx, *, member):
    #this member is not on the server, can't be mentioned
    banned_users = await ctx.guild.bans() #discord user = Marcelo#1234  -->#guild = server
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user) 
            await ctx.send(f'Unbanned {user.mention}')
            return





# cogs (organize and split up things -----------------------------------------------
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    print('Loaded.')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    print('Unloaded.')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    print('Reloaded.')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')





client.run('ODA1OTY0NDA5OTY4OTE4NTU4.YBii2Q.uADfFLy4AU9djJvuJYTs5lIubJY')

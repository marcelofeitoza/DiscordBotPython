# Setup
import discord, random, os, json
from discord.ext import commands, tasks
from itertools import cycle



def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]



client = commands.Bot(command_prefix= get_prefix)
status = cycle(['Botting', 'Moderating'])



@client.event
async def on_ready(): # 'on_ready' means that the bot is ready to go
    #await client.change_presence(status = discord.Status.do_not_disturb, activity = discord.Game('Botting...'))
    change_status.start()
    print('The bot is ready')   


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("This command doesn't exist. Try '.help' to check all of them!")







@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)


    prefixes[str(guild.id)] = '.'    

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)


    prefixes.pop(str(guild.id))   

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

@client.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

    await ctx.send(f"Prefix changed to: '{prefix}'")






@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount: int):
   await ctx.channel.purge(limit = amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify how many messages to delete.')

#check
def is_it_me(ctx):
    return ctx.author.id == 449777486142636062

@client.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f'Hi I am {ctx.author}')










@tasks.loop(seconds = 5)
async def change_status():
    await client.change_presence(activity = discord.Game(next(status)))


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
@client.command()
# 'ping' will answer 'pong'
async def ping(ctx):  # context = ctx
    await ctx.send(f'Pong! You have {round(client.latency * 1000)}ms of ping.')




@client.command(aliases = ['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.", "It is decidedly so.", "Without a doubt.",
                "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
                "Most likely.", "Outlook good.", "Yes.",
                "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
                "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
                "Don't count on it.", "My reply is no.", "My sources say no.",
                "Outlook not so good.", "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')





#kick / ban ----------------------------------------------------------------------
@client.command()
async def kick(ctx, member: discord.Member, *, reason = None):  #kicking
    #this member is on the server, can be mentioned
    await member.kick(reason= reason)
    await ctx.send(f'Kicked {member.mention}')
    print(f'{member} was kicked')

@kick.error                         #error kicking
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify who you want to kick.')


@client.command()
async def ban(ctx, member: discord.Member, *, reason = None):   #banning
    await member.ban(reason= reason)
    await ctx.send(f'Banned {member.mention}')
    print(f'{member} was banned')

@ban.error                          #error banning
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify who you want to ban.')





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
            print(f'{member} was unbanned')
            return

@unban.error
async def unban_error(ctx, error):         #error unbaning
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify who you want to unban.')

        
        


# cogs (organize and split up things) -----------------------------------------------
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

    



#        for filename in os.listdir('./cogs'):
#          if filename.endswith('.py'):
#                client.load_extension(f'cogs.{filename[:-3]}')





client.run('####BOTTOKKEN####')

##########################################################################################
#             ChickenBot 
# To use this bot the user need to install FFmpeg 
# It's recommended to use https://repl.it/ to remote hosed the bot to make it stayed online
##########################################################################################
import discord
import os
from random import choice
from discord.ext import commands, tasks
from keep_alive import keep_alive

#import the default help command
#inoder to call this help command, user need to
#type in "!help". The prefix "!" can be change by
#the code down below
help_command = commands.DefaultHelpCommand(
    no_category = 'Main commands'
)

#Setting for the command prefix
client = commands.Bot(
    command_prefix="!",
    help_command = help_command
)

# Bot status list
status = ['chicken dinner', 'his feathers!', 'PUBG!']
# Bad words list, if any user said bad words in the server
#bad_words = ['fuck', 'shit', 'piss', 'shit', 'dick', 'asshole', 'bitch', 'bastard', 'damn', 'cunt']

bad_words = []

# To comfirmed discord bot is login
@client.event
async def on_ready():
    change_status.start()
    print('We have loggedin as {0.user}'.format(client))


# Change status every 10 min
@tasks.loop(seconds=600)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))


# Catch error input command
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Command missed required arguments.')


# Command to load cogs
@client.command(name='load', help='This command will load a extension commands ')
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


# Command to unload cogs
@client.command(name='unload', help='This command will unload a extension command ')
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


# Search /cogs folder, it will load all file with .py at the end
# When loading the cogs it will automatically remove last three 
#file name, which is ".py"
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# Command to load listener
# Listener will read all user text message
@client.command(name='listener_on', help='This command will turn on listener ')
async def listener_on(ctx):
    client.add_listener(on_message, name=None)
    await ctx.channel.send("Listener is on")

# Read all user message
@client.listen('on_message')
async def on_message(message):
    # Skip ChickenBot own message
    if message.author == client:
        return
    #Change input message to lower case
    msg = message.content.lower()

    # Check if any user input bad word
    # If bad words found then chickbot will sent out warning message
    if any(word in msg for word in bad_words):
        await message.channel.send("@" + str(message.author)[:-5])
        await message.channel.send("https://memegenerator.net/img/instances/47634591.jpg")    


# Command to unload cogs
@client.command(ame='listener_off', help='This command will turn off listener ')
async def listener_off(ctx):
    client.remove_listener(on_message, name=None)
    await ctx.channel.send("Listener is off")

#Use web server(uptimerobot) to keep the bot alive
keep_alive()        
#Get login information from env filename
client.run(os.getenv('TOKEN'))
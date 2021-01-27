##########################################################################################
#             ChickenBot 
# To use this bot the user need to install FFmpeg 
# It's recommended to use https://repl.it/ to remote hosed the bot to make it stayed online
##########################################################################################
import requests
import discord
import json
import random
import datetime
import pytz
import feedparser
import requests
import webbrowser
import youtube_dl
from random import choice
from replit import db
from joke.jokes import *
from keep_alive import keep_alive
from datetime import datetime
from datetime import tzinfo
from discord.ext import commands, tasks
import os
os.system('chmod +777 ./ffmpeg')
os.system('./ffmpeg')

client = commands.Bot(command_prefix="!")

#Sad word list
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]
#Bot status list
status = ['chicken dinner', 'his feathers!', 'PUBG!']
#To store music
queue = []

#Encouragements words
starter_encouragements = [
  "Cheer up",
  "Hang in there",
  "You are a greate person / bot!"
]


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)       

if "responding" not in db.keys():
  db["responding"] = True

#Get quote from zenquotes.io
#Learn from YouTube by (FreeCodeCamp.org)
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

#Database control
def update_encouragements(encouraging_message):
  #encouragements is the key
  #If key is not in the database we ill add it
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements  

#To comfirmed discord bot is login
@client.event
async def on_ready():
  change_status.start()
  print('We have loggedin as {0.user}'.format(client))

#Here is all the command options chickekBot has
@client.command(name='inspire', help='This command returns a inspire quote ' )
async def inspire(ctx):
   quote = get_quote()
   await ctx.send(quote)

@client.command(name='joke', help='This command returns a random joke '  )
async def jokes(ctx):
   from random import choice
   joke = choice([geek, icanhazdad, chucknorris, icndb])()
   await ctx.send(joke)   

@client.command(name='news', help='This command returns three pc game news '  )
async def news(ctx):
   feed = feedparser.parse("https://www.gameinformer.com/news.xml")

   x = 0

   for entry in feed.entries:
    article_link = entry.link
    await ctx.send(article_link)  
    x+= 1

    if(x == 3 ): 
       break

@client.command(name='time', help='This command returns current Pacific time ')
async def time(ctx):
   timestamp = datetime.now(pytz.timezone('US/Pacific'))
   await ctx.send("The current time is " + timestamp.strftime(r"%I:%M %p"))       
     

@client.command(name='weather', help='This command needs to include a city name to return current weather of that city' )
async def weather(ctx, *, args):
    city = str(args[:]) 
    user_api = os.environ['APIKEY']
    location = city

    complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+user_api
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()

    if api_data['cod'] == '404':
      await ctx.send ("Invalid City: {}, please check your City name".format(location))
    else: 
      #create variables to store and display data
      temp_city_c = ( (api_data['main']['temp']) - 273.15)
      temp_city_f = ((( (api_data['main']['temp']) - 273.15)*9/5)+32) 
      weather_desc = "Current weather desc  :"+ api_data['weather'][0]['description']
      hmdt = "Current Humidity      : " + str(api_data['main']['humidity']) + " %"
      wind_spd = "Current wind speed    : " + str(api_data['wind']['speed']) + " kmph"
      date_time = datetime.now(pytz.timezone('US/Pacific'))
      emoji = '\N{THUMBS UP SIGN}'

      await ctx.send ("-------------------------------------------------------------")
      await ctx.send ("Weather Stats for - {}  || {}".format(location.upper(), date_time))
      await ctx.send ("-------------------------------------------------------------")

      await ctx.send ("Current temperature in Celsius is: {:.2f} deg C".format(temp_city_c))
      await ctx.send ("Current temperature in Fahrenheit is: {:.2f} deg F".format(temp_city_f))
      await ctx.send (weather_desc)
      await ctx.send (hmdt)
      await ctx.send (wind_spd) 
      await ctx.send("Have a good day.")
      await ctx.send(emoji)  

#All the music function (from R.K. Coding)
@client.command(name='join', help='This command makes the bot join the voice channel')
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return
    
    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

@client.command(name='queue', help='This command adds a song to the queue')
async def queue_(ctx, url):
    global queue

    queue.append(url)
    await ctx.send(f'`{url}` added to queue!')

@client.command(name='remove', help='This command removes an item from the list')
async def remove(ctx, number):
    global queue

    try:
        del(queue[int(number)])
        await ctx.send(f'Your queue is now `{queue}!`')
    
    except:
        await ctx.send('Your queue is either **empty** or the index is **out of range**')
        
@client.command(name='play', help='This command plays songs')
async def play(ctx):
    global queue

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(queue[0], loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Now playing:** {}'.format(player.title))
    del(queue[0])

@client.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.pause()

@client.command(name='resume', help='This command resumes the song!')
async def resume(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.resume()

@client.command(name='view', help='This command shows the queue')
async def view(ctx):
    await ctx.send(f'Your queue is now `{queue}!`')

@client.command(name='leave', help='This command stops makes the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

@client.command(name='stop', help='This command stops the song!')
async def stop(ctx):
    server = ctx.message.guild
    voice_channel = server.voice_client

    voice_channel.stop()

@tasks.loop(seconds=20)
async def change_status():
    await client.change_presence(activity=discord.Game(choice(status)))

#Read user message and response
@client.listen('on_message')
async def on_message(message):

  #If meessage is from bot itself return
  if message.author == client.user:
    return

  msg = message.content  

  #Check if user input sad word
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))   
  
  #Optino to add or delete new encouragements word from database
  if msg.startswith("$new"):
    encouraging_message = msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  #Enable or disable chickenbot
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")  

#Use web server(uptimerobot) to keep the bot alive
keep_alive()        
#Get login information from env
client.run(os.getenv('TOKEN'))
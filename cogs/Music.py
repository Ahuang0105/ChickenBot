import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os

class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='join', help='This command makes the bot join the voice channel')
    async def join(self, ctx):
        #get user voice channel name
        channel = ctx.message.author.voice.channel   
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await voice.disconnect()

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
            print(f"The ChickenBot has connected to {channel}\n")

        await ctx.send(f"ChickenBot joined {channel}")    

    @commands.command(name='leave', help='This command makes the bot leave the voice channel')
    async def leave(self, ctx):
        #get user voice channel name
        channel = ctx.message.author.voice.channel   
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"The bot has left {channel}")
            await ctx.send(f"ChickenBot Left {channel}")
        else:
            await ctx.send("I am not in a voice channel")

    @commands.command(pass_context=True, aliases=['p', 'pla'])
    async def play(self, ctx, url: str):

        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file")

        except PermissionError:
            print("Trying to delete song file, but it's being played")
            await ctx.send("ERROR: Music playing")
            return

        await ctx.send("Getting everything ready now")

        voice = get(self.client.voice_clients, guild=ctx.guild)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing: {nname[1]}")
        print("playing\n")        


def setup(client):
    client.add_cog(Music(client))

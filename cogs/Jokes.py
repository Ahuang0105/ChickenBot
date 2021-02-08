import discord
import os
from discord.ext import commands
from joke.jokes import *

# A simple API I found online that stored lots of joke
class Jokes(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='joke', help='This command returns a random joke ')
    async def jokes(self, ctx):
        from random import choice
        joke = choice([geek, icanhazdad, chucknorris, icndb])()
        await ctx.send(joke)

def setup(client):
    client.add_cog(Jokes(client))
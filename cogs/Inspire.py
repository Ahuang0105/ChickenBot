import discord
import os
import json
import requests
from discord.ext import commands
from joke.jokes import *

class Inspire(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Get quote from zenquotes.io
    # Learn from YouTube by (FreeCodeCamp.org)
    @commands.command(name='inspire', help='This command returns a inspire quote ')
    async def inspire(self, ctx):
        quote = get_quote()
        await ctx.send(quote)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)

def setup(client):
    client.add_cog(Inspire(client))
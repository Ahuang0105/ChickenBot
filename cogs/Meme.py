import praw
import random
import os
from discord.ext import commands

reddit = praw.Reddit(client_id= os.getenv('id'),
                     client_secret= os.getenv('secret'),
                     user_agent='ChickenBot')

# The praw API will parser seleced information from reddit
# For chikcenBot we only want to display memes 
class Meme(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='meme', help='This command returns a random meme from reddit')
    async def meme(self, ctx):
        #use memes subreddit
        memes_submissions = reddit.subreddit('memes').hot()
        #Random choice 1 meme from the top 10 memes
        post_to_pick = random.randint(1, 10)

        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        await ctx.send(submission.url)

def setup(client):
    client.add_cog(Meme(client))
import discord
import feedparser
from discord.ext import commands


class News(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name='news', help='This command returns the amount  of pc game news user want')
    async def news(self, ctx, *args):
        #the feed is an list file
        feed = feedparser.parse("https://www.gameinformer.com/news.xml")
        
        # if no user didn't input how many news they want 
        # the chicken will print all the pc game news from
        # today
        if not args:
          for entry in feed.entries:
            # We only print the link since discord will automatically
            # display the pic and some content
            article_link = entry.link
            await ctx.send(article_link)

        # if there is an input number 
        # print only the amount  user want     
        else:
           x = int(args[0])

           for i in range(x):
             await ctx.send(feed.entries[i].link)
        
def setup(client):
    client.add_cog(News(client))
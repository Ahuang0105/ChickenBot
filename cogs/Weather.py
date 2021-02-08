import discord
import datetime
import pytz
import requests
import json
import os
from discord.ext import commands
from datetime import datetime
from datetime import tzinfo

class Weather(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #Command to return current time 
    @commands.command(name='time', help='This command returns current Pacific time ')
    async def time(self, ctx):
        timestamp = datetime.now(pytz.timezone('US/Pacific'))
        await ctx.send("The current time is " + timestamp.strftime(r"%I:%M %p"))
    
    #Command to return input city's current weather
    #Example "!weather los angeles"
    @commands.command(name='weather',
                    help='This command returns current weather of the input city')
    async def weather(self, ctx, *, args):
        city = str(args[:])
        user_api = "5dc2324d2c97885c17e3f057a4245fdd"
        location = city

        complete_api_link = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&appid=" + user_api
        api_link = requests.get(complete_api_link)
        api_data = api_link.json()
        
        #If input city name not found in the date base return invalid message
        if api_data['cod'] == '404':
            await ctx.send("Invalid City: {}, please check your City name".format(location))
        #Return current weather    
        else:
            # create variables to store and display data
            temp_city_c = ((api_data['main']['temp']) - 273.15)
            temp_city_f = ((((api_data['main']['temp']) - 273.15) * 9 / 5) + 32)
            weather_desc = "Current weather desc  :" + api_data['weather'][0]['description']
            hmdt = "Current Humidity      : " + str(api_data['main']['humidity']) + " %"
            wind_spd = "Current wind speed    : " + str(api_data['wind']['speed']) + " kmph"
            date_time = datetime.now(pytz.timezone('US/Pacific'))
            emoji = '\N{THUMBS UP SIGN}'

            await ctx.send("-------------------------------------------------------------")
            await ctx.send("Weather Stats for - {}  || {}".format(location.upper(), date_time.strftime(r"%I:%M %p")))
            await ctx.send("-------------------------------------------------------------")
            await ctx.send("Current temperature in Celsius is: {:.2f} deg C".format(temp_city_c))
            await ctx.send("Current temperature in Fahrenheit is: {:.2f} deg F".format(temp_city_f))
            await ctx.send(weather_desc)
            await ctx.send(hmdt)
            await ctx.send(wind_spd)
            await ctx.send("Have a good day.")
            await ctx.send(emoji)

def setup(client):
    client.add_cog(Weather(client))
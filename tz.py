import os
import discord
from dotenv import load_dotenv
import requests
import datetime
import config

ZONE_HOUR = -1
ZONE_INFO = {}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN = config.discord_token

intents = discord.Intents.default()
intents.message_content=True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord!')

@client.event
async def on_message(message):
    global ZONE_HOUR
    global ZONE_INFO
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello')
    
    if message.content.startswith('!tz'):
        # Check time on stored TZ
        now = datetime.datetime.now()
        if now.hour == ZONE_HOUR:
            # Return Stored Info because it wont have changed
            await message.channel.send("Same Zone Info")
            await message.channel.send(ZONE_INFO)
        else:
            await message.channel.send("New Zone")
            if now.second > 5: # wait 5 seconds for tz to update 
                # If from current time slot, send in chat
                # Else query API, store time & zone & send
                token= config.rw_key
                # r = requests.get("https://d2runewizard.com/api/terror-zone", params={"token": token})
                r = {"status_code": 200, "r.json()": {'zone': 'Arreat Plateau and Pit of Acheron', 'act': 'act5', 'lastReportedBy': {'displayName': 'thewiz', 'uid': 'yY1dEKJhXNRrBeySKQRqxWYaZ712'}, 'lastUpdate': {'seconds': 1677971582, 'nanoseconds': 39000000}, 'reportedZones': {'Arreat Plateau and Pit of Acheron': 24}, 'highestProbabilityZone': {'zone': 'Arreat Plateau and Pit of Acheron', 'act': 'act5', 'amount': 24, 'probability': 1}}}
                
                # if r.status_code == 200:
                if r['status_code'] == 200:
                    # Received Request
                    await message.channel.send(f"Request sent & received, {r['r.json()']}")
                    # ZONE_INFO = r.json()
                    ZONE_INFO = r['r.json()']
                    ZONE_HOUR = now.hour
                    await message.channel.send([ZONE_INFO, ZONE_HOUR])
                else:
                    # Logic Here
                    await message.channel.send(f"could not retrieve terror zone data, error code {r.status_code}")
client.run(TOKEN)
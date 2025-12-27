import requests
import discord
from discord import option
from discord.ext import tasks
import os 
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

bot = discord.Bot(intents=discord.Intents.all())

async def respon():
    url = "https://publicapi.nationsglory.fr/country/list/blue"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer NGAPI_!IK5XrC3*k%A*muQKAPKu^Op9^XRBO24949bbd48e26609a198f0b167e2a360ac"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    claimed_names = [item["name"] for item in data["claimed"]]

    for index in claimed_names:
        urll = f"https://publicapi.nationsglory.fr/country/blue/{index}"
        responsse = requests.get(urll, headers=headers)
        dataa = responsse.json()

        name = dataa.get("name")
        power = int(dataa.get("power", 0))
        count_claims = int(dataa.get("count_claims", 0))

        if count_claims > power:
            return name  
    return None  


@bot.event
async def on_ready():
    print("connected")
    auto_message.start()  


@bot.slash_command(name="join", description="how to join?")
async def join(ctx):
    await ctx.respond("Pour nous rejoindre, va sur https://www.nationsglory.fr, télécharge le launcher, crée toi un compte et lance le jeux. entre sur le serveur **blue** et fais /f join zimbabwe.")

@bot.slash_command(name="souspower", description="verifie les pays sous-power")
async def join(ctx):
    result = await respon()
    if result:
        channel = bot.get_channel(1454267038087385128)
        timestamp = datetime.utcnow().time()
        await channel.send(f"{timestamp} || {result}")
    await ctx.respond("okay, je lance")

@tasks.loop(seconds=3600)
async def auto_message():
    result = await respon()
    if result:
        channel = bot.get_channel(1454267038087385128)
        timestamp = datetime.utcnow().time()
        await channel.send(f"{timestamp}, || {result}")


bot.run(os.getenv("DISCORD_TOKEN"))

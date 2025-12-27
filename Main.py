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

    results = []  

    for index in claimed_names:
        urll = f"https://publicapi.nationsglory.fr/country/blue/{index}"
        responsse = requests.get(urll, headers=headers)
        dataa = responsse.json()

        name = dataa.get("name")
        power = int(dataa.get("power", 0))
        count_claims = int(dataa.get("count_claims", 0))

        if count_claims > power:
            results.append(name)

    return results  
 


@bot.event
async def on_ready():
    print("connected")
    auto_message.start()  


@bot.slash_command(name="join", description="how to join?")
async def join_cmd(ctx):
    await ctx.respond("Pour nous rejoindre, va sur https://www.nationsglory.fr, télécharge le launcher, crée toi un compte et lance le jeux. entre sur le serveur **blue** et fais /f join zimbabwe.")


@bot.slash_command(name="souspower", description="verifie les pays sous-power")
async def souspower_cmd(ctx):
    results = await respon()
    channel = bot.get_channel(1454267038087385128)

    if results:
        timestamp = datetime.utcnow().strftime("%H:%M:%S")
        liste = ", ".join(results)
        await channel.send(f"{timestamp} || Sous-power : {liste}")
    else:
        await channel.send("Aucun pays sous-power pour le moment.")

    await ctx.respond("okay, je lance")



@bot.slash_command(name="machine", description="Wiki sur les machines")
async def machine(ctx):
    await ctx.respond("Pour en savoir plus sur les machines, rends toi sur https://wiki.nationsglory.fr/fr/category/java-les-machines-wj7rgi/")


@bot.slash_command(name="nationsglory", description="Nationsglory, c'est quoi?")
async def ng(ctx):
    await ctx.respond("NationsGlory est un serveur Minecraft très populaire, basé sur un concept unique : tu incarnes un pays réel sur une carte de la Terre, et tu dois le développer, le défendre et le faire prospérer.")


@bot.slash_command(name="wiki", description="Le wiki de nationsglory")
async def wiki(ctx):
    await ctx.respond("Retrouve le wiki officiel de Nationsglory ici ==> https://wiki.nationsglory.fr/fr/")


@bot.slash_command(name="forum", description="Le Forum de nationsglory")
async def forum(ctx):
    await ctx.respond("Retrouve le Codex officiel de Nationsglory ici ==> https://nationsglory.fr/forums/")


@bot.slash_command(name="discord", description="Les Différent Serveur discord de nationsglory")
async def discord(ctx):
    await ctx.respond("Retrouve le Serveur Nationsglory officle ==> https://discord.gg/nationsglory \n et le serveur discord du blue ==> https://discord.gg/nationsglory-blue-780390423109042196")


@bot.slash_command(name="blue", description="Le blue, c'est quoi?")
async def blue(ctx):
    await ctx.respond("Le serveur blue fais partie de l'un des sous-serveur de nationsglory. c'est le premier crée. il possède sont propre **staff**, sont propre **spawn**, ces propres events, thèmes etc...")


@bot.slash_command(name="site", description="Le site de nationsglory")
async def site(ctx):
    await ctx.respond("Retrouve le site de nationsglory ici ==> https://www.nationsglory.fr")


@tasks.loop(seconds=3600)
async def auto_message():
    result = await respon()
    if result:
        channel = bot.get_channel(1454267038087385128)
        timestamp = datetime.utcnow().strftime("%H:%M:%S")
        await channel.send(f"{timestamp} || {result}")


bot.run(os.getenv("DISCORD_TOKEN"))

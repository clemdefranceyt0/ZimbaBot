import requests
import nextcord as discord
from nextcord.ext import commands, tasks
import os
from dotenv import load_dotenv
from datetime import datetime
import asyncio

# Fix event loop for Python 3.11+
asyncio.set_event_loop(asyncio.new_event_loop())

load_dotenv()

bot = commands.Bot(
    intents=discord.Intents.all(),
    command_prefix="!"  # requis par nextcord même si tu n'utilises que des slash commands
)

# ---------------------------------------------------------
#   FONCTION : Vérifie les pays sous-power
# ---------------------------------------------------------
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


# ---------------------------------------------------------
#   EVENT : Bot prêt
# ---------------------------------------------------------
@bot.event
async def on_ready():
    print("connected")
    await bot.sync_application_commands()  # sync Nextcord
    auto_message.start()


# ---------------------------------------------------------
#   COMMANDES SLASH
# ---------------------------------------------------------
@bot.slash_command(name="join", description="Comment nous rejoindre ?")
async def join_cmd(ctx):
    await ctx.response.send_message(
        "Pour nous rejoindre, va sur https://www.nationsglory.fr, télécharge le launcher, "
        "crée un compte et lance le jeu. Entre sur le serveur **blue** et fais `/f join zimbabwe`."
    )


@bot.slash_command(name="souspower", description="Vérifie les pays sous-power")
async def souspower_cmd(ctx):
    results = await respon()
    channel = bot.get_channel(1454267038087385128)

    if results:
        timestamp = datetime.utcnow().strftime("%H:%M:%S")
        liste = ", ".join(results)
        await channel.send(f"{timestamp} || Sous-power : {liste}")
    else:
        await channel.send("Aucun pays sous-power pour le moment.")

    await ctx.response.send_message("Okay, je lance.")


@bot.slash_command(name="machine", description="Wiki sur les machines")
async def machine(ctx):
    await ctx.response.send_message(
        "Wiki des machines : https://wiki.nationsglory.fr/fr/category/java-les-machines-wj7rgi/"
    )


@bot.slash_command(name="nationsglory", description="NationsGlory, c'est quoi ?")
async def ng(ctx):
    await ctx.response.send_message(
        "NationsGlory est un serveur Minecraft où tu incarnes un pays réel sur une carte de la Terre "
        "et tu dois le développer, le défendre et le faire prospérer."
    )


@bot.slash_command(name="wiki", description="Wiki de NationsGlory")
async def wiki(ctx):
    await ctx.response.send_message("Wiki officiel : https://wiki.nationsglory.fr/fr/")


@bot.slash_command(name="forum", description="Forum de NationsGlory")
async def forum(ctx):
    await ctx.response.send_message("Forum officiel : https://nationsglory.fr/forums/")


@bot.slash_command(name="discord", description="Serveurs Discord de NationsGlory")
async def discord_cmd(ctx):
    await ctx.response.send_message(
        "Serveur officiel : https://discord.gg/nationsglory\n"
        "Serveur Blue : https://discord.gg/nationsglory-blue-780390423109042196"
    )


@bot.slash_command(name="blue", description="Le serveur Blue, c'est quoi ?")
async def blue(ctx):
    await ctx.response.send_message(
        "Le serveur Blue est le premier serveur de NationsGlory. "
        "Il possède son propre staff, spawn, events et thèmes."
    )


@bot.slash_command(name="site", description="Site officiel de NationsGlory")
async def site(ctx):
    await ctx.response.send_message("Site officiel : https://www.nationsglory.fr")


# ---------------------------------------------------------
#   TÂCHE AUTOMATIQUE : Vérifie toutes les heures
# ---------------------------------------------------------
@tasks.loop(seconds=3600)
async def auto_message():
    results = await respon()
    if results:
        channel = bot.get_channel(1454267038087385128)
        timestamp = datetime.utcnow().strftime("%H:%M:%S")
        liste = ", ".join(results)
        await channel.send(f"{timestamp} || Sous-power : {liste}")


# ---------------------------------------------------------
#   LANCEMENT DU BOT
# ---------------------------------------------------------
bot.run(os.getenv("DISCORD_TOKEN"))

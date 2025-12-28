import aiohttp
import nextcord as discord
from nextcord.ext import commands, tasks
import os
from dotenv import load_dotenv
from datetime import datetime
import asyncio

load_dotenv()

bot = commands.Bot(
    intents=discord.Intents.all(),
    command_prefix="!"
)

# ---------------------------------------------------------
#   SESSION HTTP GLOBALE (optimisation)
# ---------------------------------------------------------
session: aiohttp.ClientSession = None

async def create_session():
    global session
    if session is None or session.closed:
        session = aiohttp.ClientSession()


# ---------------------------------------------------------
#   FONCTION : Vérifie les pays sous-power (optimisée)
# ---------------------------------------------------------
async def fetch_country(name, headers):
    url = f"https://publicapi.nationsglory.fr/country/blue/{name}"
    async with session.get(url, headers=headers) as resp:
        if resp.status != 200:
            return None
        return await resp.json()

async def respon():
    await create_session()

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('NG_API_KEY')}"
    }

    async with session.get("https://publicapi.nationsglory.fr/country/list/blue", headers=headers) as resp:
        if resp.status != 200:
            return []
        data = await resp.json()

    claimed_names = [item["name"] for item in data["claimed"]]

    tasks_list = [fetch_country(name, headers) for name in claimed_names]
    countries = await asyncio.gather(*tasks_list)

    results = []
    for dataa in countries:
        if not dataa:
            continue

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
    await bot.sync_application_commands()

    if not auto_message.is_running():
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
    await ctx.response.defer()

    results = await respon()
    channel = bot.get_channel(1454267038087385128)

    if not channel:
        return await ctx.followup.send("Erreur : channel introuvable.")

    if results:
        timestamp = datetime.utcnow().strftime("%H:%M:%S")
        liste = ", ".join(results)
        await channel.send(f"{timestamp} || Sous-power : {liste}")
    else:
        await channel.send("Aucun pays sous-power pour le moment.")

    await ctx.followup.send("Okay, je lance.")


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


@bot.slash_command(name="presentation", description="une presentation de nationsglory!")
async def pres(ctx):
    await ctx.response.send_message("Regarde attentivement cette vidéo pour apprendre les bases de nationsglory! https://youtu.be/u5b5t-9s2nE")


# ---------------------------------------------------------
#   TÂCHE AUTOMATIQUE : Vérifie toutes les heures
# ---------------------------------------------------------
@tasks.loop(seconds=3600)
async def auto_message():
    results = await respon()
    channel = bot.get_channel(1454267038087385128)

    if not channel:
        return

    if results:
        timestamp = datetime.utcnow().strftime("%H:%M:%S")
        liste = ", ".join(results)
        await channel.send(f"{timestamp} || Sous-power : {liste}")


# ---------------------------------------------------------
#   LANCEMENT DU BOT
# ---------------------------------------------------------
bot.run(os.getenv("DISCORD_TOKEN"))

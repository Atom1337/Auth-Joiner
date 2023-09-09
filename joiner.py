# purely made in python by aiatom | don't skid

import os
import sys
import requests
import json
import time
from threading import Thread
import discord
from discord.ext import commands

logo = """
    _   _                    
   / \ | |_ ___  _ __ ___    
  / _ \| __/ _ \| '_ ` _ \   
 / ___ \ || (_) | | | | | |_ 
/_/   \_\__\___/|_| |_| |_(_)

    """
print(logo)

API_ENDPOINT = 'https://canary.discord.com/api/v9'
CLIENT_ID = int(input("Enter BOT ID: "))
CLIENT_SECRET = input("Enter BOT SECRET: ")
REDIRECT_URI = input("Enter BOT REDIRECT: ")
tkn = input("Enter BOT TOKEN: ")
ltc = "your_ltc_addy"


intents = discord.Intents.all()
intents.typing = False
intents.presences = False
OWNER_IDS = []
xdd = []
async def nopre(client, message):
    if message.author.id in OWNER_IDS:
        return ""
    else:
        return "."
   
bot = commands.Bot(command_prefix=nopre, intents=intents, owner_ids=OWNER_IDS)

bot.remove_command("help")

@bot.command()
async def help(ctx):
   embed = discord.Embed(description=f"```help, join (guild id) (start from) (amount),getguild, link, ltc.```")
   await ctx.send(embed=embed, mention_author=False)
def add_to_guild(access_token, userID, guild_Id):
    while True:
        url = f"{API_ENDPOINT}/guilds/{guild_Id}/members/{userID}"

        botToken = tkn
        data = {
        "access_token" : access_token,
    }
        headers = {
        "Authorization" : f"Bot {botToken}",
        'Content-Type': 'application/json'

    }
        response = requests.put(url=url, headers=headers, json=data)
        print(response.text)
        if response.status_code in (200, 201, 204):
          if "joined" not in response.text:
            print(f"[INFO]: User {userID} is already in {guild_Id}")

          print(f"[INFO]: Joined {userID} to {guild_Id}")
          break
        elif response.status_code == 429:
           print(response.status_code)
           print(response.text)
           if 'retry_after' in response.text:
               sleepxd = int(response.json()['retry_after']) + 0.5
               print("sleeping for:", sleepxd, "seconds")
               time.sleep(sleepxd)
               continue
           else:
             os.system("kill 1")
    # ... (same implementation as before)

count = 0

@bot.command()
@commands.cooldown(3, 10, commands.BucketType.user)                   
async def ping(ctx):
  embed = discord.Embed(title="Pong", description=f"**`{int(bot.latency * 1000)}ms`**", colour=00000) 
  embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/970164635170902026.gif?v=1&size=64&quality=lossless')
  await ctx.reply(embed=embed, mention_author=False)



f = open('stock.txt', 'r').readlines()



@bot.command()
@commands.is_owner()
async def getguild(ctx, guild_id: int):
    x = bot.get_guild(guild_id)
    embed = discord.Embed(description=f"Server name : {x.name}\nServer Members: {len(x.members)}")
    await ctx.send(embed=embed, mention_author=False)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
@commands.is_owner()
async def join(ctx, guild_id: int, starter: int, amount: int):
    x = bot.get_guild(guild_id)
    await ctx.send("Found Server... ")
    await ctx.send(f"Started from {len(x.members)} ")
    embed = discord.Embed(description=f"Adding {amount} Members to {x.name}")
    embed1 = discord.Embed(description=f"Successfully added {amount} Members to {guild_id}")
    await ctx.send(embed=embed, mention_author=False)
    f = open("stock.txt", "r").readlines()

    print("Guild ID:", guild_id)
    print("Start from:", starter)
    print("Amount:", amount)

    for xx, line in enumerate(f, start=1):
        if xx < starter:
            continue
        elif amount < xx - starter + 1:
            break

        line = line.strip()
        line = line.split(":")
        key = line[0]
        value = line[1]
        
        
        add_to_guild(value, key, guild_id)
    
    await ctx.send(embed=embed1, mention_author=False)



def count_lines(filename):
    try:
        with open(filename, "r") as file:
            return sum(1 for _ in file)
    except FileNotFoundError:
        return 0

@bot.command()
async def stock(ctx):
    try:
        database_lines = count_lines("stock.txt")
        

        embed = discord.Embed(title="Stock", description=f"Stock: {database_lines}")
        await ctx.send(embed=embed, mention_author=False)

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command()
async def ltc(ctx):
    embed = discord.Embed(description=ltc)
    await ctx.send(embed=embed, mention_author=False)

@bot.command(aliases=["inv","invite"])
async def link(ctx):
    embed = discord.Embed(description="https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}}&permissions=8&scope=bot")
    await ctx.send(embed=embed, mention_author=False)





bot.run(tkn)

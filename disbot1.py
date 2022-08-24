import discord
import os
import json
from dotenv import load_dotenv
from discord.ext import commands
import pymongo
from pymongo import MongoClient

#import time

load_dotenv()

DISCORD_TOKEN = os.getenv("TOKEN")
DB_TOKEN = os.getenv("DB")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents,
                   allowed_mentions=discord.AllowedMentions.none())

users = {}###

cluster = MongoClient(DB_TOKEN)

db = cluster["Skyrim"]
collection = db["Skyrim"]

@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong")
    post = {"_id": ctx.author.id}
    user = collection.find(post)
    for result in user:
        score = result["score"]
    await ctx.channel.send("DB pong")

@bot.command()
async def stats(ctx, *arg):
    if(len(arg) == 0):
        post = {"_id": ctx.author.id}
        user = collection.find(post)
        for result in user:
                score = result["score"]
        await ctx.channel.send(ctx.author.name + ": " + str(score))

        
    elif(arg[0].lower() == "all"):
        post = {}
        user = collection.find(post)
        x = ""
        for result in user:
            x += (await bot.fetch_user(result["_id"])).name + ": " + str(result["score"]) + "\n"###
        if(x != ""):
            #time.sleep(5)
            await ctx.channel.send(x)
    else:
        if(len(arg[0]) > 3):
            idd = arg[0][2:-1]
            x = await bot.fetch_user(idd)
            post = {"_id": x.id}
            user = collection.find(post)
            score = 0
            print(idd)
            for result in user:
                
                score = result["score"]
            await ctx.channel.send(x.name + ": " + str(score))

@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:
        print(f"- {guild.id} (name: {guild.name})")
        guild_count = guild_count + 1
    #await bot.get_channel("1011786977856729131").send("bot is online")
    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")

@bot.event
async def on_message(message):
    if (":pray" in message.content):
        
        post = {"_id": message.author.id}
        if (collection.count_documents(post) == 0):
            post = {"_id": message.author.id, "score": 1}
            collection.insert_one(post)

        else: 
            user = collection.find(post)
            for result in user:
                score = result["score"]
            score = score + 1
            collection.update_one({"_id":message.author.id}, {"$set":{"score":score}})

        print("Prise Tod Howards")
        #await message.channel.send("Prise Tod Howards")
    else:
        await bot.process_commands(message)


bot.run(DISCORD_TOKEN)

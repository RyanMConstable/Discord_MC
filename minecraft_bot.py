#!/usr/bin/python3

import discord
import os, subprocess # default module
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv("/home/president/minecraft/.env")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!",intents=intents) # prefix is the bot command

@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.CustomActivity(name='Server Offline'))
    print(f"{bot.user} is ready and online!")

@bot.hybrid_command(name="help_mc")
async def help_mc(ctx):
    await ctx.send("Use '/startserver' to start the minecraft server.")

@bot.hybrid_command(name="startserver")
async def startserver(ctx):
    if os.system("ps aux | grep minecraft_server.jar | grep -v grep") != 256:
        await ctx.send("Server is already running bozo")
        return

    try:
        os.chdir("/home/president/minecraft/minecraft_server_1.21.4")
        result = subprocess.Popen(["java", "-Xmx4096M", "-Xms4096M", "-jar", "minecraft_server.jar", "nogui"])
        await ctx.send("Server started, the server will go offline after 5 minutes of no activity")
        await bot.change_presence(activity=discord.CustomActivity(name='Server Online'))
    except Exception as e:
        await ctx.send("Failed to start server, check if the server is already running")

@bot.hybrid_command(name="status")
async def status(ctx):
    await ctx.send("This is a test")

bot.run(os.getenv("DISCORDMCBOT"))

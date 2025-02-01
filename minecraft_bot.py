#!/usr/bin/python3

import discord
import os, subprocess # default module
from discord.ext import commands
from dotenv import load_dotenv
import pika
import aio_pika
import asyncio

async def receive_message_queue():
    connection = await aio_pika.connect_robust('amqp://guest:guest@localhost/')
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("mc_status")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    await bot.get_channel(1321172413060481175).send("Server is going offline")
                    await bot.change_presence(activity=discord.CustomActivity(name='Server Offline'))


load_dotenv("/home/president/minecraft/.env")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!",intents=intents) # prefix is the bot command

@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.CustomActivity(name='Server Offline'))
    await receive_message_queue()
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

async def send_offline_message():
    await ctx.send("Server offline")

bot.run(os.getenv("DISCORDMCBOT"))

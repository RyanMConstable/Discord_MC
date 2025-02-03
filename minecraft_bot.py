#!/usr/bin/python3

import discord
import os, subprocess # default module
from discord.ext import commands
from dotenv import load_dotenv
import pika
import aio_pika
import asyncio

async def receive_message_queue(ctx, messageID):
    session_user_list = []
    connection = await aio_pika.connect_robust('amqp://guest:guest@localhost/')
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("mc_status")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    new_message = message.body.decode('utf-8')
                    print(new_message)
                    if new_message == 'Server closed':
                        print("CLOSING SERVER")
                        await bot.change_presence(activity=discord.CustomActivity(name='Server Offline'))

                        discord_message = await ctx.fetch_message(messageID)

                        embed = discord_message.embeds[0]
                        embed.title = "Session Status: OFFLINE"
                        embed.description = f"No users played"
                        if session_user_list != []:
                            embed.description = f"Session Users:\n{'\n'.join(session_user_list)}"
                        embed.color = discord.Color.red()

                        await discord_message.delete()

                        await ctx.send(embed=embed)
                        await bot.get_channel(ctx.channel.id).send("Server is going offline")
                        return
                    if new_message == 'Empty':
                        #Do stuff for empty
                        discord_message = await ctx.fetch_message(messageID)

                        embed = discord_message.embeds[0]
                        embed.description = "No Users Online"

                        await discord_message.edit(embed=embed)


                    else:
                        #This is where you get a string of lists
                        users_online = new_message.split(" ")
                        for user in users_online:
                            if user not in session_user_list:
                                session_user_list.append(user)

                        discord_message = await ctx.fetch_message(messageID)

                        embed = discord_message.embeds[0]
                        embed.description = f"User List:\n{'\n'.join(users_online)}"

                        await discord_message.edit(embed=embed)


load_dotenv("/home/president/minecraft/.env")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!",intents=intents) # prefix is the bot command

@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.CustomActivity(name='Server Offline'))
    #await receive_message_queue()
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

    #Below we want to send an embedded message
    embed = discord.Embed(
            title="Session Status: ONLINE",
            description="Starting Server...",
            color=discord.Color.green()
        )
    message = await ctx.send(embed=embed)
    await receive_message_queue(ctx, message.id)

@bot.hybrid_command(name="status")
async def status(ctx):
    await ctx.send("This is a test")

async def send_offline_message():
    await ctx.send("Server offline")

bot.run(os.getenv("DISCORDMCBOT"))

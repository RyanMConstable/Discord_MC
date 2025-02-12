#!/usr/bin/python3

from dotenv import load_dotenv
from mcstatus import JavaServer
import subprocess
import os
import pika
from current_status import return_status

def send_close_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='mc_status')
    channel.basic_publish(exchange='', routing_key='mc_status', body='Server closed')
    connection.close()

def send_status_to_queue():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='mc_status')
    channel.basic_publish(exchange='', routing_key='mc_status', body=f'{return_status()}')
    connection.close()


if __name__ == "__main__":
    load_dotenv('/home/president/minecraft/.env')

    try:
        server = JavaServer(os.getenv("MYIP"), 25565)
        status = server.status()
    except Exception as e:
        print("Server is down or ip is wrong, most likely server is down")
        exit()

    players_online = status.players.online
    send_status_to_queue()

    if players_online == 0:
        os.system("echo 0 >> /home/president/minecraft/test")
        f = open("/home/president/minecraft/test")
        minutes_with_no_players = len(f.readlines())
        f.close()
        if minutes_with_no_players >= 5:
            os.system("rm /home/president/minecraft/test")
            os.system("ps ax | grep minecraft_server.jar | grep -v grep | awk '{print $1}' > /home/president/minecraft/mcserverps")
            f = open("/home/president/minecraft/mcserverps")
            mcserverps = f.read().splitlines()[0]
            f.close()
            os.system("rm /home/president/minecraft/mcserverps")
            print(mcserverps)
            os.system(f"kill {mcserverps}")

            send_close_queue()
    else:
        if os.path.exists("/home/president/minecraft/test"):
            os.system("rm /home/president/minecraft/test")

#!/usr/bin/python3

from mcstatus import JavaServer
import subprocess
import os

server = JavaServer(os.getenv("MYIP"), 25565)

status = server.status()
result = subprocess.run(["ps", "ax", "|", "grep", "minecraft_server"], capture_output=True, text=True)

print(result)
print()
print(f"{status}")
print()
print(status.players.online)

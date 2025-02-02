from mcstatus import JavaServer
import os

def return_status():
    server = JavaServer(os.getenv("MYIP"), 25565)
    status = server.status()

    print(status.players)

return_status()

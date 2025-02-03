from mcstatus import JavaServer
import os

def return_status():
    try:
        server = JavaServer(os.getenv("MYIP"), 25565)
        status = server.status()

        if status.players.sample == None:
            return "Empty"

        mylist = []
        for player in status.players.sample:
            #This actually prints player names
            mylist.append(player.name)

        return mylist
    except Exception as e:
        return -1

print(return_status())

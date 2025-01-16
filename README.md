Each of these should run as a cronjob. The bot starts when your server starts so on reboot. The status checker runs every minute. 

Create a .env file in this directory with the two variables below
1) DISCORDMCBOT
2) MYIP

The first variable is your discord bot token so that the bot can run
The second variable is for your ip address so the status checker can check your minecraft server

After your bot is added to your discord server your friends can use /startserver to start your server. If it's already online it tells you. If no one is on the server for 5 minutes during a status check then the server is shutdown to save resources.

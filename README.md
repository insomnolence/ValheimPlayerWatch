# Valheim Player Watch

This script works with the [Valheim Discord Bot](https://gitub.com/insomnolence/ValheimDiscordBot) written in Python to be run on Windows. In order for the "players" command to work, the console output needed to be searched peridically for user log in events. However, this posed a couple of problems. 

- The output was on the console only. Best guess is probably due to the fact of the amount of logging and the lack of logging facilities to rotate logs if the server has been running for a long time. 

- Getting the console logging to be available to an outside Python script ( and on Windows ) seemed a difficult task involving using some Windows internals. Again, the main scope of these scripts were to give the ability to let the batch files that run/maintain the server be run manually on the local server without having to use the scripts.

Given the above issues, the option used was to sniff packets on the Valheim Server Port and hope to try and get the Steam Id of the connecting player that way. Once that was accomplished, an easy check using the Steam API can find the user name and this information is then kept in a file. The IP address used for the connection is saved with the user name in memory so that when the player logs out, we can swtich the player's status in a file on the system. 

That file ( player.json ) is then used by the Valheim Discord Bot to determine who is online. For the players command to work, both scripts need to be run on the dedicated server.

## Third Party Libraries

The following third party libraries were needed to be installed for this script to work. They should be easily installed by using the pip install command.

* requests
* scapy

** IMPORTANT NOTE: ** Scapy is used to sniff the packets heading to port 2456 ( default port ) on the Valheim Server. In order for Scapy to be usable on Windows, another piece of software needs to be installed. It's a packet capture library for windows made by the folks at [nmap.org](https://nmap.org). You will need to insall [Npcap](https://namp.org/npcap/) in order to use the Scapy Python library. You can find more information on Scapy [here](https://scapy.readthedocs.io/en/latest/installation.html#overview)

## Script Config

It is suggested that this script is placed where your Valheim Server install is. However, it can be placed anywhere as long as the config variables are properly defined. The first variable ( IFACE ), is suggested to be left as 'None' unless you are familiar with how the interfaces are named on the Windows machine.

* IFACE = None # ( Or the interface name you want to sniff packets on r'Name of network connection' )
* PRIVATE_IP = r'The IP the Valheim Server runs on'
* STEAM_API_KEY = r'Your Steam API key'
* PLAYER_FILE_LOC = r'D:\LOCATION OF\VALHEIM SERVER\players.json'

# players.json file

This is just a simple json file that holds user name and status. The file is opened and written by both the Valheim Player Watch and Valheim Discord Bot to read/write information about players. Example of the file contents:

{"User 1": "No", "User 2": "Yes", "User 3": "Yes", "User 4": "No"}

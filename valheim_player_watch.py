import json
import os
import re

from requests import get
from scapy.all import *

#IFACE = r'YOUR NETWORK INTERFACE TO SNIFF ON'
IFACE = None # None for all interfaces
PRIVATE_IP = r'PRIVATE IP SERVER IS ON'
STEAM_API_KEY = r'YOUR STEAM API KEY'
PLAYER_FILE_LOC = r'D:\LOCATION OF\VALHEIM SERVER\players.json'
HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

steamid_match = re.compile(r'steamid:([0-9]+)')
player_left_match = re.compile(r'Application closed connection')

players = {}

def sniff_packets(iface=None):

    filter_packets = r'src not {} and port 2456'.format(PRIVATE_IP)

    if iface:
        sniff(filter=filter_packets, prn=process_packet, iface=iface, store=False)
    else:
        sniff(filter=filter_packets, prn=process_packet, store=False)


def get_user(user_id):

    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}'.format(STEAM_API_KEY, user_id)
    
    try: 
        response = get(url, headers=HEADERS)
        raw_data = str(response.content, encoding="utf8")
    except:
        print("Something Wrong! Connection Lost\n")
        return ""
    else:
        if response.status_code == 200:
            dict_data = json.loads(raw_data)
            try:
                user_name = dict_data['response']['players'][0]['personaname']
                return user_name
            except:
                print("The user id was invalid?")
                return
        
        else:
            print("Check connction. Status code is {}\n".format(response.status_code))
            return ""

def process_packet(packet):

    data = packet.load
    if data is None:
        return

    data_string = str(data)

    steam_id = steamid_match.search(data_string)
 
    if steam_id:
        ip = packet[IP].src
        user_name = get_user(steam_id[1])
        if user_name is not None:
            print('User {} has logged on'.format(user_name))
            players[ip] = user_name
            update_file(user_name, 'Yes')

        return

    player_left = player_left_match.search(data_string)

    if player_left:
        ip = packet[IP].src
        if ip in players.keys():
            user = players[ip]
            print('Player {} has left'.format(user))
            players.pop(ip, None)
            update_file(user, 'No')

def update_file(user_name, is_online):

    player_list = {}
    if os.path.exists(PLAYER_FILE_LOC):
        with open(PLAYER_FILE_LOC) as json_file:
            player_list = json.load(json_file)

    player_list[user_name] = is_online

    with open(PLAYER_FILE_LOC, 'w') as outfile:
        json.dump(player_list, outfile)


if __name__ == "__main__":

    sniff_packets(IFACE)



import requests
from collections import Counter

API_KEY = "RGAPI-e5e8bf82-fe53-4ac3-9e71-74d250430dab"  # Remplace par ta clé Riot valide
HEADERS = {"X-Riot-Token": API_KEY}

def get_puuid(game_name, tag_line):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    res = requests.get(url, headers=HEADERS)
    return res.json()["puuid"] if res.status_code == 200 else None

def get_match_ids(puuid, count=30):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&queue=420"
    res = requests.get(url, headers=HEADERS)
    return res.json() if res.status_code == 200 else []

def get_match_data(match_id):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    res = requests.get(url, headers=HEADERS)
    return res.json() if res.status_code == 200 else None

def get_player_data_for_1_game(match_data,puuid):
    find_player=False
    j=0
    while not find_player :
        if match_data['info']['participants'][j].get('puuid')==puuid:
            findPlayer=True
            break
        j+=1
    return match_data['info']['participants'][j] 

#Name = "Rambel"
#Tag = "EUW"

#puuid = get_puuid(Name,Tag)
 #print(puuid)

#match_ids = get_match_ids(puuid,1)

#print("Match id")
#print(match_ids)

#print(get_match_data(match_ids[0]))
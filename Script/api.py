import requests
from collections import Counter

API_KEY = "RGAPI-1f8fa467-0d81-47bb-8417-13acba3673eb"  # Remplace par ta clé Riot valide
HEADERS = {"X-Riot-Token": API_KEY}
REGION_ROUTING = "euw1"

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

def get_rank_info(puuid):
    # Étape 1 : récupérer le summonerId (pas possible directement avec puuid pour les ranks)
    url_summoner = f"https://{REGION_ROUTING}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    headers = {"X-Riot-Token": API_KEY}
    response = requests.get(url_summoner, headers=headers)

    if response.status_code != 200:
        print(f"Erreur API pour summoner : {response.status_code}")
        return None

    summoner = response.json()
    summoner_id = summoner["id"]

    # Étape 2 : récupérer les infos de ligue via summonerId
    url_rank = f"https://{REGION_ROUTING}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    response = requests.get(url_rank, headers=headers)

    if response.status_code != 200:
        print(f"Erreur API pour rank : {response.status_code}")
        return None

    data = response.json()
    
    # On cherche la file soloQ (RANKED_SOLO_5x5)
    for queue in data:
        if queue["queueType"] == "RANKED_SOLO_5x5":
            return {
                "tier": queue["tier"],               # ex: GOLD
                "rank": queue["rank"],               # ex: II
                "lp": queue["leaguePoints"],         # ex: 64
                "wins": queue["wins"],
                "losses": queue["losses"]
            }

    return {"tier": "UNRANKED", "rank": "", "lp": 0, "wins": 0, "losses": 0}
Name = "Rambel"
Tag = "EUW"

puuid = get_puuid(Name,Tag)
 #print(puuid)

#match_ids = get_match_ids(puuid,1)

#print("Match id")
#print(match_ids)

#print(get_match_data(match_ids[0]))
print(get_rank_info(puuid))
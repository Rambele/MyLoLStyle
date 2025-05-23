import requests
import time
import json

API_KEY = "RGAPI-9aec9d31-ad93-4edd-b3b8-43fa17d8af06"
REGION = "euw1"
MATCH_REGION = "europe"
HEADERS = {"X-Riot-Token": API_KEY}
LOG_FILE = "smartstat_pyke_log.json"


def get_diamond_players():
    url = f"https://{REGION}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/SILVER/I?page=1"
    res = requests.get(url, headers=HEADERS)
    try:
        data = res.json()
        if isinstance(data, list):
            return data
        else:
            print("⚠️ Problème avec la réponse:", data)
            return []
    except Exception as e:
        print("❌ JSON parsing failed", e)
        return []


def get_summoner_by_name(summoner_name):
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    res = requests.get(url, headers=HEADERS)
    return res.json()


def get_match_ids(puuid):
    url = f"https://{MATCH_REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=30"
    res = requests.get(url, headers=HEADERS)
    return res.json()


def get_match_data(match_id):
    url = f"https://{MATCH_REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    res = requests.get(url, headers=HEADERS)
    return res.json()


def log_progress(log_data):
    with open(LOG_FILE, "w") as f:
        json.dump(log_data, f, indent=2)


def load_logged_summoners():
    try:
        with open(LOG_FILE, "r") as f:
            return json.load(f)
    except:
        return {"processed": []}


def analyze_pyke_winrate():
    log = load_logged_summoners()
    processed_names = set(log["processed"])

    players = get_diamond_players()
    total_games = 0
    pyke_wins = 0

    for p in players:
        if "summonerName" not in p:
            continue

        name = p["summonerName"]
        if name in processed_names:
            continue

        try:
            summoner = get_summoner_by_name(name)
            if summoner.get("summonerLevel", 0) < 200:
                continue
        except:
            continue

        puuid = summoner["puuid"]
        try:
            match_ids = get_match_ids(puuid)
        except:
            continue

        for match_id in match_ids:
            try:
                match = get_match_data(match_id)
                for participant in match["info"]["participants"]:
                    if participant["puuid"] == puuid and participant["championName"] == "Pyke":
                        total_games += 1
                        if participant["win"]:
                            pyke_wins += 1
            except:
                continue

            time.sleep(1)  # pour respecter les quotas

        print(f"✅ Traité: {name} — Total Pyke games: {total_games}")
        processed_names.add(name)
        log["processed"].append(name)
        log_progress(log)

        time.sleep(1)

        if total_games >= 50:  # Limite temporaire pour test
            break

    if total_games == 0:
        print("Aucune partie trouvée avec Pyke.")
    else:
        winrate = (pyke_wins / total_games) * 100
        print(f"\n📊 Pyke Win Rate : {winrate:.2f}% ({pyke_wins}/{total_games})")


if __name__ == "__main__":
    analyze_pyke_winrate()

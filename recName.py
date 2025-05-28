import requests
import time

API_KEY = "RGAPI-5052a455-8ae5-4a6b-a82b-46ec51c87a2b"
HEADERS = {"X-Riot-Token": API_KEY}
REGION = "euw1"
TIER_LIST = ["GOLD", "PLATINUM", "EMERALD", "DIAMOND"]
DIVISION = "I"
PAGE = 2
JOUEURS_PAR_DIV = 10
SORTIE = "joueurs"

def get_puuid_from_summoner_id(summoner_id):
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json().get("puuid")
    return None

def get_tagline_from_puuid(puuid):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        data = r.json()
        return data.get("gameName"), data.get("tagLine")
    return None, None

with open(SORTIE, "a", encoding="utf-8") as f:
    for tier in TIER_LIST:
        print(f"🔍 Lecture : {tier} {DIVISION} - Page {PAGE}")
        url = f"https://{REGION}.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{DIVISION}?page={PAGE}"
        r = requests.get(url, headers=HEADERS)

        if r.status_code != 200:
            print(f"⚠️ Erreur {r.status_code} pour {tier} {DIVISION} : {r.text}")
            continue

        try:
            data = r.json()
            joueurs = data[:JOUEURS_PAR_DIV]
            for joueur in joueurs:
                summoner_id = joueur.get("summonerId")
                if not summoner_id:
                    print("⚠️ Pas de summonerId, joueur ignoré.")
                    continue

                puuid = get_puuid_from_summoner_id(summoner_id)
                if not puuid:
                    print(f"⚠️ PUUID introuvable pour summonerId: {summoner_id}")
                    continue

                name, tag = get_tagline_from_puuid(puuid)
                if name and tag:
                    ligne = f"{name},{tag}\n"
                    f.write(ligne)
                    print(f"✅ Ajouté : {ligne.strip()}")
                else:
                    print(f"⚠️ Nom/tag introuvable pour puuid: {puuid}")

                time.sleep(1.5)  # pour éviter les limites API

        except Exception as e:
            print(f"❌ Erreur JSON ou réseau sur {tier} {DIVISION} : {e}")

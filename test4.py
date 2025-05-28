import requests
import csv
import time
from collections import Counter, defaultdict

API_KEY = "RGAPI-7cd0646f-dba4-4993-a7e7-9f0209ddb2dd"  # Remplace par ta clé valide
HEADERS = {"X-Riot-Token": API_KEY}

# ---- Fonctions avec délais ----
def safe_request(url):
    delay = 1
    max_retries = 5
    for attempt in range(max_retries):
        res = requests.get(url, headers=HEADERS)
        if res.status_code == 200:
            time.sleep(1.2)  # délai de base entre les requêtes réussies
            return res
        elif res.status_code == 429:
            retry_after = int(res.headers.get("Retry-After", delay))
            print(f"⚠️ Rate limit atteint. Pause {retry_after}s...")
            time.sleep(retry_after)
        else:
            print(f"⚠️ Erreur {res.status_code} sur {url}")
            return res
        delay *= 2
    print("❌ Trop de tentatives échouées.")
    return None

def percent(val, total):
    return round(val / total, 3) if total else 0

def get_puuid(game_name, tag_line):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    res = safe_request(url)
    return res.json()["puuid"] if res and res.status_code == 200 else None

def get_summoner_id(puuid):
    url = f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    res = safe_request(url)
    return res.json()["id"] if res and res.status_code == 200 else None

def get_ranked_stats(puuid):
    summoner_id = get_summoner_id(puuid)
    if not summoner_id:
        return "Unranked", 0
    url = f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    res = safe_request(url)
    if not res or res.status_code != 200:
        return "Unranked", 0
    soloq = next((entry for entry in res.json() if entry["queueType"] == "RANKED_SOLO_5x5"), None)
    if not soloq:
        return "Unranked", 0
    return f'{soloq["tier"].capitalize()} {soloq["rank"]}', soloq["leaguePoints"]

def get_match_ids(puuid, count=30):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&queue=420"
    res = safe_request(url)
    return res.json() if res and res.status_code == 200 else []

def get_match_info(match_id):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    res = safe_request(url)
    return res.json() if res and res.status_code == 200 else None

# ---- Analyse de rôle ----
def detect_main_role(puuid, match_ids):
    role_counter = Counter()
    for match_id in match_ids:
        match = get_match_info(match_id)
        if not match:
            continue
        participant = next((p for p in match["info"]["participants"] if p["puuid"] == puuid), None)
        if participant:
            role = participant.get("teamPosition", "NONE")
            if role and role != "NONE":
                role_counter[role] += 1
    return role_counter.most_common(1)[0][0] if role_counter else "UNKNOWN"

# ---- Analyse d’un joueur ----
def analyze_player(name, tag):
    puuid = get_puuid(name, tag)
    if not puuid:
        print(f"PUUID introuvable pour {name}#{tag}")
        return None

    match_ids = get_match_ids(puuid)
    if not match_ids:
        print(f"Aucune partie trouvée pour {name}#{tag}")
        return None

    role = detect_main_role(puuid, match_ids)
    rank, lp = get_ranked_stats(puuid)

    stats_acc = defaultdict(float)
    wins = 0
    count = 0

    for match_id in match_ids:
        match = get_match_info(match_id)
        if not match:
            continue

        player = next((p for p in match["info"]["participants"] if p["puuid"] == puuid), None)
        if not player or player["teamPosition"] != role:
            continue

        team = [p for p in match["info"]["participants"] if p["teamId"] == player["teamId"]]
        n = len(team)

        def diff(val, team_vals):
            non_zero = [x for x in team_vals if x > 0]
            if not non_zero:
                return 0
            team_avg = sum(non_zero) / len(non_zero)
            return round(val / team_avg - 1, 3)

        stats_acc["dmg%_diff"] += diff(player["totalDamageDealtToChampions"], [p["totalDamageDealtToChampions"] for p in team])
        stats_acc["tank%_diff"] += diff(player["totalDamageTaken"], [p["totalDamageTaken"] for p in team])
        stats_acc["kp%_diff"] += diff(player["kills"] + player["assists"], [p["kills"] + p["assists"] for p in team])
        stats_acc["cs%_diff"] += diff(player["totalMinionsKilled"] + player["neutralMinionsKilled"], [p["totalMinionsKilled"] + p["neutralMinionsKilled"] for p in team])
        stats_acc["wardsPlaced%_diff"] += diff(player["wardsPlaced"], [p["wardsPlaced"] for p in team])
        stats_acc["wardsKilled%_diff"] += diff(player["wardsKilled"], [p["wardsKilled"] for p in team])
        stats_acc["detectors%_diff"] += diff(player["detectorWardsPlaced"], [p["detectorWardsPlaced"] for p in team])
        stats_acc["gold%_diff"] += diff(player["goldEarned"], [p["goldEarned"] for p in team])
        stats_acc["heal%_diff"] += diff(player.get("totalHealsOnTeammates", 0), [p.get("totalHealsOnTeammates", 0) for p in team])
        stats_acc["shield%_diff"] += diff(player.get("totalDamageShieldedOnTeammates", 0), [p.get("totalDamageShieldedOnTeammates", 0) for p in team])
        stats_acc["ccTime%_diff"] += diff(player["timeCCingOthers"], [p["timeCCingOthers"] for p in team])
        stats_acc["kill%_diff"] += diff(player["kills"], [p["kills"] for p in team])
        stats_acc["death%_diff"] += diff(player["deaths"], [p["deaths"] for p in team])
        stats_acc["assist%_diff"] += diff(player["assists"], [p["assists"] for p in team])

        wins += int(player["win"])
        count += 1

    if count == 0:
        print(f"Aucune partie analysable pour {name}")
        return None

    averaged_stats = {k: round(v / count, 3) for k, v in stats_acc.items()}
    total_diff = round(sum(averaged_stats.values()), 3)

    return {
        "name": f"{name}#{tag}",
        "role": role,
        "rank": rank,
        "lp": lp,
        "games": count,
        "winrate": round(wins / count, 3),
        **averaged_stats,
        "total_stats_diff": total_diff,
    }

# ---- Export vers CSV ----
def export_to_csv(data, filename="players_stats.csv"):
    if not data:
        print("Aucune donnée à exporter.")
        return
    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"✅ Données exportées dans {filename}")

# ---- Lecture des noms ----
def lire_joueurs_depuis_fichier(fichier_path):
    joueurs = []
    with open(fichier_path, 'r', encoding='utf-8') as f:
        for ligne in f:
            parts = ligne.strip().split(',')
            if len(parts) == 2:
                nom, tag = parts
                joueurs.append((nom.strip(), tag.strip()))
    return joueurs

# ---- Main ----
def main():
    joueurs = lire_joueurs_depuis_fichier("joueur")

    resultats = []
    for name, tag in joueurs:
        print(f"🔍 Analyse de {name}#{tag}...")
        res = analyze_player(name, tag)
        if res:
            resultats.append(res)

    export_to_csv(resultats)

if __name__ == "__main__":
    main()

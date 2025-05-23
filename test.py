import requests
from collections import Counter

API_KEY = "RGAPI-1f093953-fc54-49a9-b826-b91e5d79b7bb"
GAME_NAME = "Unna78"
TAG_LINE = "EUW"
HEADERS = {"X-Riot-Token": API_KEY}

def average_stats(stat_list):
    if not stat_list:
        return {}

    total = {}
    count = len(stat_list)

    for game in stat_list:
        for key, value in game.items():
            if isinstance(value, (int, float)):  # Ne garde que les nombres
                total[key] = total.get(key, 0) + value

    return {key: round(val / count, 3) for key, val in total.items()}

def detect_archetype(avg):
    if avg.get("shield%", 0) + avg.get("heal%", 0) > 1.2 and avg.get("ccTime%", 0) > 0.25:
        return "Support Pillar"
    elif avg.get("kp%", 0) > 0.65 and (avg.get("detectors%", 0) + avg.get("wardsKilled%", 0)) > 0.6:
        return "Roamer / Playmaker"
    elif avg.get("tank%", 0) > 0.25 and avg.get("detectors%", 0) > 0.4:
        return "Tank Utility"
    elif avg.get("dmg%", 0) > 0.25 and avg.get("kp%", 0) > 0.6 and avg.get("cs%", 0) > 0.2:
        return "Carry Jungler / ADC"
    elif avg.get("dmg%", 0) < 0.15 and avg.get("kp%", 0) < 0.5 and avg.get("detectors%", 0) < 0.3:
        return "Ghost / Low impact"
    else:
        return "Joueur équilibré / mixte"

def generate_profile(avg):
    def tag(value, low, mid, high):
        if value < low:
            return "faible"
        elif value < mid:
            return "moyen"
        elif value < high:
            return "élevé"
        else:
            return "très élevé"

    return {
        "vision": tag(avg.get("wardsPlaced%", 0) + avg.get("detectors%", 0), 0.3, 0.5, 0.7),
        "protection": tag(avg.get("shield%", 0) + avg.get("heal%", 0), 0.4, 0.8, 1.2),
        "impact_teamfight": tag(avg.get("kp%", 0), 0.4, 0.6, 0.75),
        "contrôle": tag(avg.get("ccTime%", 0), 0.1, 0.25, 0.4),
        "agressivité": tag(avg.get("dmg%", 0), 0.15, 0.25, 0.35)
    }



def get_puuid(game_name, tag_line):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    res = requests.get(url, headers=HEADERS)
    return res.json()["puuid"] if res.status_code == 200 else None

def get_match_ids(puuid, count=50):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&queue=420"
    res = requests.get(url, headers=HEADERS)
    return res.json() if res.status_code == 200 else []

def get_match_info(match_id):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    res = requests.get(url, headers=HEADERS)
    return res.json() if res.status_code == 200 else None

def analyze_player(puuid):
    match_ids = get_match_ids(puuid)
    roles = []
    match_stats = []

    for match_id in match_ids:
        match = get_match_info(match_id)
        if not match:
            continue
        for p in match["info"]["participants"]:
            if p["puuid"] == puuid:
                roles.append(p["teamPosition"])
                match_stats.append((match, p))
                break

    dominant_role = Counter(roles).most_common(1)[0][0]
    filtered = [(m, p) for (m, p) in match_stats if p["teamPosition"] == dominant_role]
    result = []

    for match, player_data in filtered:
        team = [p for p in match["info"]["participants"] if p["teamId"] == player_data["teamId"]]

        def percent(val, total):
            return round(val / total, 3) if total else 0

        total = {
            "damage": sum(p["totalDamageDealtToChampions"] for p in team),
            "taken": sum(p["totalDamageTaken"] for p in team),
            "kills": sum(p["kills"] for p in team),
            "cs": sum(p["totalMinionsKilled"] + p["neutralMinionsKilled"] for p in team),
            "wardsPlaced": sum(p["wardsPlaced"] for p in team),
            "wardsKilled": sum(p["wardsKilled"] for p in team),
            "detectors": sum(p["detectorWardsPlaced"] for p in team),
            "shields": sum(p.get("totalDamageShieldedOnTeammates", 0) for p in team),
            "heals": sum(p.get("totalHealsOnTeammates", 0) for p in team),
            "cc": sum(p["timeCCingOthers"] for p in team)

        }

        player_stats = {
            "champion": player_data["championName"],
            "dmg%": percent(player_data["totalDamageDealtToChampions"], total["damage"]),
            "tank%": percent(player_data["totalDamageTaken"], total["taken"]),
            "kp%": percent(player_data["kills"] + player_data["assists"], total["kills"]),
            "cs%": percent(player_data["totalMinionsKilled"] + player_data["neutralMinionsKilled"], total["cs"]),
            "wardsPlaced%": percent(player_data["wardsPlaced"], total["wardsPlaced"]),
            "wardsKilled%": percent(player_data["wardsKilled"], total["wardsKilled"]),
            "detectors%": percent(player_data["detectorWardsPlaced"], total["detectors"]),
            "shield%": percent(player_data.get("totalDamageShieldedOnTeammates", 0), total["shields"]),
            "heal%": percent(player_data.get("totalHealsOnTeammates", 0), total["heals"]),
            "ccTime%": percent(player_data["timeCCingOthers"], total["cc"])
            
        }

        result.append(player_stats)

    return dominant_role, result

if __name__ == "__main__":
    puuid = get_puuid(GAME_NAME, TAG_LINE)
    if puuid:
        role, stats = analyze_player(puuid)
        print(f"Rôle dominant : {role}\n")
        avg = average_stats(stats)
        print(f"Rôle dominant : {role}")
        print(f"\n📈 Moyenne sur {len(stats)} games :")
        for k, v in avg.items():
            print(f"{k}: {v}")
        archetype = detect_archetype(avg)
        print(f"\n🧠 Archétype détecté : {archetype}")
        profile = generate_profile(avg)
        print("\n📊 Profil multidimensionnel :")
        for k, v in profile.items():
            print(f"- {k.capitalize()} : {v}")
    else:
        print("PUUID non trouvé.")

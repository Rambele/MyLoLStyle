import requests
from collections import Counter

API_KEY = "RGAPI-7cd0646f-dba4-4993-a7e7-9f0209ddb2dd"  # Remplace par ta clé Riot valide
HEADERS = {"X-Riot-Token": API_KEY}

def detect_main_role(puuid, match_ids):
    role_counter = Counter()
    for match_id in match_ids:
        match = get_match_info(match_id)
        if not match:
            continue
        participant = next((p for p in match["info"]["participants"] if p["puuid"] == puuid), None)
        if participant:
            role = participant["teamPosition"]
            if role:
                role_counter[role] += 1
    return role_counter.most_common(1)[0][0] if role_counter else None

def get_puuid(game_name, tag_line):
    url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
    res = requests.get(url, headers=HEADERS)
    return res.json()["puuid"] if res.status_code == 200 else None

def get_match_ids(puuid, count=30):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&queue=420"
    res = requests.get(url, headers=HEADERS)
    return res.json() if res.status_code == 200 else []

def get_match_info(match_id):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    res = requests.get(url, headers=HEADERS)
    return res.json() if res.status_code == 200 else None

def percent(val, total):
    return round(val / total, 3) if total else 0

def analyze_player(puuid):
    match_ids = get_match_ids(puuid)
    main_role = detect_main_role(puuid, match_ids)
    print(f"Rôle dominant détecté : {main_role}")
    stats = []

    for match_id in match_ids:
        match = get_match_info(match_id)
        if not match:
            continue

        participants = match["info"]["participants"]
        player_data = next((p for p in participants if p["puuid"] == puuid), None)
        if not player_data:
            continue

        role = player_data["teamPosition"]
        if role != main_role:
            continue

        team_id = player_data["teamId"]
        enemy_team = [p for p in participants if p["teamId"] != team_id]
        same_role_enemy = next((p for p in enemy_team if p["teamPosition"] == role), None)
        team = [p for p in participants if p["teamId"] == team_id]

        total = {
            "damage": sum(p["totalDamageDealtToChampions"] for p in team),
            "taken": sum(p["totalDamageTaken"] for p in team),
            "kills": sum(p["kills"] for p in team),
            "deaths": sum(p["deaths"] for p in team),
            "assists": sum(p["assists"] for p in team),
            "gold": sum(p["goldEarned"] for p in team),
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
            "win": player_data["win"],
            "dmg%": percent(player_data["totalDamageDealtToChampions"], total["damage"]),
            "tank%": percent(player_data["totalDamageTaken"], total["taken"]),
            "kp%": percent(player_data["kills"] + player_data["assists"], total["kills"]),
            "cs%": percent(player_data["totalMinionsKilled"] + player_data["neutralMinionsKilled"], total["cs"]),
            "wardsPlaced%": percent(player_data["wardsPlaced"], total["wardsPlaced"]),
            "wardsKilled%": percent(player_data["wardsKilled"], total["wardsKilled"]),
            "detectors%": percent(player_data["detectorWardsPlaced"], total["detectors"]),
            "shield%": percent(player_data.get("totalDamageShieldedOnTeammates", 0), total["shields"]),
            "heal%": percent(player_data.get("totalHealsOnTeammates", 0), total["heals"]),
            "ccTime%": percent(player_data["timeCCingOthers"], total["cc"]),
            "kill%": percent(player_data["kills"], total["kills"]),
            "death%": percent(player_data["deaths"], total["deaths"]),
            "assist%": percent(player_data["assists"], total["assists"]),
            "gold%": percent(player_data["goldEarned"], total["gold"])
        }

        if same_role_enemy:
            enemy_stats = {
                "dmg%_enemy": percent(same_role_enemy["totalDamageDealtToChampions"],
                                      sum(p["totalDamageDealtToChampions"] for p in enemy_team)),
                "tank%_enemy": percent(same_role_enemy["totalDamageTaken"],
                                       sum(p["totalDamageTaken"] for p in enemy_team)),
                "kp%_enemy": percent(same_role_enemy["kills"] + same_role_enemy["assists"],
                                     sum(p["kills"] for p in enemy_team)),
                "cs%_enemy": percent(same_role_enemy["totalMinionsKilled"] + same_role_enemy["neutralMinionsKilled"],
                                     sum(p["totalMinionsKilled"] + p["neutralMinionsKilled"] for p in enemy_team)),
                "wardsPlaced%_enemy": percent(same_role_enemy["wardsPlaced"],
                                              sum(p["wardsPlaced"] for p in enemy_team)),
                "wardsKilled%_enemy": percent(same_role_enemy["wardsKilled"],
                                              sum(p["wardsKilled"] for p in enemy_team)),
                "detectors%_enemy": percent(same_role_enemy["detectorWardsPlaced"],
                                            sum(p["detectorWardsPlaced"] for p in enemy_team)),
                "shield%_enemy": percent(same_role_enemy.get("totalDamageShieldedOnTeammates", 0),
                                         sum(p.get("totalDamageShieldedOnTeammates", 0) for p in enemy_team)),
                "heal%_enemy": percent(same_role_enemy.get("totalHealsOnTeammates", 0),
                                       sum(p.get("totalHealsOnTeammates", 0) for p in enemy_team)),
                "ccTime%_enemy": percent(same_role_enemy["timeCCingOthers"],
                                         sum(p["timeCCingOthers"] for p in enemy_team)),
                "kill%_enemy": percent(same_role_enemy["kills"], sum(p["kills"] for p in enemy_team)),
                "death%_enemy": percent(same_role_enemy["deaths"], sum(p["deaths"] for p in enemy_team)),
                "assist%_enemy": percent(same_role_enemy["assists"], sum(p["assists"] for p in enemy_team)),
                "gold%_enemy": percent(same_role_enemy["goldEarned"], sum(p["goldEarned"] for p in enemy_team))
            }
        else:
            enemy_stats = {k + "_enemy": None for k in list(player_stats.keys())[2:]}

        player_stats["vs"] = same_role_enemy["championName"] if same_role_enemy else "N/A"

        diff_stats = {}
        for key in player_stats:
            if key in ["champion", "win", "vs"]:
                continue
            enemy_key = key + "_enemy"
            player_val = player_stats.get(key)
            enemy_val = enemy_stats.get(enemy_key)
            diff_stats[key + "_diff"] = round(player_val - enemy_val, 3) if player_val is not None and enemy_val is not None else None

        stats.append({**player_stats, **enemy_stats, **diff_stats})

    return stats

def main():
    name = "Rambel"
    tag = "EUW"
    print(f"\nAnalyse de {name}#{tag}...")

    puuid = get_puuid(name, tag)
    if not puuid:
        print("PUUID introuvable.")
        return

    stats = analyze_player(puuid)

    for i, s in enumerate(stats, 1):
        print(f"\nMatch {i} - {s['champion']} vs {s['vs']} - {'Victoire' if s['win'] else 'Défaite'}")
        for key in s:
            if key.endswith("_diff"):
                base = key.replace("_diff", "")
                joueur = s.get(base)
                ennemi = s.get(base + "_enemy")
                diff = s.get(key)
                if joueur is not None and ennemi is not None:
                    print(f"  {base:<14s}: {joueur:<5} | ennemi: {ennemi:<5} | diff: {diff:+}")
    
    print("\n=== Moyenne des écarts (player - ennemi) sur les matchs analysés ===")
    diff_totaux = {}
    n = 0
    for s in stats:
        for key in s:
            if key.endswith("_diff") and s[key] is not None:
                diff_totaux[key] = diff_totaux.get(key, 0) + s[key]
        n += 1
    for key, total in diff_totaux.items():
        print(f"{key:<14s}: {round(total / n, 3):+}")
    
        # Calcul du score global filtré 
    excluded_keys = [] #'cs%_diff', 'assist%_diff' , 'death%_diff'
    custom_score = sum(
        total / n for key, total in diff_totaux.items() if key not in excluded_keys
    )
    print(f"\n🔹 Score Global (filtré) : {round(custom_score, 3):+}")


if __name__ == "__main__":
    main()

import requests
from collections import Counter

API_KEY = "RGAPI-059be12d-57cf-4c88-93f7-d4a832be0f27"  # Remplace par ta clé Riot valide
HEADERS = {"X-Riot-Token": API_KEY}

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
        team_id = player_data["teamId"]
        enemy_team = [p for p in participants if p["teamId"] != team_id]
        same_role_enemy = next((p for p in enemy_team if p["teamPosition"] == role), None)

        # équipe du joueur
        team = [p for p in participants if p["teamId"] == team_id]
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
            "ccTime%": percent(player_data["timeCCingOthers"], total["cc"])
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
                                         sum(p["timeCCingOthers"] for p in enemy_team))
            }
        else:
            enemy_stats = {k + "_enemy": None for k in list(player_stats.keys())[2:]}

        stats.append({**player_stats, **enemy_stats})

    return stats

def main():

    name = "Rambel"
    tag = "EUW"
    print(f"\nAnalyse de {name}#{tag}...")

    puuid = get_puuid(name, tag)
    if not puuid:
        print("PUUID introuvable.")

    stats = analyze_player(puuid)

    for i, s in enumerate(stats, 1):
        print(f"\nMatch {i} - {s['champion']} - {'Victoire' if s['win'] else 'Défaite'}")
        for key in s:
            if key not in ["champion", "win"]:
                val = s[key]
                if "_enemy" in key:
                    base_key = key.replace("_enemy", "")
                    print(f"  {base_key:14s} ennemi: {val}")
                elif f"{key}_enemy" in s:
                    print(f"  {key:14s}: {val}", end="")
                else:
                    print(f"  {key:14s}: {val}")

if __name__ == "__main__":
    main()

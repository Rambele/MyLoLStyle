from api import RiotAPI
from processor import ImpactProcessor
from impact_stats_config import IMPACT_STATS

def flatten_player_data(player_data):
    clean_data = {}

    for key, value in player_data.items():
        if key == "challenges":
            # On fusionne les champs challenges au même niveau
            for c_key, c_value in value.items():
                clean_data[c_key] = c_value
        elif isinstance(value, (int, float, str, bool)) or value is None:
            clean_data[key] = value
        # On ignore les objets trop complexes comme les listes de builds ou dicts imbriqués

    return clean_data

def print_player_stats_from_keys(match_data, puuid, stat_keys):
    player = next((p for p in match_data["info"]["participants"] if p["puuid"] == puuid), None)
    if not player:
        print("Joueur introuvable.")
        return

    for key in stat_keys:
        # Cherche d'abord dans les clés racines, sinon dans 'challenges'
        value = player.get(key, player.get("challenges", {}).get(key, "Non disponible"))
        print(f"{key} : {value}")


api = RiotAPI(api_key="RGAPI-45c64edf-b5f7-4dc4-a67b-4058f0150e5e")
puuid = api.get_puuid("Rambel", "EUW")
match_ids = api.get_match_ids(puuid, count=5,queue=420)
i=0
for match_id in match_ids :
    match_data = api.get_match_data(match_ids[i])
    process = ImpactProcessor(match_data)

    impact_player = process.compare_vs_opponent(puuid,IMPACT_STATS)
    print(impact_player)
    print("===")
    i=i+1
    print_player_stats_from_keys(match_data,puuid,IMPACT_STATS)
    print("=========================================")


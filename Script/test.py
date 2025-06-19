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



api = RiotAPI(api_key="RGAPI-5ba2ef4e-7255-4996-8c35-f0e4bd1c7666")
puuid = api.get_puuid("Rambel", "EUW")
match_ids = api.get_match_ids(puuid, count=1,queue=420)
match_data = api.get_match_data(match_ids[0])
process = ImpactProcessor(match_data)

impact_player = process.calculate_impact_vs_team(puuid,IMPACT_STATS)
print(impact_player)
print("=========================================")
impact_player = process.compare_vs_opponent(puuid,IMPACT_STATS)
print(impact_player)
print(next(p for p in match_data["info"]["participants"] if p["puuid"] == puuid)["championName"])

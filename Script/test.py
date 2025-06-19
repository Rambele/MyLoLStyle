from api import RiotAPI

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



api = RiotAPI(api_key="RGAPI-be3ec282-311c-43ca-8a53-4ae150d114cb")

puuid = api.get_puuid("Rambel", "EUW")
match_ids = api.get_match_ids(puuid, count=1)
match_data = api.get_match_data(match_ids[0])

# Trouver les données du joueur via son puuid
player_data = next((p for p in match_data["info"]["participants"] if p["puuid"] == puuid), None)

player_data = flatten_player_data(player_data)

for key, value in player_data.items():
    print(f"{key}: {value}")
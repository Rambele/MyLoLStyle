import requests
from collections import Counter
import api

def get_opponent_puuid(info, puuid):
    # Récupérer la teamId du joueur ciblé
    target_team = None
    for p in info['info']['participants']:
        if p['puuid'] == puuid:
            target_team = p['teamId']
            target_lane = p['individualPosition']
            break
    # Chercher l'opposant sur la lane (même position, autre team)
    for p in info['info']['participants']:
        if p['teamId'] != target_team and p['individualPosition'] == target_lane:
            return p['puuid']
    return None

def printPlayer(data_player_game):
    summoner_name = data_player_game.get('riotIdGameName', 'Inconnu')
    champion_name = data_player_game.get('championName', 'Inconnu')
    print(f"Joueur : {summoner_name} | Champion : {champion_name}")

def printPlayerStats(data_player) :
    stats_to_show = [
        'damageTakenOnTeamPercentage',
        'kda',
        'immobilizeAndKillWithAlly',
        'killAfterHiddenWithAlly',
        'killParticipation',
        'killsNearEnemyTurret',
        'killsOnOtherLanesEarlyJungleAsLaner',
        'killsUnderOwnTurret',
        'knockEnemyIntoTeamAndKill',
        'multikillsAfterAggressiveFlash',
        'outnumberedKills'
    ]

    challenges = data_player.get('challenges', {})

    print("=== Statistiques spécifiques du joueur ===")
    for stat in stats_to_show:
        value = challenges.get(stat, 'Non disponible')
        print(f"{stat} : {value}")

def get_diff_stats_player(data_player):
    # 'damageTakenOnTeamPercentage', 'kda','immobilizeAndKillWithAlly', 'killAfterHiddenWithAlly',
    #  'killParticipation', 'killsNearEnemyTurret', 'killsOnOtherLanesEarlyJungleAsLaner', 'killsUnderOwnTurret'
    #   'knockEnemyIntoTeamAndKill', 'multikillsAfterAggressiveFlash', 'outnumberedKills'
    #
    return 0

def get_dmg_stats_player(data_player):
    # 
    return 0
def get_vision_stast_player(data_player):
    return 0
def get_utility_stats_player(data_player):
    return 0
def get_ressources_stats_player(data_player):
    return 0
def get_kda_stats_player(data_player):
    return 0
def get_map_pressur_stats_player(data_player):
    return 0

name = "Rambel" 
tag = "EUW"

puuid = api.get_puuid(name,tag)
matchs_id = api.get_match_ids(puuid,2)
match_1_data = api.get_match_data(matchs_id[0])

printPlayer(api.get_player_data_for_1_game(match_1_data,puuid))
printPlayerStats(api.get_player_data_for_1_game(match_1_data,puuid))
print("===================")
printPlayer(api.get_player_data_for_1_game(match_1_data,get_opponent_puuid(match_1_data,puuid)))
printPlayerStats(api.get_player_data_for_1_game(match_1_data,get_opponent_puuid(match_1_data,puuid)))
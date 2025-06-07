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
        'knockEnemyIntoTeamAndKill','immobilizeAndKillWithAlly'
        'multikillsAfterAggressiveFlash',
        'outnumberedKills'
    ]

    challenges = data_player.get('challenges', {})

    print("=== Statistiques spécifiques du joueur ===")
    for stat in stats_to_show:
        value = challenges.get(stat, 'Non disponible')
        print(f"{stat} : {value}")

def printPlayerAttckStats(data_player):
    dmg_to_champs = data_player.get('totalDamageDealtToChampions', 0)
    dmg_to_turrets = data_player.get('damageDealtToTurrets', 0)
    dmg_to_buildings = data_player.get('damageDealtToBuildings', 0)
    dmg_to_objectives = data_player.get('damageDealtToObjectives', 0)
    dmg_self_mitigated = data_player.get('damageSelfMitigated',0)
    total_dmg_taken = data_player.get('totalDamageTaken',0)
    effective_heal_and_shielding=data_player.get('challenges', {}).get('effectiveHealAndShielding')
    enemy_champion_immobilizations=data_player.get('challenges', {}).get('enemyChampionImmobilizations')
    time_ccing_others = data_player.get('timeCCingOthers', 0)
    total_heal = data_player.get('totalHeal', 0)
    total_damage_shielded_on_teammates = data_player.get('totalDamageShieldedOnTeammates', 0)
    total_heals_on_teammates = data_player.get('totalHealsOnTeammates', 0)
    total_time_cc_dealt = data_player.get('totalTimeCCDealt', 0)
    total_units_healed = data_player.get('totalUnitsHealed', 0)
    knock_enemy_into_team_and_kill = data_player.get('knockEnemyIntoTeamAndKill', 0)
    immobilize_and_kill_with_ally = data_player.get('immobilizeAndKillWithAlly', 0)

    visionWardsBoughtInGame = data_player.get('visionWardsBoughtInGame', 0)
    wardsKilled = data_player.get('wardsKilled', 0)
    wardsPlaced = data_player.get('wardsPlaced', 0)
    controlWardsPlaced = data_player.get('challenges', {}).get('controlWardsPlaced')
    wardTakedowns = data_player.get('challenges', {}).get('wardTakedowns')
    wardsGuarded = data_player.get('challenges', {}).get('wardsGuarded')
    detectorWardsPlaced = data_player.get('detectorWardsPlaced', 0)
    enemyVisionPings = data_player.get('enemyVisionPings', 0)
    killAfterHiddenWithAlly = data_player.get('killAfterHiddenWithAlly', 0)
    #autherstats
    kills = data_player.get('kills', 0)
    deaths = data_player.get('deaths', 0)
    assists = data_player.get('assists', 0)
    gameLength = data_player.get('gameLength', 0)
    goldEarned = data_player.get('challenges', {}).get('goldEarned')
    multikillsAfterAggressiveFlash = data_player.get('challenges', {}).get('multikillsAfterAggressiveFlash')
    pickKillWithAlly = data_player.get('challenges', {}).get('pickKillWithAlly')
    saveAllyFromDeath = data_player.get('challenges', {}).get('saveAllyFromDeath')
    skillshotsDodged = data_player.get('challenges', {}).get('skillshotsDodged')
    skillshotsHit = data_player.get('challenges', {}).get('skillshotsHit')
    survivedThreeImmobilizesInFight = data_player.get('challenges', {}).get('survivedThreeImmobilizesInFight')
    tookLargeDamageSurvived = data_player.get('challenges', {}).get('tookLargeDamageSurvived')
    longestTimeSpentLiving = data_player.get('longestTimeSpentLiving', 0)
    totalTimeSpentDead = data_player.get('totalTimeSpentDead', 0)


    print("=== Statistiques spécifiques du joueur ===")
    print("-> Stats de DMG : ")
    print(" Total dmg dealt to champion : ", dmg_to_champs)
    print(" Total dmg dealt to Turets : ", dmg_to_turrets)
    print(" Total dmg dealt to Objective neutre : ", dmg_to_objectives - dmg_to_buildings)

    print("-> Stats de DIFF : ")
    print(" Total dmg taken : ", total_dmg_taken)
    print(" Total dmg mitigated : ", dmg_self_mitigated)

    print("-> Stats de SUPP : ")
    print(" Effective Heal And Shielding : ", effective_heal_and_shielding)
    print(" totalHeal : ", total_heal)
    print(" totalDamageShieldedOnTeammates : ",total_damage_shielded_on_teammates )
    print(" totalHealsOnTeammates : ", total_heals_on_teammates)
    print(" totalUnitsHealed : ", total_units_healed)

    print("-> Stats de CC")
    print(" Enemy Champion Immobilizations : ", enemy_champion_immobilizations)
    print(" timeCCingOthers : ",time_ccing_others)
    print(" totalTimeCCDealt : ", total_time_cc_dealt)
    print(" knockEnemyIntoTeamAndKill : ", knock_enemy_into_team_and_kill)
    print(" immobilizeAndKillWithAlly : ", immobilize_and_kill_with_ally)

    print("-> Stats de Vision")
    print(" visionWardsBoughtInGame : ",visionWardsBoughtInGame)
    print(" wardsKilled : ",wardsKilled)
    print(" wardsPlaced : ",wardsPlaced)
    print(" controlWardsPlaced : ",controlWardsPlaced)
    print(" wardTakedowns : ",wardTakedowns)
    print(" wardsGuarded : ",wardsGuarded)
    print(" detectorWardsPlaced : ",detectorWardsPlaced)
    print(" enemyVisionPings : ",enemyVisionPings)
    print(" killAfterHiddenWithAlly : ",killAfterHiddenWithAlly)

    print("-> Stats de Autre ")
    print("kills : ",kills)
    print("deaths : ",deaths)
    print("assists : ",assists)
    print("gameLength : ",gameLength)
    print("goldEarned : ",goldEarned)
    print("multikillsAfterAggressiveFlash : ",multikillsAfterAggressiveFlash)
    print("pickKillWithAlly : ",pickKillWithAlly)
    print("saveAllyFromDeath : ",saveAllyFromDeath)
    print("skillshotsDodged : ",skillshotsDodged)
    print("skillshotsHit : ",skillshotsHit)
    print("survivedThreeImmobilizesInFight : ",survivedThreeImmobilizesInFight)
    print("tookLargeDamageSurvived : ",tookLargeDamageSurvived)
    print("longestTimeSpentLiving : ",longestTimeSpentLiving)
    print("totalTimeSpentDead : ",totalTimeSpentDead)

    return [dmg_to_buildings, dmg_to_objectives, dmg_to_turrets, 0, dmg_to_champs]  # même ordre que ton exemple

        


name = "Unna78" 
tag = "EUW"

puuid = api.get_puuid(name,tag)
matchs_id = api.get_match_ids(puuid,3)
match_1_data = api.get_match_data(matchs_id[2])
player_data=api.get_player_data_for_1_game(match_1_data,puuid)
player2_data=api.get_player_data_for_1_game(match_1_data,get_opponent_puuid(match_1_data,puuid))

printPlayer(player_data)
printPlayerAttckStats(player_data)
print("============")
printPlayer(player2_data)
printPlayerAttckStats(player2_data)







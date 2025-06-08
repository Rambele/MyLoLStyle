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

def printPlayerStats1(data_player):
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

        
#=========
def player_impact_in_game(game_data, player_puuid):
    # Trouver le joueur à partir de son puuid
    player_data = next((p for p in game_data['info']['participants'] if p['puuid'] == player_puuid), None)
    if not player_data:
        return None

    # Extraire les données de l'équipe du joueur
    team_id = player_data['teamId']
    team_players = [p for p in game_data['info']['participants'] if p['teamId'] == team_id]

    # Sums pour chaque section
    def team_sum(key, subkey=None):
        if subkey:
            return sum(p.get(key, {}).get(subkey, 0) for p in team_players)
        return sum(p.get(key, 0) for p in team_players)

    def percent(value, total):
        return round((value / total) * 100, 2) if total else 0.0

    # === Dégâts ===
    dmg_to_champs = player_data.get('totalDamageDealtToChampions', 0)
    dmg_to_buildings = player_data.get('damageDealtToBuildings', 0)
    dmg_to_objectives = player_data.get('damageDealtToObjectives', 0) - dmg_to_buildings

    team_dmg_to_champs = team_sum('totalDamageDealtToChampions')
    team_dmg_to_buildings = team_sum('damageDealtToBuildings')
    team_dmg_to_objectives = team_sum('damageDealtToObjectives') - team_dmg_to_buildings

    # === Tanking ===
    dmg_self_mitigated = player_data.get('damageSelfMitigated', 0)
    total_dmg_taken = player_data.get('totalDamageTaken', 0)
    team_dmg_self_mitigated = team_sum('damageSelfMitigated')
    team_total_dmg_taken = team_sum('totalDamageTaken')

    # === Utility ===
    effective_heal_and_shielding = player_data.get('challenges', {}).get('effectiveHealAndShielding', 0)
    total_damage_shielded_on_teammates = player_data.get('totalDamageShieldedOnTeammates', 0)
    total_heals_on_teammates = player_data.get('totalHealsOnTeammates', 0)
    total_self_heal = player_data.get('totalHeal', 0) - total_heals_on_teammates

    team_effective_heal_and_shielding = team_sum('challenges', 'effectiveHealAndShielding')
    team_damage_shielded = team_sum('totalDamageShieldedOnTeammates')
    team_heals_on_teammates = team_sum('totalHealsOnTeammates')
    team_self_heal = team_sum('totalHeal') - team_heals_on_teammates

    # === CC ===
    enemy_champion_immobilizations = player_data.get('challenges', {}).get('enemyChampionImmobilizations', 0)
    time_ccing_others = player_data.get('timeCCingOthers', 0)
    total_time_cc_dealt = player_data.get('totalTimeCCDealt', 0)

    team_immobilizations = team_sum('challenges', 'enemyChampionImmobilizations')
    team_ccing = team_sum('timeCCingOthers')
    team_total_cc = team_sum('totalTimeCCDealt')

    # === Vision ===
    wardsKilled = player_data.get('wardsKilled', 0)
    wardsPlaced = player_data.get('wardsPlaced', 0)
    controlWardsPlaced = player_data.get('challenges', {}).get('controlWardsPlaced', 0)
    wardsGuarded = player_data.get('challenges', {}).get('wardsGuarded', 0)

    team_wardsKilled = team_sum('wardsKilled')
    team_wardsPlaced = team_sum('wardsPlaced')
    team_controlWardsPlaced = team_sum('challenges', 'controlWardsPlaced')
    team_wardsGuarded = team_sum('challenges', 'wardsGuarded')

    # === KDA & KP ===
    kills = player_data.get('kills', 0)
    deaths = player_data.get('deaths', 0)
    assists = player_data.get('assists', 0)
    team_kills = sum(p.get('kills', 0) for p in team_players)
    kill_participation = percent(kills + assists, team_kills)

    return {
        'dmg_to_champs_%': percent(dmg_to_champs, team_dmg_to_champs),
        'dmg_to_buildings_%': percent(dmg_to_buildings, team_dmg_to_buildings),
        'dmg_to_objectives_%': percent(dmg_to_objectives, team_dmg_to_objectives),

        'dmg_self_mitigated_%': percent(dmg_self_mitigated, team_dmg_self_mitigated),
        'dmg_taken_%': percent(total_dmg_taken, team_total_dmg_taken),

        'effective_heal_and_shielding_%': percent(effective_heal_and_shielding, team_effective_heal_and_shielding),
        'damage_shielded_on_mates_%': percent(total_damage_shielded_on_teammates, team_damage_shielded),
        'heals_on_teammates_%': percent(total_heals_on_teammates, team_heals_on_teammates),
        'self_heal_%': percent(total_self_heal, team_self_heal),

        'enemy_immobilizations_%': percent(enemy_champion_immobilizations, team_immobilizations),
        'time_ccing_others_%': percent(time_ccing_others, team_ccing),
        'total_time_cc_dealt_%': percent(total_time_cc_dealt, team_total_cc),

        'wardsKilled_%': percent(wardsKilled, team_wardsKilled),
        'wardsPlaced_%': percent(wardsPlaced, team_wardsPlaced),
        'controlWardsPlaced_%': percent(controlWardsPlaced, team_controlWardsPlaced),
        'wardsGuarded_%': percent(wardsGuarded, team_wardsGuarded),

        'kill_participation_%': kill_participation
    }

#=========




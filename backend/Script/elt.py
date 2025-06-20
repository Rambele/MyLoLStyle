import api
import processor
from collections import defaultdict, Counter
import csv
import time

# Lire le fichier ../joueur
joueurs = []
with open("../joueur", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            nom, tag, _role = line.split(",")
            joueurs.append((nom.strip(), tag.strip(), _role.strip()))

print("Joueurs trouvés :", joueurs)

csv_rows = []

for nom, tag, _role in joueurs:
    print(f"\n=== {nom},{tag} ===")

    # Récupérer le PUUID du joueur
    puuid = api.get_puuid(nom, tag)

    # Récupérer les 30 derniers matchs
    match_ids = api.get_match_ids(puuid, count=60)
    match_datas = [api.get_match_data(match_id) for match_id in match_ids if api.get_match_data(match_id)]

    # Déterminer le rôle principal
    roles = []
    for match_data in match_datas:
        participants = match_data["info"]["participants"]
        for p in participants:
            if p["puuid"] == puuid:
                role = p.get("teamPosition", None)
                if role and role != "NONE" and role != "":
                    roles.append(role)
                break

    if roles:
        main_role = Counter(roles).most_common(1)[0][0]
        print(f"Main role détecté pour {nom} : {main_role}")
    else:
        print(f"Aucun rôle détecté pour {nom}")
        continue
    
    if _role != "n":
        main_role= _role
    # Filtrer les matchs sur ce rôle
    print("----------------------->",_role)
    filtered_match_datas = []
    for match_data in match_datas:
        participants = match_data["info"]["participants"]
        for p in participants:
            if p["puuid"] == puuid and p.get("teamPosition", None) == main_role:
                filtered_match_datas.append(match_data)
                break

    print(f"Nombre de parties où {nom} joue en {main_role} : {len(filtered_match_datas)}")

    diffs = defaultdict(list)

    numeroMatch = 0
    for match_data in filtered_match_datas:
        numeroMatch+=1
        impactP1 = processor.player_impact_in_game(match_data, puuid)
        opponent_puuid = processor.get_opponent_puuid(match_data, puuid)
        impactP2 = processor.player_impact_in_game(match_data, opponent_puuid)
        champion_name = next((p["championName"] for p in participants if p["puuid"] == puuid), "Unknown")

        if impactP1 is None or impactP2 is None:
            print("=================")
            print(f"[WARNING] Impact data manquant dans un match pour {nom}, numero match {numeroMatch}")
            print("Champion ",champion_name)
            print("PUUID OPPENET ",opponent_puuid)
            print("=================")
            continue  # Skip ce match

        all_stats = set(impactP1.keys()) | set(impactP2.keys())

        for stat in all_stats:
            value1 = impactP1.get(stat)
            value2 = impactP2.get(stat)

            if isinstance(value1, (int, float)) and isinstance(value2, (int, float)):
                diff = value1 - value2
                diffs[stat].append(diff)

    # Calcul du winrate
    wins = sum(1 for match_data in filtered_match_datas
               for p in match_data["info"]["participants"]
               if p["puuid"] == puuid and p.get("win"))

    total = len(filtered_match_datas)
    winrate = (wins / total) * 100 if total > 0 else 0

    # Récupérer les infos de rang
    rank_data = api.get_rank_info(puuid)

    # Construire la ligne pour le CSV
    player_row = {
        "summoner_name": nom,
        "tag": tag,
        "rank": rank_data.get("tier", "N/A"),
        "division": rank_data.get("rank", ""),
        "lp": rank_data.get("leaguePoints", "N/A"),
        "season_wins": rank_data.get("wins", 0),
        "season_losses": rank_data.get("losses", 0),
        "main_role": main_role,
        "games_analyzed": total,
        "winrate_main_role": round(winrate, 2)
    }

    # Ajouter toutes les stats d’impact (différence moyenne)
    for stat, values in diffs.items():
        moyenne = round(sum(values) / len(values), 2) if values else ""
        player_row[f"impact_{stat}"] = moyenne

    csv_rows.append(player_row)

    # Sauvegarder après chaque joueur pour ne rien perdre
    fieldnames = list(player_row.keys())
    with open("../mike.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    print(f"Fichier CSV mis à jour pour {nom}.")
    time.sleep(1)  # Pour éviter d'être rate limité par l'API

print("\nAnalyse terminée. Fichier CSV généré avec succès !")

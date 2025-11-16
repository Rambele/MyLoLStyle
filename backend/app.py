from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_compress import Compress
from re import compile
from Script import api, processor, impact_stats_config
import os
from collections import defaultdict, Counter
from Script.api import SummonerNotFound   # 🔹 importe l’exception

app = Flask(__name__)

# Perf : compression des réponses
Compress(app)

# CORS : autorise ton front (prod + previews Vercel) et le local
CORS(app, resources={
    r"/*": {
        "origins": [
            compile(r"https://.*\.vercel\.app$"),
            "https://impactgame.app",        # ✅ ton nouveau domaine
            "https://www.impactgame.app",    # ✅ (si tu veux que le www marche aussi)
            "http://localhost:5173",
            "http://localhost:3000"
        ],
        "methods": ["GET"],
        "allow_headers": ["Content-Type"]
    }
})

# Santé simple
@app.get("/ping")
def ping():
    return "pong"

# ====== Ta logique d'origine ======

# Récupération sécurisée de la clé API Riot
api_key = os.environ.get("RIOT_API_KEY")
if not api_key:
    raise Exception("RIOT_API_KEY not found in environment variables")

riot_api = api.RiotAPI(api_key=api_key)

@app.route('/analyze', methods=['GET'])
def analyze():
    summoner_name = request.args.get('name')
    tag = request.args.get('tag')

    if not summoner_name or not tag:
        return jsonify({"error": "Missing name or tag"}), 400

    try:
        try :
            puuid = riot_api.get_puuid(summoner_name, tag)
        except SummonerNotFound:
            return jsonify({"error": "SUMMONER_NOT_FOUND"}), 404
        match_ids = riot_api.get_match_ids(puuid, count=30, queue=420)

        match_roles = []
        full_match_data = []

        # Étape 1 : Récupère les rôles et data
        for match_id in match_ids:
            match_data = riot_api.get_match_data(match_id)
            participant = next(p for p in match_data["info"]["participants"] if p["puuid"] == puuid)
            role_key = f"{participant['teamPosition']}".lower()  # top, jungle, mid, etc.
            if role_key in {"top", "jungle", "middle", "bottom", "utility"}:
                match_roles.append(role_key)
                full_match_data.append((match_data, role_key))

        # Étape 2 : Trouve le rôle dominant
        most_common_role = Counter(match_roles).most_common(1)[0][0]

        # Étape 3 : Analyse les matchs de ce rôle uniquement
        impact_results = []
        champion_stats = {}  # {champion: {"games": X, "wins": Y}}
        for match_data, role in full_match_data:
            if role != most_common_role:
                continue
            
            # On récupère à nouveau ton participant pour connaître le champion joué
            participant = next(
                p for p in match_data["info"]["participants"]
                if p["puuid"] == puuid
            )

            champ_name = participant.get("championName")
            if champ_name:
                if champ_name not in champion_stats:
                    champion_stats[champ_name] = {"games": 0, "wins": 0}

                champion_stats[champ_name]["games"] += 1
                if participant.get("win"):
                    champion_stats[champ_name]["wins"] += 1

            process = processor.ImpactProcessor(match_data)
            impact = process.compare_vs_opponent(puuid, impact_stats_config.IMPACT_STATS)
            impact_results.append(impact)

        if not impact_results:
            return jsonify({"error": "Aucune game avec rôle dominant trouvée"}), 400

        # Étape 4 : Moyenne
        average_impact = defaultdict(float)
        for result in impact_results:
            for stat, value in result.items():
                average_impact[stat] += value
        for stat in average_impact:
            average_impact[stat] /= len(impact_results)

        # 🔹 Résumé des champions joués sur les games analysées
        champions_summary = []
        for champ, stats in champion_stats.items():
            games = stats["games"]
            wins = stats["wins"]
            winrate = round((wins / games) * 100, 1) if games > 0 else 0.0

            champions_summary.append({
                "champion": champ,
                "games": games,
                "wins": wins,
                "winrate": winrate
            })

        # on trie : les plus joués en premier
        champions_summary.sort(key=lambda x: x["games"], reverse=True)              


        # 🔹 Calcul du winrate des games analysées (rôle dominant uniquement)
        wins = 0
        total = 0

        for match_data, role in full_match_data:
            if role != most_common_role:
                continue

            participant = next(
                p for p in match_data["info"]["participants"]
                if p["puuid"] == puuid
            )

            total += 1
            if participant.get("win"):
                wins += 1

        winrate = round((wins / total) * 100, 1) if total > 0 else 0.0

        # Étape 5 : Retour complet
        response = {
            "role": most_common_role,
            "games_analyzed": len(impact_results),
            "winrate": winrate,            
            "impact": dict(average_impact),
            "champions": champions_summary,   # 🔥 nouveau champ
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ⚠️ Pas de app.run() ici : Gunicorn démarre l'app en prod

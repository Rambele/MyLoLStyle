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
        # 1) Récupération du PUUID
        try:
            puuid = riot_api.get_puuid(summoner_name, tag)
        except SummonerNotFound:
            return jsonify({"error": "SUMMONER_NOT_FOUND"}), 404

        # 2) Récupération des matchs récents en SoloQ
        match_ids = riot_api.get_match_ids(puuid, count=30, queue=420)

        match_roles = []
        full_matches = []  # (match_data, participant, role)

        for match_id in match_ids:
            match_data = riot_api.get_match_data(match_id)
            participants = match_data["info"]["participants"]

            participant = next((p for p in participants if p["puuid"] == puuid), None)
            if not participant:
                continue

            role_key = str(participant.get("teamPosition", "")).lower()
            if role_key in {"top", "jungle", "middle", "bottom", "utility"}:
                match_roles.append(role_key)
                full_matches.append((match_data, participant, role_key))

        if not match_roles:
            return jsonify({"error": "Aucune game avec rôle valide trouvée"}), 400

        # 3) Rôle dominant
        most_common_role = Counter(match_roles).most_common(1)[0][0]

        # 4) Analyse des matchs sur ce rôle : impact, winrate, champions
        impact_results = []
        average_impact = defaultdict(float)

        total_games = 0
        total_wins = 0

        champion_stats = {}  # {champion: {"games": X, "wins": Y}}

        for match_data, participant, role in full_matches:
            if role != most_common_role:
                continue

            total_games += 1
            if participant.get("win"):
                total_wins += 1

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

        # 5) Moyenne des impacts
        # 5) Moyenne des impacts (robuste aux None)
        stat_counts = defaultdict(int)

        for result in impact_results:
            for stat, value in result.items():
                if isinstance(value, (int, float)):  # on ignore les None et autres
                    average_impact[stat] += value
                    stat_counts[stat] += 1

        for stat, total in average_impact.items():
            count = stat_counts[stat] or 1
            average_impact[stat] = total / count


        # 6) Winrate global sur les games analysées
        winrate = round((total_wins / total_games) * 100, 1) if total_games > 0 else 0.0

        # 7) Champions joués + winrate par champion
        champions_summary = []
        for champ, stats in champion_stats.items():
            games = stats["games"]
            wins = stats["wins"]
            champ_winrate = round((wins / games) * 100, 1) if games > 0 else 0.0

            champions_summary.append({
                "champion": champ,
                "games": games,
                "wins": wins,
                "winrate": champ_winrate
            })

        champions_summary.sort(key=lambda x: x["games"], reverse=True)

        # 8) Réponse finale
        response = {
            "summoner_name": summoner_name,
            "tag": tag,
            "role": most_common_role,
            "games_analyzed": len(impact_results),
            "winrate": winrate,
            "impact": dict(average_impact),
            "champions": champions_summary,
        }

        return jsonify(response)

    except Exception as e:
        # En prod : tu peux logger e pour toi
        print("[ERROR] /analyze failed:", e)
        return jsonify({"error": str(e)}), 500


# ⚠️ Pas de app.run() ici : Gunicorn démarre l'app en prod

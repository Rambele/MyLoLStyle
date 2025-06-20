from flask import Flask, request, jsonify
from Script import api, processor, impact_stats_config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permet au frontend React d’accéder à l’API

# Init de l'API Riot
riot_api = api.RiotAPI(api_key="RGAPI-5ba2ef4e-7255-4996-8c35-f0e4bd1c7666")

@app.route('/analyze', methods=['GET'])
def analyze():
    summoner_name = request.args.get('name')
    tag = request.args.get('tag')

    if not summoner_name or not tag:
        return jsonify({"error": "Missing name or tag"}), 400

    try:
        puuid = riot_api.get_puuid(summoner_name, tag)
        match_ids = riot_api.get_match_ids(puuid, count=1, queue=420)
        match_data = riot_api.get_match_data(match_ids[0])
        process = processor.ImpactProcessor(match_data)

        impact_player = process.calculate_impact_vs_team(puuid, impact_stats_config.IMPACT_STATS)

        return jsonify(impact_player)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

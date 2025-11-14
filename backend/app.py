from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_compress import Compress
from Script import api, processor, impact_stats_config
import os
from collections import defaultdict, Counter

app = Flask(__name__)
Compress(app)
# Autorise ton front Vercel (ajoute ton autre domaine si tu en as un)
CORS(app, resources={
    r"/*": {
        "origins": [
            compile(r"https://.*\.vercel\.app$"),  # toutes tes URLs Vercel (prod+preview)
            "http://localhost:5173",
            "http://localhost:3000"
        ],
        "methods": ["GET"],
        "allow_headers": ["Content-Type"]
    }
})

# Santé simple pour tester le déploiement
@app.get("/ping")
def ping():
    return "pong"

# Récupération sécurisée de la clé API Riot
api_key = os.environ.get("RIOT_API_KEY")
if not api_key:
    raise Exception("RIOT_API_KEY not found in environment variables")

from flask import Flask, request, jsonify
from flask_cors import CORS
+from flask_compress import Compress
from Script import api, processor, impact_stats_config
import os
from collections import defaultdict, Counter

app = Flask(__name__)
-CORS(app)
+Compress(app)
+# Autorise ton front Vercel (ajoute ton autre domaine si tu en as un)
+CORS(app, resources={r"/*": {"origins": [
+    "https://my-lo-l-style-rachids-projects-28808a7f.vercel.app"
+]}})

# Santé simple pour tester le déploiement
+@app.get("/ping")
+def ping():
+    return "pong"

# Récupération sécurisée de la clé API Riot
api_key = os.environ.get("RIOT_API_KEY")
if not api_key:
    raise Exception("RIOT_API_KEY not found in environment variables")

#!/bin/bash

echo "📁 Création de la structure du projet MyLoLStyle..."

# Créer les dossiers principaux
mkdir -p frontend
mkdir -p backend/{riot_api,logic,utils,static}
mkdir -p shared

# Créer les fichiers backend de base
echo "from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return 'MyLoLStyle backend is running ✅'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
" > backend/app.py

# Fichier requirements.txt
echo -e "flask\nrequests\npython-dotenv" > backend/requirements.txt

# Créer le fichier .env (à compléter manuellement)
echo "RIOT_API_KEY=colle_ta_clé_ici" > .env

# Init frontend avec Create React App
npx create-react-app frontend --template cra-template

# Nettoyage React (facultatif)
rm -f frontend/src/logo.svg frontend/src/setupTests.js frontend/src/reportWebVitals.js frontend/src/App.test.js

# Affichage final
echo "✅ Structure complète créée."
echo "➡️ Lance ensuite : git add . && git commit -m 'Initialisation structure' && git push"

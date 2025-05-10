from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # autorise tous les domaines pour le test

@app.route("/info", methods=["GET"])
def send_info():
    return jsonify({
        "nom": "Slimane",
        "prenom": "Rachid",
        "naissance": "1998-03-15"
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

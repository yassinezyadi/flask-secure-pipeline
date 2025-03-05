from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Route pour recevoir les Webhooks GitHub
@app.route('/webhook', methods=['POST'])
def github_webhook():
    # Vérifier si la requête est bien un Webhook GitHub
    if request.method == 'POST':
        # Logique pour valider le Webhook, par exemple vérifier la signature
        # Tu peux utiliser une clé secrète GitHub pour valider les Webhooks

        payload = request.json  # Récupérer les données du Webhook

        # Exemple : On vérifie si le push est sur la branche principale (master/main)
        if payload.get('ref') == 'refs/heads/main':
            # Exécuter l'analyse de sécurité Semgrep dans le dépôt
            run_semgrep_analysis()

            return jsonify({"message": "Webhook reçu et analyse lancée"}), 200
        else:
            return jsonify({"message": "Pas sur la branche principale"}), 400

def run_semgrep_analysis():
    """Fonction pour exécuter Semgrep sur le code source"""
    try:
        # Exécuter Semgrep via un subprocess dans l'environnement virtuel
        subprocess.run(["semgrep", "--config=auto", "."], check=True)
        print("Analyse Semgrep terminée avec succès")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de Semgrep : {e}")

if __name__ == '__main__':
    app.run(debug=True, port=5000)

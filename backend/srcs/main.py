from flask import Flask, send_file, request, jsonify
import os
import matplotlib.pyplot as plt
import io
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route("/prediction_id", methods=["POST"])
def make_prediction_by_id():
    data = request.get_json()
    
    if not data or "animal_id" not in data:
        return jsonify({"error": "ID d'animal manquant"}), 400
    
    # Charger les données
    try:
        df_taureaux = pd.read_csv("./data/DATA_TAUREAUX_ANO.txt", sep="\t")  # Vérifie le séparateur
    except Exception as e:
        return jsonify({"error": f"Erreur lors du chargement des données : {str(e)}"}), 500
    
    animal_id = data["animal_id"]

    # Vérifier si l'ID existe dans le DataFrame
    animal_data = df_taureaux[df_taureaux["ID_ANIMAL"] == animal_id]
    
    if animal_data.empty:
        return jsonify({"error": "ID d'animal non trouvé"}), 404
    
    # Récupérer toutes les colonnes de l'animal
    variables_animal = animal_data.iloc[0].to_dict()

    # Remplacer les NaN par None pour éviter les erreurs JSON
    variables_animal = {k: (v if pd.notna(v) else None) for k, v in variables_animal.items()}
     
    # Appels des prédictions
    result = {
        "variables": variables_animal,
        "predictions": {
            "p_libeco2": prediction_libeco2(),
            "p_libeco3": prediction_libeco3(),
            "p_enchere": prediction_enchere(),
            "p_PN": prediction_PNC(),
            "p_PN210": prediction_PN210(),
        }
    }

    # Retour des résultats
    return jsonify(result)



def prediction_libeco2():
    
    
def prediction_libeco3():
    
    
def prediction_enchere():


def prediction_PNC():
    
    
def prediction_PN210():
    
    
    

if __name__ == '__main__':
    app.run(debug=True)

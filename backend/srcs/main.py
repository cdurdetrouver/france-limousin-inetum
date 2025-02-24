from flask import Flask, send_file, request, jsonify
import os
import matplotlib.pyplot as plt
import io
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/graph')
def generate_graph():
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [10, 20, 25, 30])

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return send_file(img, mimetype='image/png')


@app.route("/predidiction_id", methods=["POST"])
def make_prediction_by_id():
    data = request.get_json()
    
    if not data or "animal_id" not in data:
        return jsonify({"error": "ID d'animal manquant"}), 400
    
    # Préparation des variables
    result = []
    animal_id = data["animal_id"]
    data_taureaux = DATA_TAUREAUX_ANO.txt
    variables_to_get = ["IFNAIS", "CRSEVS", "DMSEVS", "DSSEVS", "ISEVRE", "IFVELA",
                    "ALAITS", "IVMATE", "MERPSS", "ICRCJF", "CONFJF", "cifnai",
                    "ccrsev", "cdmsev", "cdssev", "cfosse", "cavels", "calait"]
    
    animal_data = df_taureaux[df_taureaux["ID_ANIMAL"] == animal_id]
    if animal_data.empty:
        return jsonify({"error": "ID d'animal non trouvé"}), 404
    
    variables_animal = {var: animal_data[var].values[0] if var in animal_data.columns and pd.notna(animal_data[var].values[0]) else np.nan
              for var in variables_to_get}
     
    # Appels des prédictions
    result["p_libeco2"] = prediction_libeco2()
    result["p_libeco3"] = prediction_libeco3()
    result["p_enchere"] = prediction_enchere()
    result["p_PN"] = prediction_PN()
    result["p_PN120"] = prediction_PN120()
    result["p_PN210"] = prediction_PN210()

    # Retour des résultats
    return jsonify(result)


def prediction_libeco2():
    
    
def prediction_libeco3():
    
    
def prediction_enchere():


def prediction_PN():
    
    
def prediction_PN120():
    
    
def prediction_PN210():
    
    
    

if __name__ == '__main__':
    app.run(debug=True)

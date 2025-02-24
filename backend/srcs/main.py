from flask import Flask, send_file, request, jsonify
import os
import matplotlib.pyplot as plt
import io
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from pred import pred
import json 

app = Flask(__name__)


@app.route("/prediction_id", methods=["POST"])
def make_prediction_by_id():
    data = request.get_json()
    
    if not data or "id" not in data:
        return jsonify({"error": "ID d'animal manquant"}), 400

    animal_id = int(data["id"])

    result = pred(animal_id)
    result = {key: str(value) for key, value in result.items()}
    result = json.dumps(result)
    print(result)
    return result


if __name__ == '__main__':
    app.run(debug=True)
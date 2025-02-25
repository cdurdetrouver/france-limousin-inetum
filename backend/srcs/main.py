from flask import Flask, request, jsonify
from flask_cors import CORS
from pred import pred
import json

app = Flask(__name__)
CORS(app)

@app.route("/prediction_id", methods=["POST"])
def make_prediction_by_id():
    data = request.get_json()

    if not data or "id" not in data:
        return jsonify({"error": "ID d'animal manquant"}), 400

    animal_id = int(data["id"])

    result = pred(animal_id)
    result = {key: str(value) for key, value in result.items()}
    result = json.dumps(result)
    return result


if __name__ == '__main__':
    app.run(debug=True)

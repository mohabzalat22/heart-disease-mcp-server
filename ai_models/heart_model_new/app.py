from flask import Flask, request, jsonify
from flask_cors import CORS
from predict_pipeline import predict_heart_disease

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Heart Disease Prediction API is running"
    })

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        required_fields = [
            "Age",
            "Sex",
            "RestingBP",
            "Cholesterol",
            "FastingBS",
            "MaxHR",
            "ExerciseAngina",
            "Oldpeak",
            "ChestPainType",
            "RestingECG",
            "ST_Slope"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"Missing field: {field}"
                }), 400

        result = predict_heart_disease(data)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
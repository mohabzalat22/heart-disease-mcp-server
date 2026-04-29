import pandas as pd
import joblib

print("predict_pipeline.py is running...")

# 1) تحميل الموديل وترتيب الأعمدة
model = joblib.load("saved_models/best_model.pkl")
feature_columns = joblib.load("saved_models/feature_columns.pkl")


def preprocess_input(raw_data):
    # نبدأ بكل الأعمدة = 0
    data = {col: 0 for col in feature_columns}

    # الأعمدة الرقمية / الأساسية
    data["Age"] = raw_data["Age"]
    data["Sex"] = raw_data["Sex"]                  # 0 أو 1
    data["RestingBP"] = raw_data["RestingBP"]
    data["Cholesterol"] = raw_data["Cholesterol"]
    data["FastingBS"] = raw_data["FastingBS"]      # 0 أو 1
    data["MaxHR"] = raw_data["MaxHR"]
    data["ExerciseAngina"] = raw_data["ExerciseAngina"]   # 0 أو 1
    data["Oldpeak"] = raw_data["Oldpeak"]

    # العمود المحسوب
    if raw_data["MaxHR"] != 0:
        data["Cholesterol_HR_Ratio"] = raw_data["Cholesterol"] / raw_data["MaxHR"]
    else:
        data["Cholesterol_HR_Ratio"] = 0

    # One-hot encoding لـ ChestPainType
    chest_pain_col = f"ChestPainType_{raw_data['ChestPainType']}"
    if chest_pain_col in data:
        data[chest_pain_col] = 1

    # One-hot encoding لـ RestingECG
    ecg_col = f"RestingECG_{raw_data['RestingECG']}"
    if ecg_col in data:
        data[ecg_col] = 1

    # One-hot encoding لـ ST_Slope
    slope_col = f"ST_Slope_{raw_data['ST_Slope']}"
    if slope_col in data:
        data[slope_col] = 1

    # تحويل إلى DataFrame بنفس ترتيب الأعمدة
    df = pd.DataFrame([data])
    df = df[feature_columns]

    return df


def predict_heart_disease(raw_data):
    processed_df = preprocess_input(raw_data)

    prediction = model.predict(processed_df)[0]

    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(processed_df)[0][1]
    else:
        probability = None

    if prediction == 1:
        result_text = "High risk of heart disease"
    else:
        result_text = "Low risk of heart disease"

    return {
        "prediction": int(prediction),
        "probability_of_disease": float(probability) if probability is not None else None,
        "result_text": result_text
    }


# تجربة سريعة
if __name__ == "__main__":
    sample_input = {
        "Age": 55,
        "Sex": 1,
        "RestingBP": 140,
        "Cholesterol": 240,
        "FastingBS": 1,
        "MaxHR": 150,
        "ExerciseAngina": 1,
        "Oldpeak": 1.5,
        "ChestPainType": "ASY",
        "RestingECG": "Normal",
        "ST_Slope": "Flat"
    }

    result = predict_heart_disease(sample_input)
    print(result)
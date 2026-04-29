import pandas as pd
import joblib

print("test_prediction.py is running...")

# 1) تحميل الموديل
model = joblib.load("saved_models/best_model.pkl")

# 2) تحميل ترتيب الأعمدة
feature_columns = joblib.load("saved_models/feature_columns.pkl")

# 3) قراءة test data
test_df = pd.read_csv("data/test_heart.csv")

# 4) فصل الـ features عن الـ target
X_test = test_df.drop("HeartDisease", axis=1)
y_test = test_df["HeartDisease"]

# 5) ناخد أول صف فقط
sample = X_test.iloc[[0]]

# 6) نرتب الأعمدة بنفس ترتيب التدريب
sample = sample[feature_columns]

# 7) نعمل prediction
prediction = model.predict(sample)[0]

# 8) نطبع النتيجة
print("\nSample data:")
print(sample)

print("\nActual value:", y_test.iloc[0])
print("Predicted value:", prediction)

# 9) لو الموديل بيدعم probability
if hasattr(model, "predict_proba"):
    probability = model.predict_proba(sample)[0]
    print("Probabilities:", probability)
import pandas as pd
import joblib
import os

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)
import matplotlib.pyplot as plt

print("train_model.py is running...")

# =========================
# 1) Load train and test data
# =========================
train_df = pd.read_csv("data/train_heart.csv")
test_df = pd.read_csv("data/test_heart.csv")

# =========================
# 2) Split features and target
# =========================
X_train = train_df.drop("HeartDisease", axis=1)
y_train = train_df["HeartDisease"]

X_test = test_df.drop("HeartDisease", axis=1)
y_test = test_df["HeartDisease"]

# =========================
# 3) Make sure folders exist
# =========================
os.makedirs("saved_models", exist_ok=True)
os.makedirs("results", exist_ok=True)

# =========================
# 4) Train Logistic Regression
# =========================
log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train, y_train)

y_pred_log = log_model.predict(X_test)

print("\n" + "=" * 50)
print("Logistic Regression Report")
print("=" * 50)
print(classification_report(y_test, y_pred_log))

log_report = classification_report(y_test, y_pred_log, output_dict=True)
log_cm = confusion_matrix(y_test, y_pred_log)

# Save Logistic model
joblib.dump(log_model, "saved_models/logistic_model.pkl")

# Save Logistic confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=log_cm)
disp.plot()
plt.title("Logistic Regression Confusion Matrix")
plt.savefig("results/logistic_confusion_matrix.png")
plt.close()

# =========================
# 5) Train Random Forest
# =========================
rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
rf_model.fit(X_train, y_train)

y_pred_rf = rf_model.predict(X_test)

print("\n" + "=" * 50)
print("Random Forest Report")
print("=" * 50)
print(classification_report(y_test, y_pred_rf))

rf_report = classification_report(y_test, y_pred_rf, output_dict=True)
rf_cm = confusion_matrix(y_test, y_pred_rf)

# Save Random Forest model
joblib.dump(rf_model, "saved_models/random_forest_model.pkl")

# Save Random Forest confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=rf_cm)
disp.plot()
plt.title("Random Forest Confusion Matrix")
plt.savefig("results/random_forest_confusion_matrix.png")
plt.close()

# =========================
# 6) Compare models using Recall of class 1
# =========================
log_recall = log_report["1"]["recall"]
rf_recall = rf_report["1"]["recall"]

print("\n" + "=" * 50)
print("Model Comparison")
print("=" * 50)
print(f"Logistic Recall (class 1): {log_recall}")
print(f"Random Forest Recall (class 1): {rf_recall}")

if rf_recall > log_recall:
    best_model = rf_model
    best_model_name = "Random Forest"
    best_recall = rf_recall
else:
    best_model = log_model
    best_model_name = "Logistic Regression"
    best_recall = log_recall

# Save best model
joblib.dump(best_model, "saved_models/best_model.pkl")

# =========================
# 7) Save summary file
# =========================
with open("results/model_summary.txt", "w", encoding="utf-8") as f:
    f.write("Heart Disease Model Summary\n")
    f.write("=" * 50 + "\n\n")

    f.write("Logistic Regression Report:\n")
    f.write(classification_report(y_test, y_pred_log))
    f.write("\n\n")

    f.write("Random Forest Report:\n")
    f.write(classification_report(y_test, y_pred_rf))
    f.write("\n\n")

    f.write(f"Best Model: {best_model_name}\n")
    f.write(f"Best Recall for class 1: {best_recall}\n")

print("\n" + "=" * 50)
print(f"Best Model is: {best_model_name}")
print(f"Best Recall for class 1: {best_recall}")
print("All models and results saved successfully.")
print("=" * 50)
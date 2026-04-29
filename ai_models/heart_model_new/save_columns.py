import pandas as pd
import joblib

train_df = pd.read_csv("data/train_heart.csv")

X_train = train_df.drop("HeartDisease", axis=1)

joblib.dump(list(X_train.columns), "saved_models/feature_columns.pkl")

print("Feature columns saved successfully.")
print("Number of feature columns:", len(X_train.columns))
print("Columns:")
for i, col in enumerate(X_train.columns, start=1):
    print(f"{i}- {col}")
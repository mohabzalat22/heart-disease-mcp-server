import pandas as pd
from sklearn.model_selection import train_test_split

# 1) قراءة الداتا
df = pd.read_csv("data/heart.csv")

# 2) فصل الـ features عن الـ target
X = df.drop("HeartDisease", axis=1)
y = df["HeartDisease"]

# 3) تقسيم الداتا
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 4) رجّعهم DataFrame كاملين
train_df = X_train.copy()
train_df["HeartDisease"] = y_train

test_df = X_test.copy()
test_df["HeartDisease"] = y_test

# 5) احفظهم
train_df.to_csv("data/train_heart.csv", index=False)
test_df.to_csv("data/test_heart.csv", index=False)

print("Train shape:", train_df.shape)
print("Test shape:", test_df.shape)
print("Files saved successfully:")
print("- data/train_heart.csv")
print("- data/test_heart.csv")
import pandas as pd

file_path = "data/heart.csv"

df = pd.read_csv(file_path)

print("=" * 50)
print("First 5 rows:")
print(df.head())

print("\n" + "=" * 50)
print("Columns:")
print(df.columns.tolist())

print("\n" + "=" * 50)
print("Shape:")
print(df.shape)

print("\n" + "=" * 50)
print("Info:")
df.info()

print("\n" + "=" * 50)
print("Missing values:")
print(df.isnull().sum())

print("\n" + "=" * 50)
print("Duplicate rows:")
print(df.duplicated().sum())

# BUILD CLEAN BI DATASET


import pandas as pd
import numpy as np

# 1. Load raw dataset
df = pd.read_csv("data/raw/Scraped_Data.csv.zip")

# 2. Keep only Sale properties
df = df[df["RentOrSale"] == "Sale"].copy()

# 3. Remove extreme outliers (1% – 99%)
lower = df["exactPrice"].quantile(0.01)
upper = df["exactPrice"].quantile(0.99)
df = df[(df["exactPrice"] >= lower) & (df["exactPrice"] <= upper)]

# 4. Clean amenity columns (0,1,9 → 0,1)
amenity_cols = [col for col in df.columns if df[col].isin([0,1,9]).all()]
df[amenity_cols] = df[amenity_cols].replace(9, 0)

# 5. Create luxury score
df["luxury_score"] = df[amenity_cols].sum(axis=1)

# 6. Remove unrealistic carpet area
df = df[df["carpetArea"] > 100]

# 7. Clean categorical columns
categorical_fix_cols = ["facing", "furnishing", "propertyType"]

for col in categorical_fix_cols:
    df[col] = df[col].astype(str)
    df[col] = df[col].replace(["9", 9, "nan", "None"], "Unknown")

# 8. Create price per sqft
df["price_per_sqft"] = df["exactPrice"] / df["carpetArea"]

# 9. Select BI columns
bi_columns = [
    "exactPrice",
    "carpetArea",
    "bedrooms",
    "bathrooms",
    "balconies",
    "totalFlrNum",
    "luxury_score",
    "city",
    "propertyType",
    "furnishing",
    "facing",
    "price_per_sqft"
]

bi_df = df[bi_columns].dropna()

# 10. Export
bi_df.to_csv("data/processed/real_estate_bi_dataset.csv", index=False)

print("BI dataset built successfully.")
print("Final shape:", bi_df.shape)
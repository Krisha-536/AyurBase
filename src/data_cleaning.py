import pandas as pd
import os
from collections import Counter

# -------------------------------
# 1. LOAD DATASET (FIXED PATH)
# -------------------------------
base_dir = os.path.dirname(os.path.dirname(__file__))  # go to project root
file_path = os.path.join(base_dir, "data", "kaggle_dataset.csv")

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print("Dataset not found. Check file path.")
    exit()

print("Dataset Loaded Successfully!")
print(df.head())


# -------------------------------
# 2. BASIC CLEANING
# -------------------------------
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

df.fillna("unknown", inplace=True)
df.drop_duplicates(inplace=True)

print("\nAfter Cleaning:")
print(df.info())


# -------------------------------
# 3. HEALTH CONCERN CLASSIFICATION
# -------------------------------
def classify_disease(disease):
    disease = str(disease).lower()

    if any(x in disease for x in ["cough", "cold", "asthma"]):
        return "respiratory"
    elif any(x in disease for x in ["digestion", "stomach", "gas"]):
        return "digestive"
    elif any(x in disease for x in ["stress", "anxiety", "sleep"]):
        return "stress"
    elif any(x in disease for x in ["immunity", "weakness"]):
        return "immunity"
    elif any(x in disease for x in ["diabetes", "bp", "pressure"]):
        return "metabolic"
    else:
        return "other"

if 'disease' in df.columns:
    df['disease_category'] = df['disease'].apply(classify_disease)


# -------------------------------
# 4. DIGESTION & LIFESTYLE
# -------------------------------
if 'digestion_strength' in df.columns:
    df['digestion_strength'] = df['digestion_strength'].replace({
        'low': 'mild',
        'medium': 'moderate',
        'high': 'strong'
    })


# -------------------------------
# 5. SEASONAL MAPPING
# -------------------------------
def map_season(month):
    month = str(month).lower()

    if month in ['dec', 'jan', 'feb']:
        return 'winter'
    elif month in ['mar', 'apr', 'may']:
        return 'summer'
    elif month in ['jun', 'jul', 'aug', 'sep']:
        return 'monsoon'
    else:
        return 'unknown'

if 'month' in df.columns:
    df['season'] = df['month'].apply(map_season)


# -------------------------------
# 6. INGREDIENT PROCESSING
# -------------------------------
if 'ingredients' in df.columns:
    df['ingredients'] = df['ingredients'].apply(
        lambda x: [i.strip().lower() for i in str(x).split(',')]
    )


# -------------------------------
# 7. CONSTRAINT FILTERING (ALLERGIES)
# -------------------------------
allergies = ['milk', 'peanut', 'soy']

def remove_allergens(ingredients):
    return [i for i in ingredients if i not in allergies]

if 'ingredients' in df.columns:
    df['safe_ingredients'] = df['ingredients'].apply(remove_allergens)


# -------------------------------
# 8. ANALYTICAL INGREDIENT EVALUATION
# -------------------------------
if 'safe_ingredients' in df.columns:
    all_items = sum(df['safe_ingredients'], [])
    freq = Counter(all_items)

    print("\nTop Ingredients:")
    print(freq.most_common(10))


# -------------------------------
# 9. SAFETY VALIDATION
# -------------------------------
def validate(ingredients):
    return all(i not in allergies for i in ingredients)

if 'safe_ingredients' in df.columns:
    df['is_safe'] = df['safe_ingredients'].apply(validate)


# -------------------------------
# 10. SAVE CLEANED DATASET
# -------------------------------
output_path = os.path.join(base_dir, "data", "cleaned_dataset.csv")
df.to_csv(output_path, index=False)

print("\nCleaned dataset saved at:", output_path)


# -------------------------------
# 11. SAMPLE OUTPUT
# -------------------------------
print("\nSample Data:")
print(df.head())


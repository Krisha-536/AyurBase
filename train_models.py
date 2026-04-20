import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
import joblib
import warnings
warnings.filterwarnings('ignore')

# Non-medical and extremely rare disease keywords to filter out
DISEASE_BLOCKLIST_KEYWORDS = [
    'abuse', 'addiction', 'intoxication', 'withdrawal', 'suicide', 'homicide',
    'abortion', 'injury', 'fracture', 'poisoning', 'syndrome', 'behavior',
    'nailbiting', 'esteem', 'problem during pregnancy', 'problems during pregnancy',
    'foreign body', 'bite', 'burn', 'complication', 'smoking', 'tobacco'
]

# Middle Ground Grouping: Only group redundant anatomical variants
SYMPTOM_MERGES = {
    'Arm or Hand Pain': ['hand or finger pain', 'wrist pain', 'arm pain', 'elbow pain'],
    'Leg or Foot Pain': ['leg pain', 'hip pain', 'knee pain', 'foot or toe pain', 'ankle pain'],
    'Head or Neck Pain': ['headache', 'frontal headache', 'neck pain'],
    'Back Pain': ['back pain', 'low back pain'],
    'Abdominal or Pelvic Pain': ['sharp abdominal pain', 'lower abdominal pain', 'burning abdominal pain', 'upper abdominal pain', 'side pain', 'suprapubic pain', 'pelvic pain'],
    'Muscle or Joint Stiffness': ['stiffness or tightness', 'stiff'], # catches arm stiffness, neck stiffness, etc.
    'Muscle Cramps or Spasms': ['cramps or spasms', 'cramp', 'spasm'], # catches arm cramps, leg cramps, etc.
    'Localized Weakness': ['weakness'], # catches knee weakness, arm weakness, but we exclude 'weakness' (general) if we want
    'Swelling or Lumps in Extremities': ['hand or finger swelling', 'wrist swelling', 'arm swelling', 'knee swelling', 'leg swelling', 'foot or toe swelling', 'ankle swelling', 'hip swelling', 'elbow swelling', 'knee lump or mass', 'leg lump or mass', 'arm lump or mass', 'wrist lump or mass', 'hip lump or mass', 'elbow lump or mass', 'foot or toe lump or mass', 'hand or finger lump or mass']
}

def clean_and_group_symptoms(df):
    print(f"Original Dataset shape: {df.shape}", flush=True)
    
    # 1. Filter out unwanted diseases
    filtered_df = df[~df['diseases'].str.lower().str.contains('|'.join(DISEASE_BLOCKLIST_KEYWORDS))]
    print(f"Filtered out {len(df) - len(filtered_df)} rows of non-medical/rare diseases.", flush=True)
    print(f"Remaining diseases: {len(filtered_df['diseases'].unique())}", flush=True)
    
    # 2. Middle Ground Feature Grouping
    new_df = pd.DataFrame()
    new_df['diseases'] = filtered_df['diseases']
    
    original_cols = [c for c in filtered_df.columns if c != 'diseases']
    mapped_original_cols = set()
    
    # Apply merges
    for group_name, keywords in SYMPTOM_MERGES.items():
        new_df[group_name] = 0
        for col in original_cols:
            if any(kw in col.lower() for kw in keywords):
                # Ensure we don't accidentally map general 'weakness' into Localized Weakness if we want it separate
                if group_name == 'Localized Weakness' and col == 'weakness':
                    continue # Keep general weakness separate
                new_df[group_name] = new_df[group_name] | filtered_df[col]
                mapped_original_cols.add(col)
                
    # Copy over all other highly specific symptoms exactly as they are
    for col in original_cols:
        if col not in mapped_original_cols:
            new_df[col] = filtered_df[col]
            
    print(f"Reduced features from {len(original_cols)} to {len(new_df.columns)-1}.", flush=True)
    return new_df

def train_disease_model():
    print("Loading symptom_to_disease.csv...", flush=True)
    df = pd.read_csv("symptom_to_disease.csv")
    
    grouped_df = clean_and_group_symptoms(df)
    grouped_df.to_csv("grouped_symptoms_middle.csv", index=False)
    
    X = grouped_df.drop(columns=['diseases']).values
    y_raw = grouped_df['diseases'].values
    
    le = LabelEncoder()
    y = le.fit_transform(y_raw)
    
    joblib.dump(le, 'disease_label_encoder.pkl')
    symptoms = grouped_df.drop(columns=['diseases']).columns.tolist()
    joblib.dump(symptoms, 'symptoms_list.pkl')
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training MLPClassifier for Disease Prediction...", flush=True)
    model = MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=30, early_stopping=True, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"DiseasePredictor Accuracy on Test Set: {accuracy:.4f}", flush=True)
        
    joblib.dump(model, "disease_model.pkl")
    print("Disease Model saved.", flush=True)

def train_remedy_model():
    print("Loading remedy.csv...", flush=True)
    df = pd.read_csv("remedy.csv")
    
    df['Dosha Type'] = df['Dosha Type'].fillna('Unknown')
    df['Gender/Age Relevance'] = df['Gender/Age Relevance'].fillna('All')
    
    le_disease = LabelEncoder()
    le_dosha = LabelEncoder()
    le_gender_age = LabelEncoder()
    
    diseases = df['Problem'].tolist() + ['Unknown']
    doshas = df['Dosha Type'].tolist() + ['Unknown']
    genders = df['Gender/Age Relevance'].tolist() + ['Unknown']
    
    le_disease.fit(diseases)
    le_dosha.fit(doshas)
    le_gender_age.fit(genders)
    
    X_disease = le_disease.transform(df['Problem'])
    X_dosha = le_dosha.transform(df['Dosha Type'])
    X_gender_age = le_gender_age.transform(df['Gender/Age Relevance'])
    
    X = np.column_stack((X_disease, X_dosha, X_gender_age))
    y = df['ID'].values
    
    clf = DecisionTreeClassifier(random_state=42, max_depth=15)
    clf.fit(X, y)
    
    joblib.dump(clf, 'remedy_dt_model.pkl')
    joblib.dump({
        'disease': le_disease,
        'dosha': le_dosha,
        'gender_age': le_gender_age
    }, 'remedy_encoders.pkl')
    print("Remedy Decision Tree Model saved.", flush=True)

if __name__ == "__main__":
    train_disease_model()
    train_remedy_model()
    print("All models trained and saved successfully.", flush=True)

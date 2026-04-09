"""Configuration for the herbal remedy analysis and recommendation system."""
from __future__ import annotations

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_CANDIDATES = [
    BASE_DIR / 'data' / 'kaggle_dataset.csv',
    BASE_DIR / 'data' / 'AyurGenixAI_Dataset.csv',
    BASE_DIR / 'data' / 'AyurGenixAI_Dataset_cleaned.csv',
]

_env_path = os.environ.get('REMEDY_DATA_PATH')
DATA_PATH = Path(_env_path).expanduser() if _env_path else None
if DATA_PATH is None or not DATA_PATH.exists():
    for candidate in DEFAULT_DATA_CANDIDATES:
        if candidate.exists():
            DATA_PATH = candidate
            break
    else:
        DATA_PATH = DEFAULT_DATA_CANDIDATES[0]

APP_NAME = 'Multi-Factor Herbal Remedy Analysis and Recommendation System'
MAX_RESULTS = 5

# Weights used by the final ranking engine. The model is primarily content-based
# (TF-IDF + cosine similarity), then adjusted with structured profile matching,
# seasonal context, digestion profile, lifestyle context and safety gates.
SCORING_WEIGHTS = {
    'semantic_similarity': 4.5,
    'concern_match': 2.4,
    'symptom_match': 2.0,
    'season_match': 1.4,
    'digestion_match': 1.2,
    'lifestyle_match': 0.9,
    'availability_match': 0.8,
    'dosha_match': 0.6,
    'safety_penalty': 6.0,
    'allergy_penalty': 10.0,
    'condition_penalty': 3.0,
}

HEALTH_CONCERN_KEYWORDS = {
    'respiratory': ['cough', 'cold', 'asthma', 'bronch', 'sinus', 'throat', 'flu', 'fever', 'breath'],
    'digestive': ['indigestion', 'constipation', 'diarrhea', 'gastr', 'acidity', 'ibs', 'stomach', 'ulcer', 'bloating'],
    'immunity_related': ['immunity', 'immune', 'infection', 'viral', 'fever', 'cold', 'flu'],
    'stress_related': ['stress', 'anxiety', 'insomnia', 'sleep', 'fatigue', 'tension'],
    'metabolic': ['diabetes', 'thyroid', 'obesity', 'metabolic', 'cholesterol'],
    'cardiovascular': ['hypertension', 'blood pressure', 'heart', 'cholesterol'],
    'skin': ['skin', 'acne', 'eczema', 'psoriasis', 'rash'],
    'musculoskeletal': ['arthritis', 'joint', 'back pain', 'muscle', 'sprain'],
    'urinary': ['urinary', 'kidney', 'bladder', 'stone', 'renal'],
    'neurological': ['migraine', 'headache', 'seizure', 'neuropathy'],
}

SEASON_RULES = {
    'summer': {
        'prefer': ['cooling', 'light', 'hydrating', 'refreshing', 'soothing'],
        'avoid': ['warming', 'hot', 'spicy', 'heating'],
    },
    'winter': {
        'prefer': ['warming', 'spicy', 'nourishing', 'grounding'],
        'avoid': ['cold', 'cooling', 'icy'],
    },
    'monsoon': {
        'prefer': ['immunity', 'digestive', 'warm', 'dry', 'protective'],
        'avoid': ['heavy', 'stagnant', 'damp'],
    },
    'spring': {
        'prefer': ['detox', 'light', 'allergy', 'clearing'],
        'avoid': ['heavy', 'oily'],
    },
    'autumn': {
        'prefer': ['grounding', 'warm', 'stable'],
        'avoid': ['dry', 'cooling'],
    },
}

DIGESTION_RULES = {
    'weak': {
        'prefer': ['light', 'warm', 'easy to digest', 'gentle', 'soothing'],
        'avoid': ['heavy', 'oily', 'very spicy', 'rich'],
    },
    'moderate': {
        'prefer': ['balanced', 'moderate', 'gentle'],
        'avoid': [],
    },
    'strong': {
        'prefer': ['warming', 'spicy', 'robust', 'tonic'],
        'avoid': ['very light'],
    },
}

LIFESTYLE_FIELDS = ['stress_level', 'sleep_pattern', 'physical_activity', 'meal_consistency', 'dietary_habits']

CONDITION_RISK_HINTS = {
    'diabetes': ['honey', 'sugar', 'jaggery'],
    'hypertension': ['salt', 'salty'],
    'acidity': ['spicy', 'hot'],
    'kidney': ['high protein', 'salt'],
}

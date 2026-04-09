from __future__ import annotations

from typing import Any

import pandas as pd

from config import HEALTH_CONCERN_KEYWORDS, SEASON_RULES, DIGESTION_RULES
from backend.utils import extract_ingredient_keywords, normalize_text, split_items, unique_preserve_order

REQUIRED_COLUMNS = [
    'Disease', 'Symptoms', 'Seasonal Variation', 'Age Group', 'Gender',
    'Allergies (Food/Env)', 'Herbal/Alternative Remedies', 'Ayurvedic Herbs',
    'Formulation', 'Diet and Lifestyle Recommendations', 'Patient Recommendations',
    'Medical History', 'Current Medications', 'Stress Levels', 'Sleep Patterns',
    'Physical Activity Levels', 'Symptom Severity', 'Duration of Treatment',
    'Doshas', 'Constitution/Prakriti', 'Dietary Habits', 'Environmental Factors',
    'Risk Factors'
]


def classify_health_concern(text: str) -> str:
    text = normalize_text(text)
    for category, keywords in HEALTH_CONCERN_KEYWORDS.items():
        if any(k in text for k in keywords):
            return category
    return 'general'


def _ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    frame = df.copy()
    for col in REQUIRED_COLUMNS:
        if col not in frame.columns:
            frame[col] = ''
    for col in frame.columns:
        frame[col] = frame[col].where(frame[col].notna(), '')
        frame[col] = frame[col].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()
    return frame


def _build_search_text(row: pd.Series) -> str:
    parts = [
        row.get('Disease', ''), row.get('Symptoms', ''), row.get('Diagnosis & Tests', ''),
        row.get('Herbal/Alternative Remedies', ''), row.get('Ayurvedic Herbs', ''),
        row.get('Formulation', ''), row.get('Diet and Lifestyle Recommendations', ''),
        row.get('Patient Recommendations', ''), row.get('Medical History', ''),
        row.get('Current Medications', ''), row.get('Risk Factors', ''),
        row.get('Environmental Factors', ''), row.get('Stress Levels', ''),
        row.get('Sleep Patterns', ''), row.get('Physical Activity Levels', ''),
        row.get('Dietary Habits', ''), row.get('Doshas', ''), row.get('Constitution/Prakriti', ''),
        row.get('Seasonal Variation', ''), row.get('Age Group', ''), row.get('Gender', ''),
    ]
    return ' | '.join(p for p in parts if normalize_text(p))


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    frame = _ensure_columns(df)

    frame['health_concern_group'] = frame['Disease'].apply(classify_health_concern)
    frame['disease_norm'] = frame['Disease'].map(normalize_text)
    frame['symptoms_norm'] = frame['Symptoms'].map(normalize_text)
    frame['season_norm'] = frame['Seasonal Variation'].map(normalize_text)
    frame['age_group_norm'] = frame['Age Group'].map(normalize_text)
    frame['gender_norm'] = frame['Gender'].map(normalize_text)
    frame['severity_norm'] = frame['Symptom Severity'].map(normalize_text)

    parsed_sources = [
        ('Herbal/Alternative Remedies', 'herbal_remedies_list'),
        ('Ayurvedic Herbs', 'ayurvedic_herbs_list'),
        ('Symptoms', 'symptoms_list'),
        ('Allergies (Food/Env)', 'allergy_list'),
        ('Seasonal Variation', 'season_list'),
        ('Diet and Lifestyle Recommendations', 'diet_lifestyle_list'),
        ('Patient Recommendations', 'patient_recommendations_list'),
        ('Current Medications', 'medications_list'),
        ('Medical History', 'medical_history_list'),
        ('Stress Levels', 'stress_list'),
        ('Sleep Patterns', 'sleep_list'),
        ('Physical Activity Levels', 'activity_list'),
        ('Dietary Habits', 'dietary_list'),
        ('Environmental Factors', 'environment_list'),
        ('Risk Factors', 'risk_list'),
    ]
    for source, target in parsed_sources:
        frame[target] = frame[source].apply(split_items)

    frame['ingredient_list'] = frame.apply(
        lambda row: unique_preserve_order(
            extract_ingredient_keywords(row['Herbal/Alternative Remedies'])
            + extract_ingredient_keywords(row['Ayurvedic Herbs'])
            + extract_ingredient_keywords(row['Formulation'])
        ),
        axis=1,
    )

    frame['context_tags'] = frame.apply(
        lambda row: unique_preserve_order(
            split_items(row['Seasonal Variation']) + split_items(row['Doshas']) + split_items(row['Constitution/Prakriti'])
        ),
        axis=1,
    )

    frame['search_text'] = frame.apply(_build_search_text, axis=1)
    frame['digestive_orientation'] = frame['Diet and Lifestyle Recommendations'].map(normalize_text)
    frame['safety_text'] = frame.apply(
        lambda row: ' | '.join(
            [row['Allergies (Food/Env)'], row['Medical History'], row['Current Medications'], row['Risk Factors']]
        ),
        axis=1,
    )
    return frame


def build_user_profile(**kwargs: Any) -> dict[str, Any]:
    def _clean_text(value):
        return normalize_text(value)

    def _clean_list(value):
        if isinstance(value, list):
            return [normalize_text(v) for v in value if normalize_text(v)]
        return split_items(value)

    age = kwargs.get('age')
    try:
        age = int(age) if age not in (None, '', 'null') else None
    except Exception:
        age = None

    profile = {
        'concern': _clean_text(kwargs.get('concern')),
        'symptoms': _clean_text(kwargs.get('symptoms')),
        'season': _clean_text(kwargs.get('season')),
        'digestion_strength': _clean_text(kwargs.get('digestion_strength') or kwargs.get('digestion')),
        'meal_consistency': _clean_text(kwargs.get('meal_consistency')),
        'age': age,
        'gender': _clean_text(kwargs.get('gender')),
        'allergies': _clean_list(kwargs.get('allergies')),
        'medical_history': _clean_list(kwargs.get('medical_history')),
        'current_medications': _clean_list(kwargs.get('current_medications')),
        'stress_level': _clean_text(kwargs.get('stress_level')),
        'sleep_pattern': _clean_text(kwargs.get('sleep_pattern')),
        'physical_activity': _clean_text(kwargs.get('physical_activity')),
        'dietary_habits': _clean_text(kwargs.get('dietary_habits')),
        'available_ingredients': _clean_list(kwargs.get('available_ingredients')),
        'family_history': _clean_list(kwargs.get('family_history')),
    }
    profile['health_concern_group'] = classify_health_concern(' '.join([profile['concern'], profile['symptoms']]))
    profile['query_text'] = ' | '.join(
        part for part in [
            profile['concern'], profile['symptoms'], profile['season'], profile['digestion_strength'],
            profile['meal_consistency'], profile['stress_level'], profile['sleep_pattern'],
            profile['physical_activity'], profile['dietary_habits'], ' '.join(profile['medical_history']),
            ' '.join(profile['current_medications']), ' '.join(profile['allergies']), ' '.join(profile['available_ingredients'])
        ] if part
    )
    return profile

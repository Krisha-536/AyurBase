from __future__ import annotations

from typing import Iterable

from config import CONDITION_RISK_HINTS
from backend.utils import age_matches, contains_any, gender_matches, normalize_text, season_matches, split_items


def _allergy_overlap(record_text: str, allergies: list[str]) -> bool:
    record_terms = set(split_items(record_text))
    user_terms = set(normalize_text(a) for a in allergies if normalize_text(a))
    if not record_terms or not user_terms:
        return False
    return bool(record_terms & user_terms)


def _ingredient_overlap(ingredients: list[str], allergies: list[str]) -> bool:
    record_terms = set(normalize_text(i) for i in ingredients if normalize_text(i))
    user_terms = set(normalize_text(a) for a in allergies if normalize_text(a))
    return bool(record_terms & user_terms)


def filter_records(records, profile: dict) -> list:
    kept = []
    for record in records:
        if not age_matches(profile.get('age'), record.age_group):
            continue
        if not gender_matches(profile.get('gender'), record.gender):
            continue
        if _allergy_overlap(record.allergies, profile.get('allergies', [])):
            continue
        if _ingredient_overlap(record.ingredients + record.herbs + record.remedies, profile.get('allergies', [])):
            continue
        kept.append(record)
    return kept


def safety_flags(profile: dict, record) -> list[str]:
    flags = []
    text_blob = ' | '.join([
        record.search_text,
        record.raw.get('Diet and Lifestyle Recommendations', ''),
        record.raw.get('Patient Recommendations', ''),
        record.raw.get('Medical Intervention', ''),
    ])
    user_medical = ' '.join(profile.get('medical_history', []))
    user_meds = ' '.join(profile.get('current_medications', []))
    user_allergies = profile.get('allergies', [])

    if _allergy_overlap(record.allergies, user_allergies):
        flags.append('Potential allergy overlap from the source record.')
    if _ingredient_overlap(record.ingredients + record.herbs + record.remedies, user_allergies):
        flags.append('One or more listed ingredients overlap with the allergy list.')

    # Conservative condition-aware cautions.
    for condition, hints in CONDITION_RISK_HINTS.items():
        if condition in normalize_text(user_medical) or condition in normalize_text(user_meds):
            if contains_any(text_blob, hints):
                flags.append(f'Contains text cues that may need caution for {condition}.')
    return flags

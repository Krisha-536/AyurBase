from __future__ import annotations

from collections import Counter
from itertools import combinations
from typing import Any

import numpy as np

from config import DIGESTION_RULES, MAX_RESULTS, SCORING_WEIGHTS, SEASON_RULES
from backend.filtering import filter_records, safety_flags
from backend.preprocessing import classify_health_concern
from backend.utils import contains_any, normalize_text, phrase_overlap, safe_div, split_items


DIGESTION_KEYWORDS = {
    'weak': ['light', 'gentle', 'soothing', 'easy to digest', 'warm water', 'simple'],
    'moderate': ['balanced', 'moderate', 'regular'],
    'strong': ['warming', 'spicy', 'tonic', 'robust', 'digestive'],
}

LIFESTYLE_KEYWORDS = {
    'stress_level': ['stress', 'calming', 'relax', 'tension', 'mind'],
    'sleep_pattern': ['sleep', 'rest', 'night', 'insomnia', 'relaxation'],
    'physical_activity': ['exercise', 'movement', 'walk', 'activity', 'yoga'],
    'dietary_habits': ['diet', 'food', 'meal', 'fiber', 'light', 'healthy'],
}


def _score_keyword_fit(user_value: str, text: str, category: str) -> float:
    user_value = normalize_text(user_value)
    text = normalize_text(text)
    if not user_value or not text:
        return 0.0
    rules = DIGESTION_RULES if category == 'digestion' else SEASON_RULES
    if user_value not in rules:
        return 0.0
    preferred = rules[user_value]['prefer']
    avoid = rules[user_value]['avoid']
    pref_score = 0.0
    if contains_any(text, preferred):
        pref_score += 1.0
    if contains_any(text, avoid):
        pref_score -= 0.6
    return max(0.0, pref_score)


def _lifestyle_fit(profile: dict[str, Any], record) -> tuple[float, dict[str, float]]:
    values = {
        'stress_level': profile.get('stress_level', ''),
        'sleep_pattern': profile.get('sleep_pattern', ''),
        'physical_activity': profile.get('physical_activity', ''),
        'dietary_habits': profile.get('dietary_habits', ''),
    }
    field_texts = {
        'stress_level': record.raw.get('Stress Levels', ''),
        'sleep_pattern': record.raw.get('Sleep Patterns', ''),
        'physical_activity': record.raw.get('Physical Activity Levels', ''),
        'dietary_habits': record.raw.get('Dietary Habits', ''),
    }
    sub = {}
    total = 0.0
    for field, user_value in values.items():
        score = phrase_overlap(user_value, field_texts[field])
        sub[field] = score
        total += score
    return total / max(1, len(values)), sub


def _availability_match(profile: dict[str, Any], record) -> float:
    available = set(normalize_text(x) for x in profile.get('available_ingredients', []) if normalize_text(x))
    if not available:
        return 0.0
    record_items = set(normalize_text(x) for x in (record.ingredients + record.herbs + record.remedies) if normalize_text(x))
    if not record_items:
        return 0.0
    return safe_div(len(available & record_items), len(record_items))


def _concern_match(profile: dict[str, Any], record) -> float:
    concern = profile.get('concern', '')
    symptoms = profile.get('symptoms', '')
    return max(
        phrase_overlap(concern, record.disease),
        phrase_overlap(concern, record.symptoms),
        phrase_overlap(symptoms, record.symptoms),
        phrase_overlap(symptoms, record.raw.get('Diagnosis & Tests', '')),
    )


def _season_fit(profile: dict[str, Any], record) -> float:
    season = normalize_text(profile.get('season'))
    if not season:
        return 0.0
    record_text = ' '.join([
        record.season,
        record.raw.get('Diet and Lifestyle Recommendations', ''),
        record.raw.get('Patient Recommendations', ''),
        record.raw.get('Formulation', ''),
    ])
    score = 0.0
    if season in normalize_text(record.season):
        score += 1.0
    rules = SEASON_RULES.get(season, {'prefer': [], 'avoid': []})
    if contains_any(record_text, rules['prefer']):
        score += 0.55
    if contains_any(record_text, rules['avoid']):
        score -= 0.45
    return max(0.0, score)


def _digestion_fit(profile: dict[str, Any], record) -> float:
    digestion = normalize_text(profile.get('digestion_strength'))
    if not digestion:
        return 0.0
    record_text = ' '.join([
        record.raw.get('Diet and Lifestyle Recommendations', ''),
        record.raw.get('Patient Recommendations', ''),
        record.raw.get('Formulation', ''),
        record.raw.get('Dietary Habits', ''),
    ])
    return _score_keyword_fit(digestion, record_text, 'digestion')


def _severity_fit(profile: dict[str, Any], record) -> float:
    user_text = normalize_text(profile.get('symptoms'))
    record_severity = normalize_text(record.severity)
    if not user_text or not record_severity:
        return 0.0
    if any(k in record_severity for k in ['severe', 'high']) and any(k in user_text for k in ['severe', 'worse', 'persistent', 'high']):
        return 1.0
    if any(k in record_severity for k in ['mild']) and any(k in user_text for k in ['mild', 'light', 'minor']):
        return 1.0
    return 0.35


def _dosha_fit(profile: dict[str, Any], record) -> float:
    user_text = ' '.join([
        profile.get('concern', ''), profile.get('symptoms', ''), profile.get('season', ''),
        profile.get('digestion_strength', ''), profile.get('dietary_habits', ''),
    ])
    return max(phrase_overlap(user_text, record.doshas), phrase_overlap(user_text, record.prakriti))


def build_user_profile(**kwargs: Any) -> dict[str, Any]:
    from backend.preprocessing import build_user_profile as _build
    return _build(**kwargs)


def rank_recommendations(kb, profile: dict[str, Any], limit: int = MAX_RESULTS) -> list[dict[str, Any]]:
    query = profile.get('query_text') or ' '.join(x for x in [profile.get('concern', ''), profile.get('symptoms', '')] if x)
    search_hits = kb.search(query, limit=75)
    candidate_records = filter_records([record for record, _ in search_hits], profile)

    ranked = []
    for record, semantic_score in search_hits:
        if record not in candidate_records:
            continue

        concern_score = _concern_match(profile, record)
        season_score = _season_fit(profile, record)
        digestion_score = _digestion_fit(profile, record)
        lifestyle_score, lifestyle_breakdown = _lifestyle_fit(profile, record)
        availability_score = _availability_match(profile, record)
        dosha_score = _dosha_fit(profile, record)
        severity_score = _severity_fit(profile, record)

        safety_notes = safety_flags(profile, record)
        safety_penalty = 0.0
        if safety_notes:
            safety_penalty += min(1.0, len(safety_notes) * 0.35)

        score = (
            SCORING_WEIGHTS['semantic_similarity'] * semantic_score
            + SCORING_WEIGHTS['concern_match'] * concern_score
            + SCORING_WEIGHTS['symptom_match'] * severity_score
            + SCORING_WEIGHTS['season_match'] * season_score
            + SCORING_WEIGHTS['digestion_match'] * digestion_score
            + SCORING_WEIGHTS['lifestyle_match'] * lifestyle_score
            + SCORING_WEIGHTS['availability_match'] * availability_score
            + SCORING_WEIGHTS['dosha_match'] * dosha_score
            - SCORING_WEIGHTS['safety_penalty'] * safety_penalty
        )

        reasons = []
        comp = {
            'semantic_similarity': round(semantic_score, 4),
            'concern_match': round(concern_score, 4),
            'season_match': round(season_score, 4),
            'digestion_match': round(digestion_score, 4),
            'lifestyle_match': round(lifestyle_score, 4),
            'availability_match': round(availability_score, 4),
            'dosha_match': round(dosha_score, 4),
            'severity_fit': round(severity_score, 4),
            'safety_penalty': round(safety_penalty, 4),
        }

        if semantic_score >= 0.2:
            reasons.append('Strong semantic similarity to the user query.')
        if concern_score >= 0.2:
            reasons.append('Matches the stated health concern and symptoms.')
        if season_score >= 0.3:
            reasons.append(f'Seasonal profile aligns with {profile.get("season", "the selected season")} context.')
        if digestion_score >= 0.3:
            reasons.append('Ingredient and lifestyle guidance fit the digestion profile.')
        if lifestyle_score >= 0.25:
            reasons.append('Lifestyle guidance aligns with stress, sleep, activity, or diet pattern.')
        if availability_score >= 0.25:
            reasons.append('Uses ingredients you marked as available.')
        if dosha_score >= 0.2:
            reasons.append('Descriptive language matches the dosha / prakriti pattern.')
        if safety_notes:
            reasons.append('Safety validation added caution notes before ranking.')

        ranked.append({
            'disease': record.disease,
            'health_concern_group': profile.get('health_concern_group') or classify_health_concern(record.disease),
            'score': round(score, 4),
            'semantic_similarity': round(semantic_score, 4),
            'season': record.season,
            'age_group': record.age_group,
            'gender': record.gender,
            'symptoms': record.symptoms,
            'diagnosis_tests': record.raw.get('Diagnosis & Tests', ''),
            'medical_history': record.raw.get('Medical History', ''),
            'current_medications': record.raw.get('Current Medications', ''),
            'risk_factors': record.raw.get('Risk Factors', ''),
            'ingredients': record.ingredients,
            'herbs': record.herbs,
            'remedies': record.remedies,
            'doshas': record.doshas,
            'prakriti': record.prakriti,
            'diet_lifestyle': record.raw.get('Diet and Lifestyle Recommendations', ''),
            'yoga': record.raw.get('Yoga & Physical Therapy', ''),
            'medical_intervention': record.raw.get('Medical Intervention', ''),
            'prevention': record.raw.get('Prevention', ''),
            'prognosis': record.raw.get('Prognosis', ''),
            'complications': record.raw.get('Complications', ''),
            'patient_recommendations': record.raw.get('Patient Recommendations', ''),
            'matched_components': comp,
            'lifestyle_breakdown': {k: round(v, 4) for k, v in lifestyle_breakdown.items()},
            'safety_notes': safety_notes,
            'reasons': reasons,
        })

    ranked.sort(key=lambda item: item['score'], reverse=True)
    return ranked[:limit]


def ingredient_frequency_summary(kb, records: list | None = None, top_n: int = 10) -> list[dict[str, Any]]:
    if records:
        counts = Counter()
        for record in records:
            for ingredient in record.get('ingredients', []):
                counts[ingredient] += 1
            for herb in record.get('herbs', []):
                counts[herb] += 1
        return [{'ingredient': ing, 'count': count} for ing, count in counts.most_common(top_n)]
    return [{'ingredient': ing, 'count': count} for ing, count in kb.ingredient_top_n(top_n)]


def ingredient_cooccurrence_summary(records: list[dict[str, Any]], top_n: int = 10) -> list[dict[str, Any]]:
    pairs = Counter()
    for record in records:
        items = [x for x in (record.get('ingredients', []) + record.get('herbs', [])) if x]
        for a, b in combinations(sorted(set(items)), 2):
            pairs[(a, b)] += 1
    return [
        {'ingredient_a': a, 'ingredient_b': b, 'count': count}
        for (a, b), count in pairs.most_common(top_n)
    ]


def explain_recommendation(profile: dict[str, Any], item: dict[str, Any]) -> dict[str, Any]:
    highlights = []
    if item['matched_components']['semantic_similarity'] >= 0.2:
        highlights.append('Semantic match')
    if item['matched_components']['season_match'] >= 0.3:
        highlights.append('Season fit')
    if item['matched_components']['digestion_match'] >= 0.3:
        highlights.append('Digestion fit')
    if item['matched_components']['availability_match'] >= 0.25:
        highlights.append('Availability fit')
    if item['matched_components']['lifestyle_match'] >= 0.25:
        highlights.append('Lifestyle fit')

    return {
        'summary': ' ; '.join(item['reasons']) if item['reasons'] else 'Selected using the dataset-driven ranking model.',
        'highlights': highlights,
        'safety_notes': item['safety_notes'],
        'component_scores': item['matched_components'],
    }


def build_response(kb, profile: dict[str, Any], limit: int = MAX_RESULTS) -> dict[str, Any]:
    recommendations = rank_recommendations(kb, profile, limit=limit)
    top_ingredients = ingredient_frequency_summary(kb, recommendations, 10)
    top_pairs = ingredient_cooccurrence_summary(recommendations, 10)
    return {
        'profile': profile,
        'health_concern_group': profile.get('health_concern_group'),
        'recommendations': [{**item, 'explanation': explain_recommendation(profile, item)} for item in recommendations],
        'top_ingredients': top_ingredients,
        'top_pairs': top_pairs,
        'safety_summary': {
            'passed': all(not r['safety_notes'] for r in recommendations),
            'reviewed': len(recommendations),
        },
    }

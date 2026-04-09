from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Iterable, List, Sequence

import pandas as pd

_SPLIT_PATTERN = re.compile(r"[,\n;/|]+")


def normalize_text(value) -> str:
    if value is None:
        return ''
    try:
        if pd.isna(value):
            return ''
    except Exception:
        pass
    text = str(value).strip().lower()
    text = re.sub(r'\s+', ' ', text)
    return text


def split_items(value) -> List[str]:
    text = normalize_text(value)
    if not text or text in {'none', 'none specific', 'n/a', 'na', '-', 'null', 'nan'}:
        return []
    parts = [p.strip() for p in _SPLIT_PATTERN.split(text)]
    cleaned = []
    for part in parts:
        part = re.sub(r'\s+', ' ', part).strip(' .')
        if part and part not in {'none', 'none specific', 'n/a', 'na', '-', 'null', 'nan'}:
            cleaned.append(part)
    return cleaned


def tokenize(value) -> List[str]:
    text = normalize_text(value)
    if not text:
        return []
    return [t for t in re.findall(r'[a-z0-9]+', text) if len(t) > 1]


def unique_preserve_order(items: Iterable[str]) -> List[str]:
    seen = set()
    out = []
    for item in items:
        item = normalize_text(item)
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def phrase_overlap(query: str, text: str) -> float:
    q = normalize_text(query)
    t = normalize_text(text)
    if not q or not t:
        return 0.0
    q_tokens = set(tokenize(q))
    t_tokens = set(tokenize(t))
    if not q_tokens or not t_tokens:
        return 0.0
    token_score = len(q_tokens & t_tokens) / len(q_tokens)
    seq_score = SequenceMatcher(None, q, t).ratio()
    return max(token_score, seq_score * 0.8)


def extract_ingredient_keywords(text: str) -> List[str]:
    items = split_items(text)
    out = []
    for item in items:
        item = re.sub(r'\([^)]*\)', '', item)
        item = re.sub(r'\b\d+(?:\.\d+)?\s*(mg|g|ml|tsp|tbsp|cup|cups|drops?|pieces?|leaf|leaves|slices?)\b', '', item)
        item = re.sub(r'\b\d+(?:\.\d+)?\b', '', item)
        item = re.sub(r'\s+', ' ', item).strip(' -:')
        if item:
            out.append(item)
    return unique_preserve_order(out)


def parse_age_group(age_group: str):
    text = normalize_text(age_group)
    if not text or 'all age' in text or 'any age' in text:
        return None, None
    nums = re.findall(r'\d+', text)
    if not nums:
        return None, None
    if '+' in text and len(nums) == 1:
        return int(nums[0]), None
    if len(nums) >= 2:
        return int(nums[0]), int(nums[1])
    return int(nums[0]), int(nums[0])


def age_matches(user_age: int | None, age_group_text: str) -> bool:
    if user_age is None:
        return True
    low, high = parse_age_group(age_group_text)
    if low is None and high is None:
        return True
    if high is None:
        return user_age >= low
    return low <= user_age <= high


def gender_matches(user_gender: str | None, row_gender: str) -> bool:
    user_gender = normalize_text(user_gender)
    row_gender = normalize_text(row_gender)
    if not user_gender or not row_gender:
        return True
    if row_gender in {'all genders', 'both genders', 'any gender'}:
        return True
    if user_gender.startswith('f') and 'female' in row_gender:
        return True
    if user_gender.startswith('m') and 'male' in row_gender:
        return True
    return user_gender in row_gender


def season_matches(user_season: str | None, row_seasons: str) -> bool:
    user_season = normalize_text(user_season)
    row_seasons = normalize_text(row_seasons)
    if not user_season or not row_seasons:
        return True
    if user_season in row_seasons:
        return True
    if user_season == 'rainy' and 'monsoon' in row_seasons:
        return True
    if user_season == 'monsoon' and 'rainy' in row_seasons:
        return True
    return False


def contains_any(text: str, keywords: Sequence[str]) -> bool:
    text = normalize_text(text)
    return any(normalize_text(k) in text for k in keywords if normalize_text(k))

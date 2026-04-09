from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.data_loader import load_data
from backend.preprocessing import preprocess_dataframe
from backend.utils import normalize_text, tokenize, unique_preserve_order


@dataclass(frozen=True)
class RemedyRecord:
    idx: int
    disease: str
    symptoms: str
    season: str
    age_group: str
    gender: str
    allergies: str
    herbs: list[str]
    remedies: list[str]
    ingredients: list[str]
    severity: str
    doshas: str
    prakriti: str
    search_text: str
    raw: dict


class RemedyKnowledgeBase:
    def __init__(self, df: pd.DataFrame):
        self.df = df.reset_index(drop=True)
        self.records = [self._row_to_record(i, row) for i, (_, row) in enumerate(self.df.iterrows())]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words='english')
        self.doc_matrix = self.vectorizer.fit_transform([r.search_text for r in self.records])
        self._build_indexes()

    @classmethod
    def from_csv(cls, path: str | None = None) -> 'RemedyKnowledgeBase':
        df = preprocess_dataframe(load_data(path))
        return cls(df)

    def _row_to_record(self, idx: int, row: pd.Series) -> RemedyRecord:
        raw = row.to_dict()
        return RemedyRecord(
            idx=idx,
            disease=str(row.get('Disease', '')).strip(),
            symptoms=str(row.get('Symptoms', '')).strip(),
            season=str(row.get('Seasonal Variation', '')).strip(),
            age_group=str(row.get('Age Group', '')).strip(),
            gender=str(row.get('Gender', '')).strip(),
            allergies=str(row.get('Allergies (Food/Env)', '')).strip(),
            herbs=list(row.get('ayurvedic_herbs_list', [])),
            remedies=list(row.get('herbal_remedies_list', [])),
            ingredients=list(row.get('ingredient_list', [])),
            severity=str(row.get('Symptom Severity', '')).strip(),
            doshas=str(row.get('Doshas', '')).strip(),
            prakriti=str(row.get('Constitution/Prakriti', '')).strip(),
            search_text=str(row.get('search_text', '')).strip(),
            raw=raw,
        )

    def _build_indexes(self) -> None:
        self.disease_index = defaultdict(list)
        self.token_index = defaultdict(list)
        self.ingredient_frequency = Counter()
        self.ingredient_pairs = Counter()
        for record in self.records:
            disease_key = normalize_text(record.disease)
            self.disease_index[disease_key].append(record.idx)
            for token in set(tokenize(record.search_text)) | set(tokenize(record.disease)) | set(tokenize(record.symptoms)):
                self.token_index[token].append(record.idx)
            for ingredient in unique_preserve_order(record.ingredients + record.herbs + record.remedies):
                self.ingredient_frequency[ingredient] += 1
            ingredients = unique_preserve_order(record.ingredients + record.herbs)
            for pair in combinations(sorted(set(ingredients)), 2):
                self.ingredient_pairs[pair] += 1

    def all_records(self) -> list[RemedyRecord]:
        return list(self.records)

    def search(self, query: str, limit: int = 25) -> list[tuple[RemedyRecord, float]]:
        q = normalize_text(query)
        if not q:
            return [(record, 0.0) for record in self.records[:limit]]
        q_vec = self.vectorizer.transform([q])
        scores = cosine_similarity(q_vec, self.doc_matrix).ravel()
        ranked = np.argsort(scores)[::-1][:limit]
        return [(self.records[i], float(scores[i])) for i in ranked]

    def ingredient_top_n(self, n: int = 10):
        return self.ingredient_frequency.most_common(n)

    def cooccurring_pairs(self, n: int = 10):
        return self.ingredient_pairs.most_common(n)


@lru_cache(maxsize=1)
def get_knowledge_base(path: str | None = None) -> RemedyKnowledgeBase:
    return RemedyKnowledgeBase.from_csv(path)

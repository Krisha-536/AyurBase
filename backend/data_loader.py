from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

from config import DATA_PATH


@lru_cache(maxsize=1)
def load_raw_data(path: str | Path | None = None) -> pd.DataFrame:
    csv_path = Path(path) if path else Path(DATA_PATH)
    if not csv_path.exists():
        raise FileNotFoundError(f'Dataset not found at {csv_path}. Put the CSV in /data or set REMEDY_DATA_PATH.')
    return pd.read_csv(csv_path, encoding='utf-8-sig')


def load_data(path: str | Path | None = None) -> pd.DataFrame:
    df = load_raw_data(path).copy()
    df.columns = [c.strip() for c in df.columns]
    return df

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.schema import validate_games_dataframe

DEFAULT_DATA_PATH = Path("data/sample_games.csv")


def load_games_data(path: str | Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    data_path = Path(path)
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")

    df = pd.read_csv(data_path)
    return validate_games_dataframe(df)

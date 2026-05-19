from __future__ import annotations

from typing import Iterable

import pandas as pd

REQUIRED_COLUMNS: tuple[str, ...] = (
    "game_id",
    "game_name",
    "platform",
    "genre",
    "business_model",
    "avg_session_minutes",
    "daily_task_minutes",
    "payment_entry_points",
    "lootbox_presence",
    "fomo_event_frequency",
    "price_obfuscation",
    "odds_disclosure",
    "parental_control_support",
)

NUMERIC_BOUNDED_COLUMNS: dict[str, tuple[float, float]] = {
    "payment_entry_points": (0, 100),
    "lootbox_presence": (0, 1),
    "fomo_event_frequency": (0, 100),
    "price_obfuscation": (0, 100),
    "odds_disclosure": (0, 100),
    "parental_control_support": (0, 100),
}

POSITIVE_COLUMNS: tuple[str, ...] = (
    "avg_session_minutes",
    "daily_task_minutes",
)


def _missing_columns(columns: Iterable[str]) -> list[str]:
    existing = set(columns)
    return [name for name in REQUIRED_COLUMNS if name not in existing]


def validate_games_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and normalize a game dataframe for MVP use.

    Returns a copy of `df` when valid; raises ValueError on schema issues.
    """
    missing = _missing_columns(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    cleaned = df.copy()

    if cleaned["game_id"].duplicated().any():
        raise ValueError("Column 'game_id' must be unique.")

    for col in ("game_id", "game_name", "platform", "genre", "business_model"):
        if cleaned[col].isna().any() or (cleaned[col].astype(str).str.strip() == "").any():
            raise ValueError(f"Column '{col}' contains empty values.")

    for col in POSITIVE_COLUMNS:
        cleaned[col] = pd.to_numeric(cleaned[col], errors="raise")
        if (cleaned[col] < 0).any():
            raise ValueError(f"Column '{col}' must be >= 0.")

    for col, (min_v, max_v) in NUMERIC_BOUNDED_COLUMNS.items():
        cleaned[col] = pd.to_numeric(cleaned[col], errors="raise")
        if ((cleaned[col] < min_v) | (cleaned[col] > max_v)).any():
            raise ValueError(f"Column '{col}' must be between {min_v} and {max_v}.")

    return cleaned

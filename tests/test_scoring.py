import pandas as pd
import pytest

from src.schema import validate_games_dataframe
from src.scoring import add_risk_scores


def _base_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "game_id": "g1",
                "game_name": "A",
                "platform": "Mobile",
                "genre": "RPG",
                "business_model": "F2P",
                "avg_session_minutes": 30,
                "daily_task_minutes": 60,
                "payment_entry_points": 70,
                "lootbox_presence": 1,
                "fomo_event_frequency": 80,
                "price_obfuscation": 65,
                "odds_disclosure": 50,
                "parental_control_support": 40,
            }
        ]
    )


def test_validate_games_dataframe_passes_on_valid_data():
    df = _base_df()
    validated = validate_games_dataframe(df)
    assert len(validated) == 1


def test_validate_games_dataframe_fails_on_missing_column():
    df = _base_df().drop(columns=["platform"])
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_games_dataframe(df)


def test_validate_games_dataframe_fails_on_out_of_range():
    df = _base_df()
    df.loc[0, "payment_entry_points"] = 120
    with pytest.raises(ValueError, match="between 0 and 100"):
        validate_games_dataframe(df)


def test_add_risk_scores_generates_expected_columns_and_bounds():
    scored = add_risk_scores(_base_df())
    expected_cols = {
        "consumption_pressure_score",
        "time_burden_score",
        "transparency_risk_score",
        "total_risk_score",
        "risk_level",
    }
    assert expected_cols.issubset(scored.columns)
    assert scored["total_risk_score"].between(0, 100).all()
    assert scored.loc[0, "risk_level"] in {"Low", "Medium", "High"}


def test_add_risk_scores_maps_level_boundaries():
    df = pd.concat([_base_df(), _base_df(), _base_df()], ignore_index=True)
    df.loc[0, ["payment_entry_points", "lootbox_presence", "fomo_event_frequency", "price_obfuscation", "daily_task_minutes", "avg_session_minutes", "odds_disclosure", "parental_control_support"]] = [0, 0, 0, 0, 0, 0, 100, 100]
    df.loc[1, ["payment_entry_points", "lootbox_presence", "fomo_event_frequency", "price_obfuscation", "daily_task_minutes", "avg_session_minutes", "odds_disclosure", "parental_control_support"]] = [60, 1, 55, 55, 80, 50, 55, 50]
    df.loc[2, ["payment_entry_points", "lootbox_presence", "fomo_event_frequency", "price_obfuscation", "daily_task_minutes", "avg_session_minutes", "odds_disclosure", "parental_control_support"]] = [100, 1, 100, 100, 180, 120, 0, 0]

    scored = add_risk_scores(df)
    assert scored.loc[0, "risk_level"] == "Low"
    assert scored.loc[2, "risk_level"] == "High"

from __future__ import annotations

import pandas as pd


def _clip_0_100(series: pd.Series) -> pd.Series:
    return series.clip(lower=0, upper=100)


def add_risk_scores(df: pd.DataFrame) -> pd.DataFrame:
    scored = df.copy()

    consumption = (
        0.35 * scored["payment_entry_points"]
        + 0.25 * (scored["lootbox_presence"] * 100)
        + 0.25 * scored["fomo_event_frequency"]
        + 0.15 * scored["price_obfuscation"]
    )

    time_burden = (
        0.55 * (scored["daily_task_minutes"].clip(upper=180) / 180 * 100)
        + 0.30 * (scored["avg_session_minutes"].clip(upper=120) / 120 * 100)
        + 0.15 * scored["fomo_event_frequency"]
    )

    transparency_risk = (
        0.45 * scored["price_obfuscation"]
        + 0.35 * (100 - scored["odds_disclosure"])
        + 0.20 * (100 - scored["parental_control_support"])
    )

    scored["consumption_pressure_score"] = _clip_0_100(consumption).round(2)
    scored["time_burden_score"] = _clip_0_100(time_burden).round(2)
    scored["transparency_risk_score"] = _clip_0_100(transparency_risk).round(2)

    total = (
        0.40 * scored["consumption_pressure_score"]
        + 0.30 * scored["time_burden_score"]
        + 0.30 * scored["transparency_risk_score"]
    )
    scored["total_risk_score"] = _clip_0_100(total).round(2)

    scored["risk_level"] = pd.cut(
        scored["total_risk_score"],
        bins=[-0.01, 33, 66, 100],
        labels=["Low", "Medium", "High"],
        include_lowest=True,
    ).astype(str)

    return scored

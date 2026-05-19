from __future__ import annotations

import altair as alt
import streamlit as st

from src.data_loader import DEFAULT_DATA_PATH, load_games_data
from src.scoring import add_risk_scores

st.set_page_config(page_title="LudoLens MVP", layout="wide")

st.title("🎮 LudoLens MVP")
st.caption("A local prototype for analyzing game monetization pressure, time burden, and transparency risk.")
st.info("This is a heuristic MVP prototype with local sample data. It is not a definitive judgment of any game.")

raw_df = load_games_data(DEFAULT_DATA_PATH)
scored_df = add_risk_scores(raw_df)

st.sidebar.header("Filters")
platforms = st.sidebar.multiselect("Platform", sorted(scored_df["platform"].unique()), default=sorted(scored_df["platform"].unique()))
genres = st.sidebar.multiselect("Genre", sorted(scored_df["genre"].unique()), default=sorted(scored_df["genre"].unique()))
models = st.sidebar.multiselect(
    "Business model",
    sorted(scored_df["business_model"].unique()),
    default=sorted(scored_df["business_model"].unique()),
)

filtered = scored_df[
    scored_df["platform"].isin(platforms)
    & scored_df["genre"].isin(genres)
    & scored_df["business_model"].isin(models)
]

st.subheader("Game Overview")
st.dataframe(
    filtered[
        [
            "game_name",
            "platform",
            "genre",
            "business_model",
            "consumption_pressure_score",
            "time_burden_score",
            "transparency_risk_score",
            "total_risk_score",
            "risk_level",
        ]
    ].sort_values("total_risk_score", ascending=False),
    use_container_width=True,
)

st.subheader("Risk Score Comparison")
chart = (
    alt.Chart(filtered)
    .mark_bar()
    .encode(
        x=alt.X("game_name:N", sort="-y", title="Game"),
        y=alt.Y("total_risk_score:Q", title="Total risk score"),
        color=alt.Color("risk_level:N", title="Risk level"),
        tooltip=["game_name", "total_risk_score", "risk_level"],
    )
    .properties(height=360)
)
st.altair_chart(chart, use_container_width=True)

st.subheader("Single Game Analysis Card")
selected_game = st.selectbox("Choose a game", filtered["game_name"].tolist() if not filtered.empty else [])

if selected_game:
    row = filtered[filtered["game_name"] == selected_game].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Consumption Pressure", f"{row['consumption_pressure_score']}")
    c2.metric("Time Burden", f"{row['time_burden_score']}")
    c3.metric("Transparency Risk", f"{row['transparency_risk_score']}")
    c4.metric("Total Risk", f"{row['total_risk_score']} ({row['risk_level']})")

    st.markdown(
        f"""
**Interpretation hints (MVP):**
- **Monetization pressure** reflects payment entry intensity, lootbox presence, and FOMO events.
- **Time burden** reflects routine task and session-time commitment.
- **Transparency risk** reflects price complexity, low odds disclosure, and weak parental controls.
"""
    )

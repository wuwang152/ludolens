# LudoLens Methodology (MVP v1)

## Data model
Each game includes categorical metadata (platform/genre/business model) and structured indicators (0-100 scale where applicable).

## Risk dimensions

### 1) Consumption Pressure Score
Weighted signals:
- payment_entry_points (35%)
- lootbox_presence (25%; mapped from 0/1 to 0/100)
- fomo_event_frequency (25%)
- price_obfuscation (15%)

### 2) Time Burden Score
Weighted signals:
- daily_task_minutes normalized by cap 180 min (55%)
- avg_session_minutes normalized by cap 120 min (30%)
- fomo_event_frequency (15%)

### 3) Transparency Risk Score
Weighted signals:
- price_obfuscation (45%)
- inverse odds_disclosure i.e., (100 - odds_disclosure) (35%)
- inverse parental_control_support i.e., (100 - parental_control_support) (20%)

## Total score
`total_risk_score = 0.40 * consumption + 0.30 * time + 0.30 * transparency`

All scores are clipped to [0, 100].

## Risk levels
- Low: 0-33
- Medium: 34-66
- High: 67-100

## Limitations
- The model is heuristic and intentionally simple.
- Inputs are sample data rather than externally verified production data.
- Score interpretation should be comparative, not absolute.

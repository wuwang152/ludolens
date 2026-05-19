# AGENTS

## Scope
These instructions apply to the entire repository.

## Project constraints (MVP v1)
- Do **not** add crawlers or scraping pipelines.
- Do **not** add databases or ORM dependencies.
- Do **not** call external APIs.
- Keep the frontend simple: Streamlit only.
- Keep code easy to read and test.

## Coding guidelines
- Prefer pure functions in `src/scoring.py`.
- Keep data validation centralized in `src/schema.py`.
- Raise clear `ValueError` messages for invalid input data.
- Avoid hidden global state.

## Testing guidelines
- All scoring logic changes should have pytest coverage.
- Run `pytest` locally before committing.

## Git workflow
- Do not push directly to `main`.
- Use clear commit messages with scope, e.g. `feat: add MVP scoring pipeline`.

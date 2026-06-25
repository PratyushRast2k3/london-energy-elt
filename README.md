# London Energy ELT

End-to-end ELT pipeline on ~167M UK smart-meter readings, demonstrating both
data engineering and business analytics skills.

**Stack:** Python · PySpark · Snowflake · dbt · Airflow/Dagster · Supabase · Tableau/Power BI

## Architecture
Kaggle raw CSVs -> PySpark (clean -> Parquet) -> Snowflake (RAW) ->
dbt (staging -> marts) -> Supabase (serving) + Tableau (BI), orchestrated and version-controlled.

## Project structure
```
config/         central settings (reads .env)
ingestion/      Phase 1 - download raw data
spark/          Phase 2 - PySpark cleaning -> Parquet
dbt/            Phase 4 - dbt project (init here)
orchestration/  Phase 5 - Airflow/Dagster DAGs
serving/        Phase 6 - reverse-ETL to Supabase
dashboards/     Phase 7 - Tableau/Power BI workbooks
scripts/        utilities (connection test, etc.)
data/           raw/ and curated/ (git-ignored)
docs/           diagrams and notes
```

## Setup
1. `python -m venv venv` and activate it
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and fill in your credentials
4. `python scripts/test_connections.py`

See the project roadmap for the full phase-by-phase guide.

"""Verify every external connection before we start moving data.

Run from the project root:
    python scripts/test_connections.py

It checks Snowflake, Supabase (Postgres) and Kaggle and prints a clear
PASS/FAIL for each. Fix any FAILs (usually a missing value in .env) and re-run.
"""
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from config import settings


def check_snowflake():
    cfg = settings.SNOWFLAKE
    if not cfg["account"]:
        return False, "SNOWFLAKE_ACCOUNT is blank in .env"
    try:
        import snowflake.connector
        conn = snowflake.connector.connect(
            account=cfg["account"], user=cfg["user"], password=cfg["password"],
            role=cfg["role"], warehouse=cfg["warehouse"], login_timeout=15,
        )
        ver = conn.cursor().execute("SELECT CURRENT_VERSION()").fetchone()[0]
        conn.close()
        return True, f"connected (Snowflake {ver})"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def check_supabase():
    cfg = settings.SUPABASE
    if not cfg["host"]:
        return False, "SUPABASE_HOST is blank in .env"
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=cfg["host"], port=cfg["port"], dbname=cfg["dbname"],
            user=cfg["user"], password=cfg["password"], connect_timeout=15,
        )
        cur = conn.cursor()
        cur.execute("SELECT version();")
        v = cur.fetchone()[0].split(" on ")[0]
        conn.close()
        return True, f"connected ({v})"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def check_kaggle():
    has_json = (Path.home() / ".kaggle" / "kaggle.json").exists()
    has_env = bool(os.getenv("KAGGLE_KEY"))
    if not (has_json or has_env):
        return False, "no ~/.kaggle/kaggle.json and no KAGGLE_KEY in .env"
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        return True, "authenticated"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def main():
    checks = [
        ("Snowflake", check_snowflake),
        ("Supabase",  check_supabase),
        ("Kaggle",    check_kaggle),
    ]
    print("\nChecking connections...")
    print("-" * 52)
    all_ok = True
    for name, fn in checks:
        ok, msg = fn()
        print(f"[{'PASS' if ok else 'FAIL'}] {name:10} {msg}")
        all_ok = all_ok and ok
    print("-" * 52)
    print("All connections good - ready for Phase 1!" if all_ok
          else "Fix the FAIL lines above (usually a .env value), then re-run.")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()

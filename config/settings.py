"""Central config loader. Reads .env once and exposes typed dicts."""
import os
from dotenv import load_dotenv

load_dotenv()

SNOWFLAKE = {
    "account":   os.getenv("SNOWFLAKE_ACCOUNT"),
    "user":      os.getenv("SNOWFLAKE_USER"),
    "password":  os.getenv("SNOWFLAKE_PASSWORD"),
    "role":      os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "ENERGY_WH"),
    "database":  os.getenv("SNOWFLAKE_DATABASE", "ENERGY"),
    "schema":    os.getenv("SNOWFLAKE_SCHEMA", "RAW"),
}

SUPABASE = {
    "host":     os.getenv("SUPABASE_HOST"),
    "port":     os.getenv("SUPABASE_PORT", "5432"),
    "dbname":   os.getenv("SUPABASE_DB", "postgres"),
    "user":     os.getenv("SUPABASE_USER", "postgres"),
    "password": os.getenv("SUPABASE_PASSWORD"),
}

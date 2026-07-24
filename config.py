import os

# config.py
# Database connection pulled from Replit-managed environment variables.
# PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD are set automatically.

DB_CONFIG = {
    "host": os.environ.get("PGHOST", "localhost"),
    "port": int(os.environ.get("PGPORT", 5432)),
    "database": os.environ.get("PGDATABASE", "jcrc_chemistry_db"),
    "user": os.environ.get("PGUSER", "postgres"),
    "password": os.environ.get("PGPASSWORD", ""),
}

ARCHIVE_FOLDER = "archive/incoming"
PROCESSED_FOLDER = "archive/processed"
FAILED_FOLDER = "archive/failed"
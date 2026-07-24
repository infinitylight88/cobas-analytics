# Cobas Analytics

A laboratory analytics platform for the **Roche Cobas Integra 400 Plus Clinical Chemistry Analyzer**.

Imports monthly archive files from the analyzer, parses every record, stores normalized data in PostgreSQL, and exposes the data through a FastAPI REST API.

## How to run

The FastAPI backend starts automatically via the **Start application** workflow:

```
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive API docs are available at `/docs` (Swagger UI) and `/redoc`.

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13+ |
| Database | PostgreSQL (Replit managed) |
| ORM | SQLAlchemy 2.x |
| API | FastAPI + Uvicorn |
| Desktop UI (planned) | PySide6 (Qt) |

## Database

Replit's managed PostgreSQL is used. Connection is configured automatically via the `DATABASE_URL`, `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, and `PGDATABASE` environment variables — **no manual credentials needed**.

The original database can be restored from a `.dump` or `.sql` backup file:

```bash
# For a custom-format pg_dump backup:
pg_restore --no-owner -d "$DATABASE_URL" your_backup.dump

# For a plain SQL backup:
psql "$DATABASE_URL" < your_backup.sql
```

Upload the backup file via the Replit file explorer (drag & drop into the file tree), then run the restore command above in the Shell tab.

## Project layout

```
api/            FastAPI app — routers, services, schemas, SQLAlchemy models
database/       Parser-side writers and DB utilities
parser/         Cobas archive file parser
dashboard/      PySide6 desktop dashboard (future)
main.py         CLI entry point for importing a single archive file
config.py       DB config (reads from environment variables)
```

## Importing an archive file

```bash
python main.py
```

Edit `ARCHIVE_FILE` in `main.py` to point to the archive you want to import.

## User preferences

- Keep the existing project structure and stack.
- API first, then UI.
- Use SQLAlchemy ORM; avoid raw SQL in the API layer.
- Keep routers thin; business logic lives in services.

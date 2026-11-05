"""Shared PostgreSQL settings, read from environment variables (or a .env file).

Variables: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST,
POSTGRES_PORT, or a full DATABASE_URL for the Flask app.
"""
import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


def pg_connect_kwargs(dbname=None):
    """Keyword arguments for psycopg2.connect()."""
    return {
        "dbname": dbname or os.getenv("POSTGRES_DB", "movie_rating_system"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", ""),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
    }


def database_url():
    """SQLAlchemy URL: DATABASE_URL if set, else built from POSTGRES_* vars."""
    url = os.getenv("DATABASE_URL")
    if url:
        return url
    c = pg_connect_kwargs()
    return "postgresql://{u}:{p}@{h}:{port}/{d}".format(
        u=quote_plus(c["user"]), p=quote_plus(c["password"]),
        h=c["host"], port=c["port"], d=c["dbname"])

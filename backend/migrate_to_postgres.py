import sqlite3
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from datetime import datetime

# SQLite connection
sqlite_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'movies.db')
sqlite_conn = sqlite3.connect(sqlite_db_path)
sqlite_cursor = sqlite_conn.cursor()

# PostgreSQL connection
pg_conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="129141",
    host="localhost",
    port="5432"
)
pg_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
pg_cursor = pg_conn.cursor()

# Create new database
try:
    pg_cursor.execute("DROP DATABASE IF EXISTS movie_rating_system")
    pg_cursor.execute("CREATE DATABASE movie_rating_system")
except Exception as e:
    print(f"Error creating database: {e}")

# Close initial connection and connect to new database
pg_conn.close()
pg_conn = psycopg2.connect(
    dbname="movie_rating_system",
    user="postgres",
    password="129141",
    host="localhost",
    port="5432"
)
pg_cursor = pg_conn.cursor()

# Create tables in PostgreSQL
pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
)
""")

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    language VARCHAR(50),
    release_year INTEGER,
    imdb_rating FLOAT,
    poster_url TEXT,
    synopsis TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    budget_crores FLOAT,
    gross_crores FLOAT,
    film_image_url TEXT
)
""")

pg_cursor.execute("""
CREATE TABLE IF NOT EXISTS watchlist (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    movie_id INTEGER REFERENCES movies(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Migrate users
sqlite_cursor.execute("SELECT id, username, email, password_hash, created_at, last_login FROM users")
users = sqlite_cursor.fetchall()
for user in users:
    pg_cursor.execute("""
    INSERT INTO users (id, username, email, password_hash, created_at, last_login)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, user)

# Migrate movies
sqlite_cursor.execute("SELECT id, title, genre, language, release_year, imdb_rating, poster_url, synopsis, created_at, budget_crores, gross_crores, film_image_url FROM movies")
movies = sqlite_cursor.fetchall()
for movie in movies:
    pg_cursor.execute("""
    INSERT INTO movies (id, title, genre, language, release_year, imdb_rating, poster_url, synopsis, created_at, budget_crores, gross_crores, film_image_url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, movie)

# Migrate watchlist
sqlite_cursor.execute("SELECT id, user_id, movie_id, created_at FROM watchlist")
watchlist_items = sqlite_cursor.fetchall()
for item in watchlist_items:
    pg_cursor.execute("""
    INSERT INTO watchlist (id, user_id, movie_id, created_at)
    VALUES (%s, %s, %s, %s)
    """, item)

# Reset sequences
pg_cursor.execute("SELECT setval('users_id_seq', (SELECT MAX(id) FROM users))")
pg_cursor.execute("SELECT setval('movies_id_seq', (SELECT MAX(id) FROM movies))")
pg_cursor.execute("SELECT setval('watchlist_id_seq', (SELECT MAX(id) FROM watchlist))")

# Commit changes and close connections
pg_conn.commit()
sqlite_conn.close()
pg_conn.close()

print("Migration completed successfully!")
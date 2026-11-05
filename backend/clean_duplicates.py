import psycopg2
from db_config import pg_connect_kwargs

# Connect to PostgreSQL
conn = psycopg2.connect(**pg_connect_kwargs("movie_rating_system"))
cur = conn.cursor()

# Delete duplicate movies, keeping only one copy with the lowest ID
cur.execute("""
WITH duplicates AS (
    SELECT id, title,
           ROW_NUMBER() OVER (PARTITION BY title ORDER BY id) as row_num
    FROM movies
)
DELETE FROM movies
WHERE id IN (
    SELECT id 
    FROM duplicates 
    WHERE row_num > 1
);
""")

print("Deleted duplicate movies")

# Show remaining movies
cur.execute("""
SELECT id, title, release_year, imdb_rating
FROM movies
ORDER BY id;
""")
movies = cur.fetchall()
print("\n=== REMAINING MOVIES ===")
for movie in movies:
    print(f"ID: {movie[0]}, Title: {movie[1]}, Year: {movie[2]}, Rating: {movie[3]}")

conn.commit()
cur.close()
conn.close()
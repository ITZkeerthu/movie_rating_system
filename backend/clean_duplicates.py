import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="movie_rating_system",
    user="postgres",
    password="129141",
    host="localhost",
    port="5432"
)
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
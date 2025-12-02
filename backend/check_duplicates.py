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

# Count movies and check for duplicates
cur.execute("""
SELECT title, COUNT(*) as count
FROM movies
GROUP BY title
HAVING COUNT(*) > 1
ORDER BY count DESC;
""")
duplicates = cur.fetchall()
print("\n=== DUPLICATE MOVIES ===")
if duplicates:
    for dup in duplicates:
        print(f"Movie: {dup[0]} appears {dup[1]} times")
else:
    print("No duplicate movies found")

# Show all movies for verification
print("\n=== ALL MOVIES ===")
cur.execute("""
SELECT id, title, release_year, imdb_rating
FROM movies
ORDER BY id;
""")
movies = cur.fetchall()
for movie in movies:
    print(f"ID: {movie[0]}, Title: {movie[1]}, Year: {movie[2]}, Rating: {movie[3]}")

cur.close()
conn.close()
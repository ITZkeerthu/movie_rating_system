import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="movie_rating_system",
    user="postgres",
    password="129141",
    host="localhost",
    port="5432"
)

def print_query_results(cursor, query, title):
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows:
        print(f"\n=== {title} ===")
        print(tabulate(rows, headers=[desc[0] for desc in cursor.description], tablefmt="grid"))
        print(f"Total rows: {len(rows)}\n")
    else:
        print(f"\nNo data found in {title}")

try:
    # Connect to PostgreSQL
    conn = connect_to_db()
    cur = conn.cursor(cursor_factory=DictCursor)
    
    # Movies Query
    movies_query = """
    SELECT id, title, genre, language, release_year, imdb_rating, budget_crores, gross_crores 
    FROM movies 
    ORDER BY imdb_rating DESC;
    """
    print_query_results(cur, movies_query, "MOVIES")
    
    # Users Query
    users_query = """
    SELECT id, username, email, created_at, last_login 
    FROM users 
    ORDER BY created_at;
    """
    print_query_results(cur, users_query, "USERS")
    
    # Watchlist Query with movie titles
    watchlist_query = """
    SELECT w.id, u.username, m.title, w.created_at
    FROM watchlist w
    JOIN users u ON w.user_id = u.id
    JOIN movies m ON w.movie_id = m.id
    ORDER BY w.created_at;
    """
    print_query_results(cur, watchlist_query, "WATCHLIST")

except Exception as e:
    print(f"Error: {e}")
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
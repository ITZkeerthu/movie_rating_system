import psycopg2
from psycopg2.extras import RealDictCursor

def print_table_data(cursor, table_name):
    print(f"\n=== {table_name.upper()} TABLE ===")
    
    # Get column names
    cursor.execute(f"""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = '{table_name}'
    """)
    columns = cursor.fetchall()
    print("Columns:", ", ".join([f"{col[0]} ({col[1]})" for col in columns]))
    
    # Get all data
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    print(f"\nTotal rows: {len(rows)}")
    print("\nData:")
    for row in cursor.fetchall():
        print("-" * 80)
        for key, value in row.items():
            print(f"{key}: {value}")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="movie_rating_system",
    user="postgres",
    password="129141",
    host="localhost",
    port="5432",
    cursor_factory=RealDictCursor
)
cursor = conn.cursor()

# Get all tables
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
""")
tables = cursor.fetchall()

for table in tables:
    print_table_data(cursor, table['table_name'])

conn.close()
print("\nVerification completed!")
import sqlite3
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'movies.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

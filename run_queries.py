import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import app
from backend.models import db

def run_queries():
    with app.app_context():
        # Query 1: All movies
        print("\n=== All Movies ===")
        result = db.session.execute("""
            SELECT 
                title AS "Movie Title",
                release_year AS "Year",
                genre AS "Genre",
                imdb_rating AS "IMDb Rating",
                film_image_url AS "Poster URL",
                language AS "Language",
                synopsis AS "Synopsis"
            FROM movies 
            ORDER BY imdb_rating DESC
        """)
        
        for row in result:
            print("\nMovie:", row["Movie Title"])
            print("Year:", row["Year"])
            print("Genre:", row["Genre"])
            print("Rating:", row["IMDb Rating"])
            print("Language:", row["Language"])
            print("-" * 50)

        # Query 2: The Dark Knight details
        print("\n=== The Dark Knight Details ===")
        result = db.session.execute("""
            SELECT 
                title AS "Movie Title",
                release_year AS "Year",
                genre AS "Genre",
                imdb_rating AS "IMDb Rating",
                film_image_url AS "Poster URL",
                language AS "Language",
                synopsis AS "Synopsis"
            FROM movies 
            WHERE title LIKE '%Dark Knight%'
        """)
        
        for row in result:
            print("\nMovie:", row["Movie Title"])
            print("Year:", row["Year"])
            print("Genre:", row["Genre"])
            print("Rating:", row["IMDb Rating"])
            print("Language:", row["Language"])
            print("\nSynopsis:", row["Synopsis"])
            print("-" * 50)

if __name__ == "__main__":
    run_queries()
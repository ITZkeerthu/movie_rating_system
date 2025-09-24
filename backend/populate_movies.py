#!/usr/bin/env python3
"""
Script to populate the movies database with sample movie data
including proper image URLs for poster display.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Movie

def populate_movies():
    """Populate the database with sample movie data"""
    
    # Sample movie data with real poster image URLs
    sample_movies = [
        {
            'title': 'RRR',
            'genre': 'Action/Drama',
            'language': 'Telugu',
            'release_year': 2022,
            'imdb_rating': 7.9,
            'budget_crores': 550.0,
            'gross_crores': 1200.0,
            'film_image_url': 'https://m.media-amazon.com/images/M/MV5BODUwNDNjYzctODUxNy00ZTA2LWIyYTEtMDc5Y2E5ZjBmNTMzXkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_SX300.jpg',
            'synopsis': 'A fictional story about two legendary revolutionaries and their journey away from home before they started fighting for their country in the 1920s.'
        },
        {
            'title': 'Baahubali 2: The Conclusion',
            'genre': 'Action/Drama',
            'language': 'Telugu',
            'release_year': 2017,
            'imdb_rating': 8.2,
            'budget_crores': 250.0,
            'gross_crores': 1810.0,
            'film_image_url': 'https://m.media-amazon.com/images/M/MV5BYTMxMGM2NjMtYjBhNi00MjNjLWExMDQtNGJiMmNhMTY4OTI3XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SX300.jpg',
            'synopsis': 'When Shiva, the son of Bahubali, learns about his heritage, he begins to look for answers. His story is juxtaposed with past events that unfolded in the Mahishmati Kingdom.'
        },
        {
            'title': 'Dangal',
            'genre': 'Biography/Drama',
            'language': 'Hindi',
            'release_year': 2016,
            'imdb_rating': 8.4,
            'budget_crores': 70.0,
            'gross_crores': 2024.0,
            'film_image_url': 'https://m.media-amazon.com/images/M/MV5BMTQ4MzQzMzM2Nl5BMl5BanBnXkFtZTgwMTQ1NzU3MDI@._V1_SX300.jpg',
            'synopsis': 'Former wrestler Mahavir Singh Phogat and his two wrestler daughters struggle towards glory at the Commonwealth Games in the face of societal oppression.'
        },
        {
            'title': 'The Dark Knight',
            'genre': 'Action/Crime',
            'language': 'English',
            'release_year': 2008,
            'imdb_rating': 9.0,
            'budget_crores': 185.0,
            'gross_crores': 1004.0,
            'film_image_url': 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_SX300.jpg',
            'synopsis': 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.'
        },
        {
            'title': 'Inception',
            'genre': 'Action/Sci-Fi',
            'language': 'English',
            'release_year': 2010,
            'imdb_rating': 8.8,
            'budget_crores': 160.0,
            'gross_crores': 836.0,
            'film_image_url': 'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_SX300.jpg',
            'synopsis': 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.'
        },
        {
            'title': '3 Idiots',
            'genre': 'Comedy/Drama',
            'language': 'Hindi',
            'release_year': 2009,
            'imdb_rating': 8.4,
            'budget_crores': 55.0,
            'gross_crores': 460.0,
            'film_image_url': 'https://m.media-amazon.com/images/M/MV5BNTkyOGVjMGEtNmQzZi00NzFlLTlhOWQtODYyMDc2ZGJmYzFhXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg',
            'synopsis': 'Two friends are searching for their long lost companion. They revisit their college days and recall the memories of their friend who inspired them to think differently, even as the rest of the world called them "idiots".'
        },
        {
            'title': 'Avengers: Endgame',
            'genre': 'Action/Adventure',
            'language': 'English',
            'release_year': 2019,
            'imdb_rating': 8.4,
            'budget_crores': 356.0,
            'gross_crores': 2798.0,
            'film_image_url': 'https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg',
            'synopsis': 'After the devastating events of Avengers: Infinity War, the universe is in ruins. With the help of remaining allies, the Avengers assemble once more in order to reverse Thanos\' actions and restore balance to the universe.'
        },
        {
            'title': 'Zindagi Na Milegi Dobara',
            'genre': 'Adventure/Comedy',
            'language': 'Hindi',
            'release_year': 2011,
            'imdb_rating': 8.2,
            'budget_crores': 55.0,
            'gross_crores': 153.0,
            'film_image_url': 'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxNS00OWM2LTgzN2YtMmU4MzgxZjVlZmY3XkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_SX300.jpg',
            'synopsis': 'Three friends decide to turn their fantasy vacation into reality after one of their friends gets engaged.'
        },
        {
            'title': 'Sholay',
            'genre': 'Action/Adventure',
            'language': 'Hindi',
            'release_year': 1975,
            'imdb_rating': 8.2,
            'budget_crores': 3.0,
            'gross_crores': 150.0,
            'film_image_url': 'https://m.media-amazon.com/images/M/MV5BYjhkMTlkNTctZWU0Mi00YTMyLWFkYjItMjBhZmNmNGY4MmRiXkEyXkFqcGdeQXVyNTE0MDc0NTM@._V1_SX300.jpg',
            'synopsis': 'After his family is murdered by a notorious and ruthless bandit, a former police officer enlists the services of two outlaws to capture the bandit.'
        },
        {
            'title': 'Parasite',
            'genre': 'Comedy/Drama',
            'language': 'Korean',
            'release_year': 2019,
            'imdb_rating': 8.5,
            'budget_crores': 11.4,
            'gross_crores': 258.8,
            'film_image_url': 'https://m.media-amazon.com/images/M/MV5BYWZjMjk3ZTItODQ2ZC00NTY5LWE0ZDYtZTI3MjcwN2Q5NTVkXkEyXkFqcGdeQXVyODk4OTc3MTY@._V1_SX300.jpg',
            'synopsis': 'A poor family, the Kims, con their way into becoming the servants of a rich family, the Parks. But their easy life gets complicated when their deception is threatened with exposure.'
        }
    ]
    
    with app.app_context():
        # Create all tables with new schema
        db.create_all()
        
        # Clear existing movies if any
        Movie.query.delete()
        db.session.commit()
        
        # Add sample movies
        for movie_data in sample_movies:
            movie = Movie(**movie_data)
            db.session.add(movie)
        
        # Commit all changes
        db.session.commit()
        
        print(f"✅ Successfully added {len(sample_movies)} movies to the database!")
        
        # Verify the data
        total_movies = Movie.query.count()
        print(f"📊 Total movies in database: {total_movies}")
        
        # Show some sample data
        print("\n🎬 Sample movies added:")
        for movie in Movie.query.limit(3).all():
            print(f"  • {movie.title} ({movie.release_year}) - Rating: {movie.imdb_rating}")

if __name__ == '__main__':
    populate_movies()
#!/usr/bin/env python3
"""
Simple test script to verify API endpoints are working correctly
"""

from app import app

def test_movies_api():
    """Test the movies API endpoints"""
    with app.test_client() as client:
        print('=== Testing Movies API ===')
        
        # Test movies list endpoint
        response = client.get('/movies')
        print(f'Movies endpoint status: {response.status_code}')
        
        if response.status_code == 200:
            movies = response.get_json()
            print(f'Total movies returned: {len(movies)}')
            
            if movies:
                sample_movie = movies[0]
                print('\nSample movie data:')
                print(f'  Title: {sample_movie.get("title")}')
                print(f'  Year: {sample_movie.get("release_year")}')
                print(f'  Genre: {sample_movie.get("genre")}')
                print(f'  IMDb Rating: {sample_movie.get("imdb_rating")}')
                print(f'  Budget: Rs.{sample_movie.get("budget_crores")}Cr')
                print(f'  Gross: Rs.{sample_movie.get("gross_crores")}Cr')
                
                image_url = sample_movie.get('film_image_url', 'N/A')
                if len(image_url) > 60:
                    image_url = image_url[:60] + '...'
                print(f'  Image URL: {image_url}')
                
                # Test individual movie endpoint
                movie_id = sample_movie.get('id')
                detail_response = client.get(f'/movies/{movie_id}')
                print(f'\nMovie detail endpoint status: {detail_response.status_code}')
                
                if detail_response.status_code == 200:
                    movie_detail = detail_response.get_json()
                    print(f'Movie detail title: {movie_detail.get("title")}')
                    print(f'Synopsis available: {bool(movie_detail.get("synopsis"))}')
                    print('✅ API endpoints working correctly!')
                else:
                    print('❌ Movie detail endpoint error')
            else:
                print('❌ No movies found')
        else:
            error_data = response.get_data(as_text=True)
            print(f'❌ Movies endpoint error: {error_data}')

if __name__ == '__main__':
    test_movies_api()
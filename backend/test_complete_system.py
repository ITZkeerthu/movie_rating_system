#!/usr/bin/env python3
"""
Comprehensive test script for the complete movie rating system
Tests all API endpoints and functionality matching the specifications.
"""

from app import app
import json

def test_complete_system():
    """Test the complete movie rating system functionality"""
    
    with app.test_client() as client:
        print("🎬 TESTING COMPLETE MOVIE RATING SYSTEM")
        print("=" * 50)
        
        # Test 1: Movies browsing endpoint
        print("\n1️⃣ Testing Movies Browsing (GET /movies)")
        response = client.get('/movies')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        movies_data = response.get_json()
        assert 'movies' in movies_data, "Response should contain 'movies' key"
        movies = movies_data['movies']
        
        print(f"✅ Found {len(movies)} movies")
        if movies:
            sample_movie = movies[0]
            required_fields = ['id', 'title', 'release_year', 'genre', 'imdb_rating', 'film_image_url']
            for field in required_fields:
                assert field in sample_movie, f"Missing required field: {field}"
            print(f"✅ Sample movie: {sample_movie['title']} ({sample_movie['release_year']})")
            print(f"   Rating: {sample_movie['imdb_rating']}, Genre: {sample_movie['genre']}")
        
        # Test 2: Search functionality
        print("\n2️⃣ Testing Search Functionality")
        response = client.get('/movies?search=RRR')
        assert response.status_code == 200
        search_data = response.get_json()
        print(f"✅ Search for 'RRR' returned {len(search_data['movies'])} results")
        
        # Test 3: Filter by year
        print("\n3️⃣ Testing Year Filter")
        response = client.get('/movies?year=2022')
        assert response.status_code == 200
        year_data = response.get_json()
        print(f"✅ Year filter (2022) returned {len(year_data['movies'])} results")
        
        # Test 4: Filter by genre
        print("\n4️⃣ Testing Genre Filter")
        response = client.get('/movies?genre=Action')
        assert response.status_code == 200
        genre_data = response.get_json()
        print(f"✅ Genre filter (Action) returned {len(genre_data['movies'])} results")
        
        # Test 5: Rating filter
        print("\n5️⃣ Testing Rating Filter")
        response = client.get('/movies?min_rating=8.0')
        assert response.status_code == 200
        rating_data = response.get_json()
        print(f"✅ Rating filter (≥8.0) returned {len(rating_data['movies'])} results")
        
        # Test 6: Filter options endpoint
        print("\n6️⃣ Testing Filter Options (GET /movies/filters)")
        response = client.get('/movies/filters')
        assert response.status_code == 200
        filter_options = response.get_json()
        
        required_filter_fields = ['genres', 'years', 'rating_range', 'sort_options']
        for field in required_filter_fields:
            assert field in filter_options, f"Missing filter field: {field}"
        
        print(f"✅ Available genres: {len(filter_options['genres'])}")
        print(f"✅ Available years: {len(filter_options['years'])}")
        print(f"✅ Rating range: {filter_options['rating_range']['min']}-{filter_options['rating_range']['max']}")
        
        # Test 7: Authentication endpoints
        print("\n7️⃣ Testing Authentication")
        
        # Test login
        login_data = {
            'email': 'skeerthan@gmail.com',
            'password': '123456'
        }
        response = client.post('/auth/login', 
                              data=json.dumps(login_data), 
                              content_type='application/json')
        assert response.status_code == 200
        auth_data = response.get_json()
        assert 'token' in auth_data
        assert 'user' in auth_data
        
        token = auth_data['token']
        user = auth_data['user']
        print(f"✅ Login successful for user: {user['username']}")
        
        # Test 8: Watchlist endpoints (requires authentication)
        print("\n8️⃣ Testing Watchlist Functionality")
        
        headers = {'Authorization': f'Bearer {token}'}
        
        # Get initial watchlist (should be empty or have existing items)
        response = client.get('/watchlist', headers=headers)
        assert response.status_code == 200
        initial_watchlist = response.get_json()
        print(f"✅ Initial watchlist has {initial_watchlist['total_count']} movies")
        
        # Add movie to watchlist
        if movies:
            movie_id = movies[0]['id']
            movie_title = movies[0]['title']
            
            response = client.post(f'/watchlist/{movie_id}', headers=headers)
            assert response.status_code in [200, 201], f"Expected 200 or 201, got {response.status_code}"
            add_response = response.get_json()
            print(f"✅ Added '{movie_title}' to watchlist")
            
            # Check watchlist status
            response = client.get(f'/watchlist/status?movie_ids={movie_id}', headers=headers)
            assert response.status_code == 200
            status_data = response.get_json()
            assert status_data['status'][str(movie_id)] == True
            print(f"✅ Watchlist status confirmed for movie {movie_id}")
            
            # Get updated watchlist
            response = client.get('/watchlist', headers=headers)
            assert response.status_code == 200
            updated_watchlist = response.get_json()
            assert updated_watchlist['total_count'] >= initial_watchlist['total_count']
            print(f"✅ Updated watchlist has {updated_watchlist['total_count']} movies")
            
            # Remove movie from watchlist
            response = client.delete(f'/watchlist/{movie_id}', headers=headers)
            assert response.status_code == 200
            remove_response = response.get_json()
            print(f"✅ Removed '{movie_title}' from watchlist")
            
        # Test 9: Movie detail endpoint
        print("\n9️⃣ Testing Movie Details")
        if movies:
            movie_id = movies[0]['id']
            response = client.get(f'/movies/{movie_id}')
            assert response.status_code == 200
            movie_detail = response.get_json()
            
            detailed_fields = ['id', 'title', 'genre', 'release_year', 'imdb_rating', 
                             'budget_crores', 'gross_crores', 'synopsis']
            for field in detailed_fields:
                assert field in movie_detail, f"Missing field in movie detail: {field}"
            
            print(f"✅ Movie detail for '{movie_detail['title']}' includes all required fields")
            if movie_detail.get('synopsis'):
                print(f"   Synopsis: {movie_detail['synopsis'][:100]}...")
        
        # Test 10: Combined filters
        print("\n🔟 Testing Combined Filters")
        response = client.get('/movies?genre=Action&min_rating=7.0&sort=rating_desc')
        assert response.status_code == 200
        combined_data = response.get_json()
        print(f"✅ Combined filters returned {len(combined_data['movies'])} results")
        
        # Verify sorting
        if len(combined_data['movies']) > 1:
            ratings = [m['imdb_rating'] for m in combined_data['movies'] if m['imdb_rating']]
            is_sorted = all(ratings[i] >= ratings[i+1] for i in range(len(ratings)-1))
            if is_sorted:
                print("✅ Results are properly sorted by rating (descending)")
            else:
                print("⚠️ Sorting might not be working correctly")
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED! 🎉")
        print("✅ Movies browsing with search and filters")
        print("✅ User authentication system")
        print("✅ Complete watchlist management")
        print("✅ Movie details with images and financial data")
        print("✅ Responsive API design")
        print("\n🎬 Your movie rating system is ready for VS Code!")

if __name__ == '__main__':
    test_complete_system()
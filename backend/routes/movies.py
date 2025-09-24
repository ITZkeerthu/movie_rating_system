from flask import Blueprint, request, jsonify
from sqlalchemy import func

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Movie, db


movies_bp = Blueprint("movies", __name__)


@movies_bp.get("")
def list_movies():
    """GET /movies - Browse movies with search and filter options
    
    Query parameters:
    - search: Search movie titles (Film)
    - year: Filter by release year (Year) 
    - genre: Filter by genre (Genre)
    - min_rating: Minimum IMDb rating (IMDb Rating)
    - max_rating: Maximum IMDb rating (IMDb Rating)
    - sort: Sort order (rating_desc, rating_asc, year_desc, year_asc, title_asc)
    - limit: Number of results (default 60)
    """
    
    # Get query parameters
    search = request.args.get("search", "").strip()
    year = request.args.get("year", type=int)
    genre = request.args.get("genre", "").strip()
    min_rating = request.args.get("min_rating", type=float)
    max_rating = request.args.get("max_rating", type=float)
    sort = request.args.get("sort", "rating_desc")
    limit = request.args.get("limit", 60, type=int)
    
    # Build query
    query = Movie.query
    
    # Apply filters
    if search:
        # Search in movie title (Film)
        query = query.filter(Movie.title.ilike(f"%{search}%"))
    
    if year:
        # Filter by release year (Year)
        query = query.filter(Movie.release_year == year)
    
    if genre:
        # Filter by genre (Genre)
        query = query.filter(Movie.genre.ilike(f"%{genre}%"))
    
    if min_rating is not None:
        # Filter by minimum IMDb rating
        query = query.filter(Movie.imdb_rating >= min_rating)
    
    if max_rating is not None:
        # Filter by maximum IMDb rating
        query = query.filter(Movie.imdb_rating <= max_rating)
    
    # Apply sorting
    if sort == "rating_desc":
        query = query.order_by(Movie.imdb_rating.desc())
    elif sort == "rating_asc":
        query = query.order_by(Movie.imdb_rating.asc())
    elif sort == "year_desc":
        query = query.order_by(Movie.release_year.desc())
    elif sort == "year_asc":
        query = query.order_by(Movie.release_year.asc())
    elif sort == "title_asc":
        query = query.order_by(Movie.title.asc())
    else:
        # Default to rating descending
        query = query.order_by(Movie.imdb_rating.desc())
    
    # Execute query with limit
    movies = query.limit(limit).all()
    
    # Convert to response format
    movies_data = [movie.to_dict() for movie in movies]
    
    return jsonify({
        "movies": movies_data,
        "total_count": len(movies_data),
        "filters_applied": {
            "search": search,
            "year": year,
            "genre": genre,
            "min_rating": min_rating,
            "max_rating": max_rating,
            "sort": sort
        }
    })


@movies_bp.get("/filters")
def get_filter_options():
    """GET /movies/filters - Get available filter options"""
    
    # Get unique genres
    genres_query = db.session.query(Movie.genre).filter(Movie.genre.isnot(None)).distinct().all()
    genres = sorted([genre[0] for genre in genres_query if genre[0]])
    
    # Get available years
    years_query = db.session.query(Movie.release_year).filter(Movie.release_year.isnot(None)).distinct().all()
    years = sorted([year[0] for year in years_query if year[0]], reverse=True)
    
    # Get rating range
    rating_stats = db.session.query(
        func.min(Movie.imdb_rating),
        func.max(Movie.imdb_rating)
    ).filter(Movie.imdb_rating.isnot(None)).first()
    
    min_rating = rating_stats[0] or 0.0
    max_rating = rating_stats[1] or 10.0
    
    return jsonify({
        "genres": genres,
        "years": years,
        "rating_range": {
            "min": round(min_rating, 1),
            "max": round(max_rating, 1)
        },
        "sort_options": [
            {"value": "rating_desc", "label": "Rating: High to Low"},
            {"value": "rating_asc", "label": "Rating: Low to High"},
            {"value": "year_desc", "label": "Year: Newest First"},
            {"value": "year_asc", "label": "Year: Oldest First"},
            {"value": "title_asc", "label": "Title: A to Z"}
        ]
    })


@movies_bp.get("/<int:movie_id>")
def get_movie(movie_id: int):
    m = Movie.query.get_or_404(movie_id)
    return jsonify(
        {
            "id": m.id,
            "title": m.title,
            "genre": m.genre,
            "language": m.language,
            "release_year": m.release_year,
            "imdb_rating": m.imdb_rating,
            "budget_crores": m.budget_crores,
            "gross_crores": m.gross_crores,
            "poster_url": m.film_image_url or m.poster_url,
            "film_image_url": m.film_image_url,
            "synopsis": m.synopsis,
        }
    )



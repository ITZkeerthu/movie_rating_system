from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extensions import db
from models import Watchlist, Movie


watchlist_bp = Blueprint("watchlist", __name__)


@watchlist_bp.get("")
@jwt_required()
def get_watchlist():
    """GET /watchlist - Get user's watchlist with complete movie data"""
    user_id = int(get_jwt_identity())
    
    # Get all movies in user's watchlist
    watchlist_items = (
        Watchlist.query.filter_by(user_id=user_id)
        .join(Movie, Watchlist.movie_id == Movie.id)
        .all()
    )
    
    movies_data = []
    for item in watchlist_items:
        movie_data = item.movie.to_dict()
        movie_data['added_to_watchlist'] = item.created_at.isoformat() if item.created_at else None
        movie_data['in_watchlist'] = True  # Flag for frontend
        movies_data.append(movie_data)
    
    return jsonify({
        "watchlist": movies_data,
        "total_count": len(movies_data)
    })


@watchlist_bp.post("/<int:movie_id>")
@jwt_required()
def add_movie_to_watchlist(movie_id):
    """POST /watchlist/{movie_id} - Add movie to user's watchlist"""
    user_id = int(get_jwt_identity())
    
    # Check if movie exists
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({
            "success": False,
            "message": "Movie not found"
        }), 404
    
    # Check if already in watchlist
    existing_item = Watchlist.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if existing_item:
        return jsonify({
            "success": False,
            "message": "Movie already in watchlist",
            "in_watchlist": True
        }), 200
    
    # Add to watchlist
    watchlist_item = Watchlist(user_id=user_id, movie_id=movie_id)
    db.session.add(watchlist_item)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": f"'{movie.title}' added to watchlist",
        "in_watchlist": True,
        "movie": movie.to_dict()
    }), 201


@watchlist_bp.delete("/<int:movie_id>")
@jwt_required()
def remove_movie_from_watchlist(movie_id):
    """DELETE /watchlist/{movie_id} - Remove movie from user's watchlist"""
    user_id = int(get_jwt_identity())
    
    # Check if movie exists
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({
            "success": False,
            "message": "Movie not found"
        }), 404
    
    # Find watchlist item
    watchlist_item = Watchlist.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if not watchlist_item:
        return jsonify({
            "success": False,
            "message": "Movie not in watchlist",
            "in_watchlist": False
        }), 404
    
    # Remove from watchlist
    db.session.delete(watchlist_item)
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": f"'{movie.title}' removed from watchlist",
        "in_watchlist": False,
        "movie": movie.to_dict()
    }), 200


@watchlist_bp.get("/status")
@jwt_required()
def get_watchlist_status():
    """GET /watchlist/status?movie_ids=1,2,3 - Check watchlist status for multiple movies"""
    user_id = get_jwt_identity()
    movie_ids_param = request.args.get('movie_ids', '')
    
    if not movie_ids_param:
        return jsonify({"status": {}}), 200
    
    try:
        movie_ids = [int(id.strip()) for id in movie_ids_param.split(',') if id.strip()]
    except ValueError:
        return jsonify({"error": "Invalid movie_ids format"}), 400
    
    # Get watchlist status for requested movies
    watchlist_items = Watchlist.query.filter(
        Watchlist.user_id == user_id,
        Watchlist.movie_id.in_(movie_ids)
    ).all()
    
    # Create status dictionary
    status = {movie_id: False for movie_id in movie_ids}
    for item in watchlist_items:
        status[item.movie_id] = True
    
    return jsonify({"status": status})



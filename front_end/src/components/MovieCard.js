import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import './MovieCard.css';

const MovieCard = ({ movie, initialInWatchlist = false, onWatchlistChange }) => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [inWatchlist, setInWatchlist] = useState(initialInWatchlist);
  const [isLoading, setIsLoading] = useState(false);
  const [imgError, setImgError] = useState(false);

  const handleMovieClick = () => {
    navigate(`/movie/${movie.id}`);
  };

  const handleWatchlistToggle = async (e) => {
    e.stopPropagation(); // Prevent movie click when clicking watchlist button
    
    if (!user) {
      navigate('/login');
      return;
    }

    setIsLoading(true);
    
    try {
      if (inWatchlist) {
        // Remove from watchlist
        const response = await axios.delete(`/watchlist/${movie.id}`);
        if (response.data.success) {
          setInWatchlist(false);
          onWatchlistChange && onWatchlistChange(movie.id, false);
        }
      } else {
        // Add to watchlist
        const response = await axios.post(`/watchlist/${movie.id}`);
        if (response.data.success) {
          setInWatchlist(true);
          onWatchlistChange && onWatchlistChange(movie.id, true);
        }
      }
    } catch (error) {
      console.error('Watchlist error:', error);
      // You could add a toast notification here
    } finally {
      setIsLoading(false);
    }
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(<span key={i} className="star filled">★</span>);
    }

    if (hasHalfStar) {
      stars.push(<span key="half" className="star half">★</span>);
    }

    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<span key={`empty-${i}`} className="star empty">★</span>);
    }

    return stars;
  };

  return (
    <div className="movie-card" onClick={handleMovieClick}>
      <div className="movie-poster">
        {(movie.film_image_url || movie.poster_url) ? (
          <img 
            src={movie.film_image_url || movie.poster_url} 
            alt={movie.title}
            onError={(e) => {
              // Fallback to a default movie poster placeholder
              e.target.src = 'https://via.placeholder.com/300x450/1a1a2e/6c757d?text=🎬+No+Image';
            }}
          />
        ) : (
          <div className="poster-placeholder">
            <span className="placeholder-icon">🎬</span>
            <span className="placeholder-text">No Image</span>
          </div>
        )}
        
        {/* IMDb Rating Badge - Always visible */}
        <div className="rating-badge">
          <div className="rating-stars">
            {renderStars(movie.imdb_rating || 0)}
          </div>
          <span className="rating-number">
            {movie.imdb_rating ? movie.imdb_rating.toFixed(1) : 'N/A'}
          </span>
        </div>
        
        {/* Hover overlay with financial info */}
        <div className="movie-overlay">
          {(movie.budget_crores || movie.gross_crores) && (
            <div className="movie-financials">
              {movie.budget_crores && (
                <div className="financial-item">
                  <span className="financial-label">Budget:</span>
                  <span className="financial-value">₹{movie.budget_crores}Cr</span>
                </div>
              )}
              {movie.gross_crores && (
                <div className="financial-item">
                  <span className="financial-label">Gross:</span>
                  <span className="financial-value">₹{movie.gross_crores}Cr</span>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
      
      <div className="movie-info">
        <h3 className="movie-title" title={movie.title}>
          {movie.title}
        </h3>
        <div className="movie-meta">
          <span className="movie-year">
            {movie.release_year || 'N/A'}
          </span>
          <span className="movie-genre">
            {movie.genre || 'Unknown'}
          </span>
        </div>
        
        {/* Watchlist Button - Most Important UI Element */}
        <button 
          className={`watchlist-btn ${inWatchlist ? 'in-watchlist' : 'not-in-watchlist'} ${isLoading ? 'loading' : ''}`}
          onClick={handleWatchlistToggle}
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <span className="spinner"></span>
              {inWatchlist ? 'Removing...' : 'Adding...'}
            </>
          ) : (
            <>
              {inWatchlist ? (
                <>
                  <span className="check-icon">✓</span>
                  In Watchlist
                </>
              ) : (
                <>
                  <span className="plus-icon">+</span>
                  Add to Watchlist
                </>
              )}
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default MovieCard;

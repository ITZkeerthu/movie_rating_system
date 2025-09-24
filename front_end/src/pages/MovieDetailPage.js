import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './MovieDetailPage.css';

const MovieDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [isInWatchlist, setIsInWatchlist] = useState(false);
  const [isLiked, setIsLiked] = useState(false);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    fetchMovieDetails();
  }, [id]);

  const fetchMovieDetails = async () => {
    try {
      setLoading(true);
      setError('');

      const response = await axios.get(`/movies/${id}`);
      setMovie(response.data);
      
      // Check if movie is in user's watchlist and liked status
      // This would require additional API endpoints
      // For now, we'll set default values
      setIsInWatchlist(false);
      setIsLiked(false);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to fetch movie details');
    } finally {
      setLoading(false);
    }
  };

  const handleAddToWatchlist = async () => {
    if (!movie) return;

    try {
      setActionLoading(true);
      
      if (isInWatchlist) {
        await axios.delete(`/user/watchlist/${movie.id}`);
        setIsInWatchlist(false);
      } else {
        await axios.post('/user/watchlist', { movie_id: movie.id });
        setIsInWatchlist(true);
      }
    } catch (err) {
      console.error('Failed to update watchlist:', err);
      // You might want to show a toast notification here
    } finally {
      setActionLoading(false);
    }
  };

  const handleLike = async () => {
    if (!movie) return;

    try {
      setActionLoading(true);
      
      if (isLiked) {
        await axios.delete(`/user/likes/${movie.id}`);
        setIsLiked(false);
      } else {
        await axios.post('/user/likes', { movie_id: movie.id });
        setIsLiked(true);
      }
    } catch (err) {
      console.error('Failed to update like status:', err);
      // You might want to show a toast notification here
    } finally {
      setActionLoading(false);
    }
  };

  const handleBackToHome = () => {
    navigate('/');
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

  if (loading) {
    return (
      <div className="movie-detail-page">
        <div className="loading-spinner">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="movie-detail-page">
        <div className="error-message">
          <h3>Oops! Something went wrong</h3>
          <p>{error}</p>
          <button onClick={handleBackToHome} className="btn btn-primary">
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  if (!movie) {
    return (
      <div className="movie-detail-page">
        <div className="empty-state">
          <h3>Movie not found</h3>
          <p>The movie you're looking for doesn't exist.</p>
          <button onClick={handleBackToHome} className="btn btn-primary">
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="movie-detail-page">
      <div className="movie-detail-container">
        <div className="movie-detail-content">
          <div className="movie-poster-section">
            {(movie.film_image_url || movie.poster_url) ? (
              <img 
                src={movie.film_image_url || movie.poster_url} 
                alt={movie.title}
                className="movie-poster"
                onError={(e) => {
                  e.target.src = 'https://via.placeholder.com/400x600/1a1a2e/6c757d?text=🎬+No+Image';
                }}
              />
            ) : (
              <div className="poster-placeholder">
                <span className="placeholder-icon">🎬</span>
                <span className="placeholder-text">No Image Available</span>
              </div>
            )}
          </div>

          <div className="movie-info-section">
            <div className="movie-header">
              <h1 className="movie-title">{movie.title}</h1>
              <div className="movie-rating">
                {renderStars(movie.imdb_rating || 0)}
                <span className="rating-number">
                  {movie.imdb_rating ? movie.imdb_rating.toFixed(1) : 'N/A'}
                </span>
              </div>
            </div>

            <div className="movie-meta">
              <div className="meta-item">
                <span className="meta-label">Genre:</span>
                <span className="meta-value">{movie.genre || 'Unknown'}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Language:</span>
                <span className="meta-value">{movie.language || 'Unknown'}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Release Year:</span>
                <span className="meta-value">{movie.release_year || 'Unknown'}</span>
              </div>
              {movie.budget_crores && (
                <div className="meta-item">
                  <span className="meta-label">Budget:</span>
                  <span className="meta-value budget">₹{movie.budget_crores} Crores</span>
                </div>
              )}
              {movie.gross_crores && (
                <div className="meta-item">
                  <span className="meta-label">Box Office:</span>
                  <span className="meta-value gross">₹{movie.gross_crores} Crores</span>
                </div>
              )}
            </div>

            <div className="movie-synopsis">
              <h3>Synopsis</h3>
              <p>{movie.synopsis || 'No synopsis available for this movie.'}</p>
            </div>

            <div className="movie-actions">
              <button
                className={`btn ${isInWatchlist ? 'btn-secondary' : 'btn-primary'}`}
                onClick={handleAddToWatchlist}
                disabled={actionLoading}
              >
                {actionLoading ? (
                  <>
                    <span className="spinner-small"></span>
                    {isInWatchlist ? 'Removing...' : 'Adding...'}
                  </>
                ) : (
                  <>
                    {isInWatchlist ? '✓' : '+'} 
                    {isInWatchlist ? ' Remove from Watchlist' : ' Add to Watchlist'}
                  </>
                )}
              </button>

              <button
                className={`btn ${isLiked ? 'btn-danger' : 'btn-secondary'}`}
                onClick={handleLike}
                disabled={actionLoading}
              >
                {isLiked ? '❤️' : '🤍'} 
                {isLiked ? ' Liked' : ' Like'}
              </button>

              <button
                className="btn btn-secondary"
                onClick={handleBackToHome}
              >
                ← Back to Home
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MovieDetailPage;

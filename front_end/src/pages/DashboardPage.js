import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import MovieGrid from '../components/MovieGrid';
import axios from 'axios';
import './DashboardPage.css';

const DashboardPage = () => {
  const navigate = useNavigate();
  const [watchlist, setWatchlist] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      setError('');

      // Fetch user's watchlist
      const watchlistResponse = await axios.get('/user/watchlist');
      setWatchlist(watchlistResponse.data.movies || []);

      // Fetch recommendations (this would be a separate endpoint)
      // For now, we'll use a placeholder
      try {
        const recommendationsResponse = await axios.get('/user/recommendations');
        setRecommendations(recommendationsResponse.data.movies || []);
      } catch (err) {
        // Recommendations endpoint might not exist yet
        console.log('Recommendations not available yet');
        setRecommendations([]);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to fetch user data');
    } finally {
      setLoading(false);
    }
  };

  const handleMovieClick = (movieId) => {
    navigate(`/movie/${movieId}`);
  };

  if (loading) {
    return (
      <div className="dashboard-page">
        <div className="loading-spinner">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-page">
      <div className="dashboard-container">
        <div className="dashboard-header">
          <h1>Your Dashboard</h1>
          <p>Manage your watchlist and discover new movies</p>
        </div>

        <div className="dashboard-content">
          {/* Watchlist Section */}
          <section className="dashboard-section">
            <div className="section-header">
              <h2>Your Watchlist</h2>
              <span className="section-count">
                {watchlist.length} {watchlist.length === 1 ? 'movie' : 'movies'}
              </span>
            </div>
            
            {watchlist.length > 0 ? (
              <div className="movie-grid-container">
                <div className="movie-grid">
                  {watchlist.map(movie => (
                    <div 
                      key={movie.id} 
                      className="movie-card"
                      onClick={() => handleMovieClick(movie.id)}
                    >
                      <div className="movie-poster">
                        {movie.poster_url ? (
                          <img 
                            src={movie.poster_url} 
                            alt={movie.title}
                            onError={(e) => {
                              e.target.src = '/api/placeholder/300/450';
                            }}
                          />
                        ) : (
                          <div className="poster-placeholder">
                            <span className="placeholder-icon">🎬</span>
                            <span className="placeholder-text">No Image</span>
                          </div>
                        )}
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
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="empty-state">
                <div className="empty-icon">📝</div>
                <h3>Your watchlist is empty</h3>
                <p>Start adding movies to your watchlist to see them here.</p>
                <button 
                  className="btn btn-primary"
                  onClick={() => navigate('/')}
                >
                  Browse Movies
                </button>
              </div>
            )}
          </section>

          {/* Recommendations Section */}
          {recommendations.length > 0 && (
            <section className="dashboard-section">
              <div className="section-header">
                <h2>Recommended for You</h2>
                <span className="section-count">
                  {recommendations.length} {recommendations.length === 1 ? 'movie' : 'movies'}
                </span>
              </div>
              
              <div className="movie-grid-container">
                <div className="movie-grid">
                  {recommendations.map(movie => (
                    <div 
                      key={movie.id} 
                      className="movie-card"
                      onClick={() => handleMovieClick(movie.id)}
                    >
                      <div className="movie-poster">
                        {movie.poster_url ? (
                          <img 
                            src={movie.poster_url} 
                            alt={movie.title}
                            onError={(e) => {
                              e.target.src = '/api/placeholder/300/450';
                            }}
                          />
                        ) : (
                          <div className="poster-placeholder">
                            <span className="placeholder-icon">🎬</span>
                            <span className="placeholder-text">No Image</span>
                          </div>
                        )}
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
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </section>
          )}

          {error && (
            <div className="error-message">
              <h3>Oops! Something went wrong</h3>
              <p>{error}</p>
              <button 
                className="btn btn-primary"
                onClick={fetchUserData}
              >
                Try Again
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;

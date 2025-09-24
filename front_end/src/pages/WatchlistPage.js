import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import MovieCard from '../components/MovieCard';
import './WatchlistPage.css';

const WatchlistPage = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [watchlist, setWatchlist] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    fetchWatchlist();
  }, [user, navigate]);

  const fetchWatchlist = async () => {
    try {
      setLoading(true);
      setError('');
      
      const response = await axios.get('/watchlist');
      setWatchlist(response.data.watchlist || []);
    } catch (err) {
      console.error('Failed to fetch watchlist:', err);
      setError(err.response?.data?.message || 'Failed to load your watchlist');
    } finally {
      setLoading(false);
    }
  };

  const handleWatchlistChange = (movieId, inWatchlist) => {
    if (!inWatchlist) {
      // Remove from local state when removed from watchlist
      setWatchlist(prev => prev.filter(movie => movie.id !== movieId));
    }
  };

  const handleBackToBrowse = () => {
    navigate('/');
  };

  const handleClearWatchlist = async () => {
    if (!window.confirm('Are you sure you want to clear your entire watchlist?')) {
      return;
    }

    try {
      // Remove all movies from watchlist
      const removePromises = watchlist.map(movie => 
        axios.delete(`/watchlist/${movie.id}`)
      );
      
      await Promise.all(removePromises);
      setWatchlist([]);
    } catch (error) {
      console.error('Failed to clear watchlist:', error);
      setError('Failed to clear watchlist');
    }
  };

  if (loading) {
    return (
      <div className="watchlist-page">
        <div className="loading-container">
          <div className="spinner-large"></div>
          <p>Loading your watchlist...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="watchlist-page">
        <div className="error-container">
          <h3>Oops! Something went wrong</h3>
          <p>{error}</p>
          <div className="error-actions">
            <button onClick={fetchWatchlist} className="btn btn-primary">
              Try Again
            </button>
            <button onClick={handleBackToBrowse} className="btn btn-secondary">
              Browse Movies
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="watchlist-page">
      <div className="watchlist-header">
        <div className="header-content">
          <h1 className="page-title">
            <span className="watchlist-icon">📺</span>
            My Watchlist
          </h1>
          <p className="page-subtitle">
            {watchlist.length === 0 
              ? "Your watchlist is empty" 
              : `${watchlist.length} movie${watchlist.length !== 1 ? 's' : ''} saved for later`
            }
          </p>
        </div>
        
        <div className="header-actions">
          <button onClick={handleBackToBrowse} className="btn btn-secondary">
            ← Browse Movies
          </button>
          {watchlist.length > 0 && (
            <button onClick={handleClearWatchlist} className="btn btn-outline-danger">
              Clear All
            </button>
          )}
        </div>
      </div>

      {watchlist.length === 0 ? (
        <div className="empty-watchlist">
          <div className="empty-state">
            <div className="empty-icon">🎬</div>
            <h3>Your Watchlist is Empty</h3>
            <p>
              Start building your watchlist by browsing movies and clicking 
              the "Add to Watchlist" button on any movie you want to watch later.
            </p>
            <button onClick={handleBackToBrowse} className="btn btn-primary btn-lg">
              Discover Movies
            </button>
          </div>
        </div>
      ) : (
        <div className="watchlist-content">
          <div className="movies-grid">
            {watchlist.map(movie => (
              <MovieCard
                key={movie.id}
                movie={movie}
                initialInWatchlist={true}
                onWatchlistChange={handleWatchlistChange}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default WatchlistPage;
import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import SidebarFilters from '../components/SidebarFilters';
import MovieCard from '../components/MovieCard';
import axios from 'axios';
import './HomePage.css';

const HomePage = () => {
  const [searchParams] = useSearchParams();
  const { user } = useAuth();
  const [movies, setMovies] = useState([]);
  const [watchlistStatus, setWatchlistStatus] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    search: '',
    genre: '',
    year: '',
    min_rating: '',
    max_rating: '',
    sort: 'rating_desc'
  });
  const [filterOptions, setFilterOptions] = useState({
    genres: [],
    years: [],
    rating_range: { min: 0, max: 10 }
  });
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

  // Get search query from URL
  const searchQuery = searchParams.get('search') || '';

  const fetchFilterOptions = useCallback(async () => {
    try {
      const response = await axios.get('/movies/filters');
      setFilterOptions(response.data);
    } catch (err) {
      console.error('Failed to fetch filter options:', err);
    }
  }, []);

  const fetchWatchlistStatus = useCallback(async (movieIds) => {
    if (!movieIds || movieIds.length === 0) return;
    
    try {
      const response = await axios.get(`/watchlist/status?movie_ids=${movieIds.join(',')}`);
      setWatchlistStatus(response.data.status || {});
    } catch (err) {
      console.error('Failed to fetch watchlist status:', err);
    }
  }, []);

  const fetchMovies = useCallback(async (currentFilters) => {
    const controller = new AbortController();
    try {
      setLoading(true);
      setError('');

      const params = new URLSearchParams();
      
      // Apply all filters
      Object.entries(currentFilters).forEach(([key, value]) => {
        if (value && value !== '') {
          params.append(key, value);
        }
      });

      const response = await axios.get(`/movies?${params.toString()}`, {
        signal: controller.signal
      });
      
      const moviesData = response.data.movies || [];
      
      setMovies(moviesData);
      
      // Fetch watchlist status for logged-in users
      if (user && moviesData.length > 0) {
        await fetchWatchlistStatus(moviesData.map(m => m.id));
      }
    } catch (err) {
      if (!axios.isCancel(err)) {
        setError(err.response?.data?.message || 'Failed to fetch movies');
        setMovies([]);
      }
    } finally {
      setLoading(false);
    }
    
    return controller;
  }, [user, fetchWatchlistStatus]);

  useEffect(() => {
    fetchFilterOptions();
  }, [fetchFilterOptions]);

  useEffect(() => {
    // Update search filter when URL changes
    setFilters(prevFilters => ({ ...prevFilters, search: searchQuery }));
  }, [searchQuery]);

  useEffect(() => {
    let controller;
    const timeoutId = setTimeout(async () => {
      try {
        controller = await fetchMovies(filters);
      } catch (error) {
        if (!axios.isCancel(error)) {
          setError(error.message || 'Failed to fetch movies');
        }
      }
    }, 300);

    return () => {
      clearTimeout(timeoutId);
      if (controller) {
        controller.abort();
      }
    };
  }, [filters, fetchMovies]);



  const handleFiltersChange = useCallback((newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  }, []);

  const handleWatchlistChange = useCallback((movieId, inWatchlist) => {
    setWatchlistStatus(prev => ({
      ...prev,
      [movieId]: inWatchlist
    }));
  }, []);

  const toggleSidebar = useCallback(() => {
    setIsSidebarCollapsed(prev => !prev);
  }, []);

  const renderMovieGrid = () => {
    if (loading) {
      return (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading amazing movies for you...</p>
        </div>
      );
    }

    if (error) {
      return (
        <div className="error-container">
          <h3>Oops! Something went wrong</h3>
          <p>{error}</p>
          <button 
            onClick={() => {
              setError('');
              fetchMovies(filters);
            }} 
            className="btn btn-primary"
          >
            Try Again
          </button>
        </div>
      );
    }

    if (!movies || movies.length === 0) {
      return (
        <div className="empty-state">
          <div className="empty-icon">🎬</div>
          <h3>No movies found</h3>
          <p>Try adjusting your search or filters to discover more movies.</p>
          <button 
            onClick={() => setFilters({
              search: '',
              genre: '',
              year: '',
              min_rating: '',
              max_rating: '',
              sort: 'rating_desc'
            })} 
            className="btn btn-primary"
          >
            Clear Filters
          </button>
        </div>
      );
    }

    return (
      <div className="movies-grid">
        {movies.map(movie => (
          <MovieCard
            key={movie.id}
            movie={movie}
            initialInWatchlist={watchlistStatus[movie.id] || false}
            onWatchlistChange={handleWatchlistChange}
          />
        ))}
      </div>
    );
  };

  return (
    <div className="home-page">
      <div className="main-layout">
        <SidebarFilters
          filters={filters}
          filterOptions={filterOptions}
          onFiltersChange={handleFiltersChange}
          isCollapsed={isSidebarCollapsed}
          onToggleCollapse={toggleSidebar}
        />
        
        <div className="main-content">
          <div className="content-header">
            <h1 className="page-title">
              {filters.search ? `Search Results for "${filters.search}"` : 'Discover Movies'}
            </h1>
            <div className="results-info">
              <p className="results-count">
                {loading ? 'Loading...' : `${movies.length} movies found`}
              </p>
              {Object.values(watchlistStatus).filter(Boolean).length > 0 && (
                <p className="watchlist-info">
                  {Object.values(watchlistStatus).filter(Boolean).length} in your watchlist
                </p>
              )}
            </div>
          </div>

          <div className="movies-container">
            {renderMovieGrid()}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

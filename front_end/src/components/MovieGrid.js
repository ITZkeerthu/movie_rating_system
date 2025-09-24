import React from 'react';
import MovieCard from './MovieCard';
import './MovieGrid.css';

const MovieGrid = ({ movies, loading, error }) => {
  if (loading) {
    return (
      <div className="movie-grid-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="movie-grid-container">
        <div className="error-message">
          <h3>Oops! Something went wrong</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  if (!movies || movies.length === 0) {
    return (
      <div className="movie-grid-container">
        <div className="empty-state">
          <div className="empty-icon">🎬</div>
          <h3>No movies found</h3>
          <p>Try adjusting your search or filters to find more movies.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="movie-grid-container">
      <div className="movie-grid">
        {movies.map(movie => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </div>
    </div>
  );
};

export default MovieGrid;

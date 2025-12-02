import React, { useState, useEffect } from 'react';
import './SidebarFilters.css';

const SidebarFilters = ({ filters, filterOptions, onFiltersChange, isCollapsed, onToggleCollapse }) => {
  const [localFilters, setLocalFilters] = useState({
    genre: filters.genre || '',
    year: filters.year || '',
    min_rating: filters.min_rating || '',
    max_rating: filters.max_rating || '',
    sort: filters.sort || 'rating_desc'
  });

  // Update local filters when props change
  useEffect(() => {
    setLocalFilters({
      genre: filters.genre || '',
      year: filters.year || '',
      min_rating: filters.min_rating || '',
      max_rating: filters.max_rating || '',
      sort: filters.sort || 'rating_desc'
    });
  }, [filters]);

  const [availableGenres] = useState(filterOptions.genres || [
    'Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
    'Documentary', 'Drama', 'Family', 'Fantasy', 'Film-Noir', 'History',
    'Horror', 'Music', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
    'Sport', 'Thriller', 'War', 'Western'
  ]);

  const [availableLanguages, setAvailableLanguages] = useState([
    'English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese',
    'Russian', 'Chinese', 'Japanese', 'Korean', 'Hindi', 'Arabic'
  ]);

  const sortOptions = [
    { value: 'rating', label: 'IMDb Rating (High to Low)' },
    { value: 'rating_asc', label: 'IMDb Rating (Low to High)' },
    { value: 'year', label: 'Release Year (Newest)' },
    { value: 'year_asc', label: 'Release Year (Oldest)' },
    { value: 'title', label: 'Title (A-Z)' },
    { value: 'title_desc', label: 'Title (Z-A)' }
  ];

  const handleGenreChange = (genre) => {
    const newFilters = {
      ...localFilters,
      genre: genre === localFilters.genre ? '' : genre
    };
    setLocalFilters(newFilters);
    onFiltersChange(newFilters);
  };

  const handleYearChange = (year) => {
    const newFilters = {
      ...localFilters,
      year: year === localFilters.year ? '' : year
    };
    setLocalFilters(newFilters);
    onFiltersChange(newFilters);
  };

  const handleRatingChange = (min, max) => {
    const newFilters = {
      ...localFilters,
      min_rating: min,
      max_rating: max
    };
    setLocalFilters(newFilters);
    onFiltersChange(newFilters);
  };

  const handleSortChange = (sort) => {
    const newFilters = {
      ...localFilters,
      sort
    };
    setLocalFilters(newFilters);
    onFiltersChange(newFilters);
  };

  const clearFilters = () => {
    const defaultFilters = {
      genre: '',
      year: '',
      min_rating: '',
      max_rating: '',
      sort: 'rating_desc'
    };
    setLocalFilters(defaultFilters);
    onFiltersChange(defaultFilters);
  };

  return (
    <div className={`filter-sidebar ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="filter-header">
        <h3>Filters</h3>
        <button 
          className="collapse-btn"
          onClick={onToggleCollapse}
        >
          {isCollapsed ? '▶' : '◀'}
        </button>
      </div>

      {!isCollapsed && (
        <>
          {/* Sort Options */}
          <div className="filter-section">
            <h4>Sort By</h4>
            <select
              value={localFilters.sort}
              onChange={(e) => handleSortChange(e.target.value)}
              className="sort-dropdown"
            >
              {sortOptions.map(option => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>

          {/* Genre Filters */}
          <div className="filter-section">
            <h4>Genres</h4>
            <div className="filter-options">
              {availableGenres.map(genre => (
                <div key={genre} className="filter-option">
                  <input
                    type="radio"
                    id={`genre-${genre}`}
                    name="genre"
                    checked={localFilters.genre === genre}
                    onChange={() => handleGenreChange(genre)}
                  />
                  <label htmlFor={`genre-${genre}`}>
                    {genre}
                  </label>
                </div>
              ))}
            </div>
          </div>

          {/* Year Filter */}
          <div className="filter-section">
            <h4>Release Year</h4>
            <div className="filter-options">
              {filterOptions.years?.map(year => (
                <div key={year} className="filter-option">
                  <input
                    type="radio"
                    id={`year-${year}`}
                    name="year"
                    checked={localFilters.year === year.toString()}
                    onChange={() => handleYearChange(year.toString())}
                  />
                  <label htmlFor={`year-${year}`}>
                    {year}
                  </label>
                </div>
              )) || Array.from({ length: 10 }, (_, i) => {
                const year = new Date().getFullYear() - i;
                return (
                  <div key={year} className="filter-option">
                    <input
                      type="radio"
                      id={`year-${year}`}
                      name="year"
                      checked={localFilters.year === year.toString()}
                      onChange={() => handleYearChange(year.toString())}
                    />
                    <label htmlFor={`year-${year}`}>
                      {year}
                    </label>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Rating Range */}
          <div className="filter-section">
            <h4>IMDb Rating</h4>
            <div className="rating-range">
              <div className="rating-input">
                <label>Min:</label>
                <input
                  type="number"
                  min={filterOptions.rating_range?.min || 0}
                  max={filterOptions.rating_range?.max || 10}
                  step="0.1"
                  value={localFilters.min_rating}
                  onChange={(e) => handleRatingChange(e.target.value, localFilters.max_rating)}
                />
              </div>
              <div className="rating-input">
                <label>Max:</label>
                <input
                  type="number"
                  min={filterOptions.rating_range?.min || 0}
                  max={filterOptions.rating_range?.max || 10}
                  step="0.1"
                  value={localFilters.max_rating}
                  onChange={(e) => handleRatingChange(localFilters.min_rating, e.target.value)}
                />
              </div>
            </div>
          </div>

          {/* Clear Filters */}
          <div className="filter-actions">
            <button 
              className="btn btn-secondary clear-filters"
              onClick={clearFilters}
            >
              Clear All Filters
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default SidebarFilters;

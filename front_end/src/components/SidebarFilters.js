import React, { useState, useEffect } from 'react';
import './SidebarFilters.css';

const SidebarFilters = ({ onFiltersChange, isCollapsed, onToggleCollapse }) => {
  const [filters, setFilters] = useState({
    genres: [],
    languages: [],
    sortBy: 'rating'
  });

  const [availableGenres, setAvailableGenres] = useState([
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
    setFilters(prev => ({
      ...prev,
      genres: prev.genres.includes(genre)
        ? prev.genres.filter(g => g !== genre)
        : [...prev.genres, genre]
    }));
  };

  const handleLanguageChange = (language) => {
    setFilters(prev => ({
      ...prev,
      languages: prev.languages.includes(language)
        ? prev.languages.filter(l => l !== language)
        : [...prev.languages, language]
    }));
  };

  const handleSortChange = (sortBy) => {
    setFilters(prev => ({
      ...prev,
      sortBy
    }));
  };

  const clearFilters = () => {
    setFilters({
      genres: [],
      languages: [],
      sortBy: 'rating'
    });
  };

  // Notify parent component when filters change
  useEffect(() => {
    onFiltersChange(filters);
  }, [filters, onFiltersChange]);

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
              value={filters.sortBy}
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
                    type="checkbox"
                    id={`genre-${genre}`}
                    checked={filters.genres.includes(genre)}
                    onChange={() => handleGenreChange(genre)}
                  />
                  <label htmlFor={`genre-${genre}`}>
                    {genre}
                  </label>
                </div>
              ))}
            </div>
          </div>

          {/* Language Filters */}
          <div className="filter-section">
            <h4>Languages</h4>
            <div className="filter-options">
              {availableLanguages.map(language => (
                <div key={language} className="filter-option">
                  <input
                    type="checkbox"
                    id={`lang-${language}`}
                    checked={filters.languages.includes(language)}
                    onChange={() => handleLanguageChange(language)}
                  />
                  <label htmlFor={`lang-${language}`}>
                    {language}
                  </label>
                </div>
              ))}
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

-- Active: 1752848446615@@127.0.0.1@5432@movie_rating_system@public
-- Show all movies that appear in the frontend

select * from movies;
SELECT 
    title AS "Movie Title",
    release_year AS "Year",
    genre AS "Genre",
    imdb_rating AS "IMDb Rating",
    film_image_url AS "Poster URL",
    language AS "Language",
    synopsis AS "Synopsis"
FROM movies 
ORDER BY imdb_rating DESC;

-- Find specific details about The Dark Knight
SELECT 
    title AS "Movie Title",
    release_year AS "Year",
    genre AS "Genre",
    imdb_rating AS "IMDb Rating",
    film_image_url AS "Poster URL",
    language AS "Language",
    synopsis AS "Synopsis"
FROM movies 
WHERE title LIKE '%Dark Knight%';

-- Check the table structure that holds this data
SELECT column_name, data_type, column_default
FROM information_schema.columns
WHERE table_name = 'movies'
ORDER BY ordinal_position;

-- Show all movie titles with their details
SELECT 
    title AS "Film Name",
    release_year AS "Year",
    genre AS "Genre",
    language AS "Language",
    imdb_rating AS "Rating"
FROM movies 
ORDER BY title ASC;
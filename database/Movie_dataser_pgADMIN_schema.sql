
SELECT id,
       title,
       genre,
       language,
       release_year,
       imdb_rating,
       poster_url,
       synopsis,
       created_at,
       budget_crores,
       gross_crores,
       film_image_url
FROM public.movies
LIMIT 1000;

SELECT id,
       user_id,
       movie_id,
       created_at
FROM public.watchlist
LIMIT 1000;

SELECT id,
       username,
       email,
       password_hash,
       created_at,
       last_loginv
FROM public.users
LIMIT 1000;

UPDATE public.movies
SET 
    poster_url = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQbVg1Qw7COxX1YY3tS4-8Du8nLJ74aVkpaGQgG1DhGomXFma2P',
    synopsis = 'While working as a bounty hunter in Goa, Francis recalls his past life, a centuries-old tale of warrior Kanguva. Turns out, he has an old score to settle and someone dear to protect in the present.',
    film_image_url = 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQbVg1Qw7COxX1YY3tS4-8Du8nLJ74aVkpaGQgG1DhGomXFma2P'
WHERE title = 'Indian 2';

UPDATE public.movies
SET 
    imdb_rating = 6.5 WHERE title = 'Demonte Colony 2';
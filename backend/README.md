# Backend (Flask) for Movie Rating System

Quick start

1. Create virtualenv and install deps
   python -m venv .venv
   .venv\\Scripts\\activate
   pip install -r requirements.txt

2. Configure environment
   Copy .env.example to .env and update values as needed.

   Required variables:
   - SECRET_KEY
   - DATABASE_URL (e.g. postgresql+psycopg2://postgres:postgres@localhost:5432/movies_db)
   - JWT_SECRET_KEY
   - CORS_ORIGINS (dev: http://localhost:3000)

3. Initialize database
   flask --app app:create_app init-db

4. Run the server
   flask --app app:create_app run -p 5000

API routes

- Auth: /auth/register, /auth/login, /auth/me
- Movies: GET /movies, GET /movies/<id>
- Watchlist: GET /watchlist, POST /watchlist/add, POST /watchlist/remove



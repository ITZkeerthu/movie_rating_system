from datetime import datetime
from passlib.hash import bcrypt
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    watchlist_items = db.relationship("Watchlist", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)

    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    # Core movie information matching your specifications
    title = db.Column(db.String(255), nullable=False, index=True)  # Film → Movie name
    release_year = db.Column(db.Integer, index=True)  # Year → Release year
    genre = db.Column(db.String(120), index=True)  # Genre → Genre(s) of the movie
    budget_crores = db.Column(db.Float, index=True)  # Budget (Crores) → Budget
    gross_crores = db.Column(db.Float, index=True)  # Gross (Crores) → Worldwide gross
    imdb_rating = db.Column(db.Float, index=True)  # IMDb Rating → Rating (e.g., 7.5/10)
    film_image_url = db.Column(db.String(500))  # Film_image_URL → Link to poster or image
    
    # Additional fields
    language = db.Column(db.String(80), index=True)
    synopsis = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=func.now())
    
    # Legacy field for backward compatibility
    poster_url = db.Column(db.String(500))
    
    # Relationships
    watchlisted_by = db.relationship("Watchlist", back_populates="movie", cascade="all, delete-orphan")
    
    # Helper properties
    @property
    def poster_image(self):
        """Return the best available poster image URL"""
        return self.film_image_url or self.poster_url
        
    def to_dict(self, include_synopsis=False):
        """Convert movie to dictionary for JSON serialization"""
        data = {
            'id': self.id,
            'title': self.title,  # Film
            'release_year': self.release_year,  # Year
            'genre': self.genre,  # Genre
            'budget_crores': self.budget_crores,  # Budget (Crores)
            'gross_crores': self.gross_crores,  # Gross (Crores)
            'imdb_rating': self.imdb_rating,  # IMDb Rating
            'film_image_url': self.film_image_url,  # Film_image_URL
            'poster_url': self.poster_image,  # For backward compatibility
            'language': self.language
        }
        if include_synopsis:
            data['synopsis'] = self.synopsis
        return data

    watchlisted_by = db.relationship("Watchlist", back_populates="movie", cascade="all, delete-orphan")


class Watchlist(db.Model):
    __tablename__ = "watchlist"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="watchlist_items")
    movie = db.relationship("Movie", back_populates="watchlisted_by")

    __table_args__ = (
        db.UniqueConstraint("user_id", "movie_id", name="uq_user_movie"),
    )



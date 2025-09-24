import os
from datetime import timedelta

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import bcrypt
from dotenv import load_dotenv

app = Flask(__name__)

# Basic config
app.config["SECRET_KEY"] = "dev-secret-key"
# Use absolute path for database
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'movies.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# JWT
app.config["JWT_SECRET_KEY"] = "dev-jwt-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=3600)

# Import models first
from models import db, User

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Initialize database
with app.app_context():
    db.create_all()

# Register blueprints
from routes.auth import auth_bp
from routes.movies import movies_bp
from routes.watchlist import watchlist_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(movies_bp, url_prefix='/movies')
app.register_blueprint(watchlist_bp, url_prefix='/watchlist')


if __name__ == "__main__":
    app.run(debug=True)



import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from models import db, User
import os

def init_db():
    # Create Flask app
    app = Flask(__name__)
    
    # Configure SQLite database
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'movies.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user exists, if not create one
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Created default admin user:")
            print("Email: admin@example.com")
            print("Password: admin123")
        
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
#!/usr/bin/env python3
"""
Database migration script to update the movies table schema
to match the new model with budget_crores, gross_crores, and film_image_url.
"""

import sqlite3
import os
from datetime import datetime

def migrate_movies_table():
    """Migrate the movies table to the new schema"""
    
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'movies.db')
    print(f"Migrating database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check current schema
        cursor.execute('PRAGMA table_info(movies)')
        current_columns = {col[1]: col[2] for col in cursor.fetchall()}
        print(f"Current columns: {list(current_columns.keys())}")
        
        # Define the new schema we want
        new_columns = {
            'budget_crores': 'FLOAT',
            'gross_crores': 'FLOAT', 
            'film_image_url': 'VARCHAR(500)'
        }
        
        # Add missing columns
        for col_name, col_type in new_columns.items():
            if col_name not in current_columns:
                print(f"Adding column: {col_name}")
                cursor.execute(f'ALTER TABLE movies ADD COLUMN {col_name} {col_type}')
            else:
                print(f"Column {col_name} already exists")
        
        # If poster_url exists and film_image_url doesn't have data, copy it
        if 'poster_url' in current_columns and 'film_image_url' in new_columns:
            cursor.execute('UPDATE movies SET film_image_url = poster_url WHERE film_image_url IS NULL AND poster_url IS NOT NULL')
            
        conn.commit()
        print("✅ Migration completed successfully!")
        
        # Show updated schema
        cursor.execute('PRAGMA table_info(movies)')
        updated_columns = cursor.fetchall()
        print("\n📋 Updated table schema:")
        for col in updated_columns:
            print(f"  {col[1]} ({col[2]})")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_movies_table()
import os
from flask_migrate import Migrate, init, migrate, upgrade
from app import create_app, db
from app.models import User, Post, Comment, Rating

def init_db():
    """Initialize the database with tables"""
    print("Initializing the database...")
    
    # Create the app with the factory
    app = create_app()
    
    # Use app context
    with app.app_context():
        # Initialize migrations directory
        if not os.path.exists('migrations'):
            print("Creating migrations directory...")
            init()
        
        # Create a migration
        print("Creating migration...")
        migrate(message="Initial migration")
        
        # Apply the migration
        print("Applying migration...")
        upgrade()
        
        print("Database initialization complete!")

if __name__ == "__main__":
    init_db()


#!/usr/bin/env python3
"""
Simple startup script for Beauty Analytics
One command to run everything
"""

import os
import sys

def main():
    print("Beauty Analytics - Starting...")
    
    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("Environment loaded from .env")
    except ImportError:
        print("Using system environment variables")
    
    # Check required environment variables
    required_vars = ['DATABASE_URL', 'FLASK_SECRET_KEY']
    missing = [var for var in required_vars if not os.environ.get(var)]
    
    if missing:
        print(f"Missing environment variables: {', '.join(missing)}")
        print("Please configure your .env file")
        return False
    
    try:
        # Import Flask app
        from app import app, db, init_app
        
        print("Initializing database...")
        with app.app_context():
            # Import models
            import models
            
            # Create tables if they don't exist
            db.create_all()
            
            # Check if we need sample data
            try:
                user_count = models.User.query.count()
                if user_count == 0:
                    print("Adding sample data...")
                    # Run seed data script
                    import subprocess
                    subprocess.run([sys.executable, "seed_data.py"], check=True)
                else:
                    print(f"Database ready with {user_count} users")
            except Exception as e:
                print(f"Sample data check failed: {e}")
        
        # Initialize app with routes
        init_app()
        
        # Start server
        print("Server starting at http://localhost:5000")
        print("Press Ctrl+C to stop")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
        
    except Exception as e:
        print(f"Startup failed: {e}")
        return False

if __name__ == '__main__':
    main()
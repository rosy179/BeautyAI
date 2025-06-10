#!/usr/bin/env python3
"""
WSGI entry point for Beauty Analytics Flask application
"""
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from main import app, db

# Initialize database tables
with app.app_context():
    try:
        db.create_all()
        print("Database tables initialized successfully")
    except Exception as e:
        print(f"Database initialization warning: {e}")

# Export application for WSGI server
application = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
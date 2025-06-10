#!/usr/bin/env python3
"""
Local development server runner
Load environment variables from .env file and start the Flask application
"""

import os
import sys

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Environment variables loaded from .env file")
except ImportError:
    print("python-dotenv not installed. Install with: pip install python-dotenv")
    print("Or set environment variables manually")

if __name__ == '__main__':
    try:
        from app import app
        
        # Development configuration
        app.config['DEBUG'] = True
        app.config['ENV'] = 'development'
        
        # Check essential environment variables
        required_vars = ['DATABASE_URL', 'FLASK_SECRET_KEY']
        missing_vars = [var for var in required_vars if not os.environ.get(var)]
        
        if missing_vars:
            print("Missing required environment variables:")
            for var in missing_vars:
                print(f"  - {var}")
            print("\nPlease check your .env file configuration")
            sys.exit(1)
        
        # Run the application
        print("Starting Beauty Analytics development server...")
        print("Application will be available at: http://localhost:5000")
        print("Make sure your .env file is configured with API keys")
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure you have installed all dependencies: pip install -r dependencies.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)
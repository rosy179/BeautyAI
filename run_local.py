#!/usr/bin/env python3
"""
Local development server runner
Load environment variables from .env file and start the Flask application
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == '__main__':
    from app import app
    
    # Development configuration
    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'
    
    # Run the application
    print("🚀 Starting Beauty Analytics development server...")
    print(f"📱 Application will be available at: http://localhost:5000")
    print(f"🔑 Make sure your .env file is configured with API keys")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )
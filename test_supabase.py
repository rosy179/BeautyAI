#!/usr/bin/env python3
"""
Script để test kết nối Supabase database
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_supabase_connection():
    """Test connection to Supabase database"""
    try:
        from app import app, db
        
        with app.app_context():
            # Test basic connection
            result = db.engine.execute("SELECT 1 as test")
            print("✅ Supabase connection successful!")
            
            # List all tables
            tables = db.engine.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            
            print("\n📋 Tables in database:")
            table_list = [table[0] for table in tables]
            if table_list:
                for table in table_list:
                    print(f"  - {table}")
            else:
                print("  No tables found. Run 'python -c \"from app import app, db; app.app_context().push(); db.create_all()\"' first")
            
            # Test sample data
            if 'user' in table_list:
                user_count = db.engine.execute("SELECT COUNT(*) FROM \"user\"").scalar()
                print(f"\n👥 Users in database: {user_count}")
            
            if 'product' in table_list:
                product_count = db.engine.execute("SELECT COUNT(*) FROM product").scalar()
                print(f"🛍️ Products in database: {product_count}")
                
            return True
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your DATABASE_URL in .env file")
        print("2. Verify Supabase project is running")
        print("3. Check password and project reference")
        return False

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = {
        'DATABASE_URL': 'Supabase connection string',
        'FLASK_SECRET_KEY': 'Flask session secret',
        'FACEPP_API_KEY': 'Face++ API key for skin analysis',
        'FACEPP_API_SECRET': 'Face++ API secret'
    }
    
    print("🔑 Environment Variables Check:")
    all_good = True
    
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            # Mask sensitive values
            if 'SECRET' in var or 'PASSWORD' in var or 'KEY' in var:
                display_value = value[:8] + "..." if len(value) > 8 else "***"
            else:
                display_value = value[:50] + "..." if len(value) > 50 else value
            print(f"  ✅ {var}: {display_value}")
        else:
            print(f"  ❌ {var}: Missing - {description}")
            all_good = False
    
    return all_good

if __name__ == "__main__":
    print("🧪 Testing Supabase Connection for Beauty Analytics\n")
    
    # Check environment variables
    env_ok = check_environment()
    print()
    
    if env_ok:
        # Test database connection
        db_ok = test_supabase_connection()
        
        if db_ok:
            print("\n🎉 All checks passed! Your app is ready to run.")
            print("👉 Run: python run_local.py")
        else:
            print("\n🔧 Please fix database connection issues first.")
    else:
        print("\n🔧 Please configure your .env file first.")
        print("👉 Copy from .env.example and fill in your values.")
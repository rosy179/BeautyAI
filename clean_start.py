#!/usr/bin/env python3
"""
Complete clean restart that resolves SQLAlchemy conflicts
and tests network connectivity
"""

import os
import sys
import subprocess
import importlib

def clear_python_cache():
    """Clear all Python module caches"""
    # Clear module cache
    modules_to_clear = []
    for module_name in list(sys.modules.keys()):
        if any(x in module_name for x in ['app', 'models', 'database', 'sqlalchemy', 'flask_sqlalchemy']):
            modules_to_clear.append(module_name)
    
    for module in modules_to_clear:
        if module in sys.modules:
            del sys.modules[module]
    
    # Clear importlib cache
    importlib.invalidate_caches()

def test_network_connectivity():
    """Test network and Supabase connectivity"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("Error: DATABASE_URL not found in environment")
        return False
    
    # Test basic network connectivity first
    print("Testing network connectivity...")
    
    # Extract hostname from DATABASE_URL
    from urllib.parse import urlparse
    parsed = urlparse(db_url)
    hostname = parsed.hostname
    
    print(f"Testing connection to: {hostname}")
    
    # Test with ping first
    import platform
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    
    try:
        result = subprocess.run(['ping', param, '1', hostname], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("Network connectivity: OK")
        else:
            print("Network connectivity: Failed")
            print("Check your internet connection or Supabase hostname")
            return False
    except Exception as e:
        print(f"Network test failed: {e}")
        return False
    
    # Test database connection
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            connect_timeout=10
        )
        conn.close()
        print("Database connection: OK")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("Check your DATABASE_URL and Supabase project status")
        return False

def create_isolated_db_script():
    """Create a completely isolated database initialization script"""
    script_content = '''#!/usr/bin/env python3
import os
import sys

# Completely fresh environment
if __name__ == "__main__":
    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # Import fresh Flask and SQLAlchemy
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from sqlalchemy.orm import DeclarativeBase
    from datetime import datetime
    from werkzeug.security import generate_password_hash
    
    # Fresh declarative base
    class Base(DeclarativeBase):
        pass
    
    # Fresh db instance
    db = SQLAlchemy(model_class=Base)
    
    # Fresh app instance
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "connect_args": {"sslmode": "require"}
    }
    
    # Initialize db with app
    db.init_app(app)
    
    # Define fresh models
    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(256))
        full_name = db.Column(db.String(100))
        is_admin = db.Column(db.Boolean, default=False)
        date_joined = db.Column(db.DateTime, default=datetime.utcnow)
        
        def set_password(self, password):
            self.password_hash = generate_password_hash(password)
    
    class Category(db.Model):
        __tablename__ = 'category'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        description = db.Column(db.Text)
    
    class Product(db.Model):
        __tablename__ = 'product'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(200), nullable=False)
        description = db.Column(db.Text)
        price = db.Column(db.Float, nullable=False)
        brand = db.Column(db.String(100))
        category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
        stock_quantity = db.Column(db.Integer, default=0)
        skin_type = db.Column(db.String(100))
        image_url = db.Column(db.String(500))
        date_added = db.Column(db.DateTime, default=datetime.utcnow)
        is_active = db.Column(db.Boolean, default=True)
    
    class SkinAnalysis(db.Model):
        __tablename__ = 'skin_analysis'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        image_url = db.Column(db.String(500))
        analysis_result = db.Column(db.JSON)
        skin_type = db.Column(db.String(50))
        date_analyzed = db.Column(db.DateTime, default=datetime.utcnow)
    
    class BlogPost(db.Model):
        __tablename__ = 'blog_post'
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False)
        content = db.Column(db.Text, nullable=False)
        author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        date_created = db.Column(db.DateTime, default=datetime.utcnow)
        is_published = db.Column(db.Boolean, default=False)
    
    # Initialize database
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Verify tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Created {len(tables)} tables: {', '.join(tables)}")
        
        # Add sample data if empty
        existing_users = db.session.execute(db.select(User)).first()
        if not existing_users:
            print("Adding sample data...")
            
            # Create users
            admin = User(
                username='admin',
                email='admin@beautyapp.com',
                full_name='Beauty Admin',
                is_admin=True
            )
            admin.set_password('admin123')
            
            user = User(
                username='testuser',
                email='user@example.com',
                full_name='Test User'
            )
            user.set_password('password123')
            
            # Create categories
            skincare_cat = Category(
                name='Chăm sóc da',
                description='Sản phẩm chăm sóc da mặt và cơ thể'
            )
            
            makeup_cat = Category(
                name='Trang điểm',
                description='Sản phẩm trang điểm và làm đẹp'
            )
            
            db.session.add_all([admin, user, skincare_cat, makeup_cat])
            db.session.commit()
            
            # Create products
            products = [
                Product(
                    name='Sữa rửa mặt La Roche-Posay',
                    description='Sữa rửa mặt dành cho da dầu mụn',
                    price=250000,
                    brand='La Roche-Posay',
                    category_id=skincare_cat.id,
                    stock_quantity=50,
                    skin_type='oily',
                    image_url='https://via.placeholder.com/300x300'
                ),
                Product(
                    name='Kem chống nắng Anessa',
                    description='Kem chống nắng SPF 50+ PA++++',
                    price=450000,
                    brand='Anessa',
                    category_id=skincare_cat.id,
                    stock_quantity=30,
                    skin_type='all',
                    image_url='https://via.placeholder.com/300x300'
                ),
                Product(
                    name='Son môi MAC Ruby Woo',
                    description='Son lì màu đỏ ruby kinh điển',
                    price=650000,
                    brand='MAC',
                    category_id=makeup_cat.id,
                    stock_quantity=40,
                    skin_type='all',
                    image_url='https://via.placeholder.com/300x300'
                )
            ]
            
            db.session.add_all(products)
            db.session.commit()
            
            # Create blog post
            blog = BlogPost(
                title='Hướng dẫn chăm sóc da cơ bản',
                content='Chăm sóc da là một quá trình quan trọng...',
                author_id=admin.id,
                is_published=True
            )
            
            db.session.add(blog)
            db.session.commit()
            
            print("Sample data added successfully!")
            
            # Final verification
            user_count = db.session.execute(db.select(User)).scalars().all()
            product_count = db.session.execute(db.select(Product)).scalars().all()
            
            print(f"Users created: {len(user_count)}")
            print(f"Products created: {len(product_count)}")
            
        else:
            print("Database already contains data")
        
        print("Database initialization complete!")
'''
    
    return script_content

def main():
    print("Beauty Analytics - Clean Database Setup")
    print("=" * 45)
    
    # Step 1: Clear all caches
    print("Step 1: Clearing Python module caches...")
    clear_python_cache()
    
    # Step 2: Test connectivity
    print("\nStep 2: Testing connectivity...")
    if not test_network_connectivity():
        print("\nPlease fix connectivity issues before proceeding:")
        print("1. Check your internet connection")
        print("2. Verify Supabase project is running")
        print("3. Check DATABASE_URL in .env file")
        return
    
    # Step 3: Create and run isolated database script
    print("\nStep 3: Creating database tables...")
    
    script_content = create_isolated_db_script()
    
    # Write to temporary file
    script_path = 'isolated_db_init.py'
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Run in completely separate process
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("Database initialization successful!")
            print(result.stdout)
            
            # Clean up temporary file
            os.remove(script_path)
            
            print("\n" + "=" * 45)
            print("SUCCESS: Database is ready!")
            print("=" * 45)
            print("Next steps:")
            print("1. Your Supabase database now has all tables")
            print("2. Sample data has been added")
            print("3. You can now integrate with your full Flask app")
            print("\nTest accounts:")
            print("- Admin: admin@beautyapp.com / admin123")
            print("- User: user@example.com / password123")
            
        else:
            print("Database initialization failed:")
            print(result.stderr)
            print("\nTroubleshooting:")
            print("1. Check your .env file configuration")
            print("2. Verify Supabase project status")
            print("3. Try restarting your terminal/IDE")
            
    except subprocess.TimeoutExpired:
        print("Database initialization timed out")
        print("This may indicate network or authentication issues")
    
    except Exception as e:
        print(f"Error running database initialization: {e}")
    
    finally:
        # Clean up temporary file if it exists
        if os.path.exists(script_path):
            os.remove(script_path)

if __name__ == '__main__':
    main()
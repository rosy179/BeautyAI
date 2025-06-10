#!/usr/bin/env python3
"""
Final comprehensive solution for Beauty Analytics setup
Addresses network issues and SQLAlchemy conflicts
"""

import os
import sys
import subprocess
import time

def load_environment():
    """Load environment variables"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        return True
    except ImportError:
        print("Note: python-dotenv not available, using system environment")
        return False

def diagnose_database_url():
    """Diagnose and fix DATABASE_URL issues"""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("ERROR: DATABASE_URL not found in environment")
        print("Please check your .env file")
        return None
    
    print(f"Database URL found: {db_url[:50]}...")
    
    # Common Supabase URL issues
    if 'supabase.co' in db_url:
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(db_url)
        
        # Check if SSL is specified
        if 'sslmode' not in db_url:
            if '?' in db_url:
                fixed_url = db_url + '&sslmode=require'
            else:
                fixed_url = db_url + '?sslmode=require'
            
            print("Adding SSL requirement to DATABASE_URL")
            os.environ['DATABASE_URL'] = fixed_url
            return fixed_url
    
    return db_url

def test_basic_connectivity():
    """Test basic network connectivity"""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        return False
    
    from urllib.parse import urlparse
    parsed = urlparse(db_url)
    hostname = parsed.hostname
    
    print(f"Testing connectivity to {hostname}...")
    
    # Try to resolve hostname
    try:
        import socket
        socket.gethostbyname(hostname)
        print("Hostname resolution: OK")
        return True
    except socket.gaierror as e:
        print(f"Hostname resolution failed: {e}")
        print("This indicates a network connectivity issue")
        return False

def create_minimal_db_test():
    """Create minimal database connection test"""
    script_content = '''
import os
import sys

def test_db_connection():
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            print("No DATABASE_URL found")
            return False
        
        parsed = urlparse(db_url)
        
        # Add connection timeout and SSL
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            database=parsed.path[1:] if parsed.path else 'postgres',
            user=parsed.username,
            password=parsed.password,
            connect_timeout=30,
            sslmode='require'
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"Connected successfully to: {version[:60]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    success = test_db_connection()
    sys.exit(0 if success else 1)
'''
    return script_content

def create_isolated_database_setup():
    """Create completely isolated database setup script"""
    script_content = '''
import os
import sys

def setup_database():
    try:
        # Fresh imports
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from sqlalchemy.orm import DeclarativeBase
        from datetime import datetime
        from werkzeug.security import generate_password_hash
        
        # Create fresh declarative base
        class Base(DeclarativeBase):
            pass
        
        # Create fresh SQLAlchemy instance
        db = SQLAlchemy(model_class=Base)
        
        # Create fresh Flask app
        app = Flask(__name__)
        
        # Configure database
        db_url = os.environ.get('DATABASE_URL')
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "pool_recycle": 300,
            "pool_pre_ping": True,
            "connect_args": {
                "sslmode": "require",
                "connect_timeout": 30
            }
        }
        
        # Initialize database with app
        db.init_app(app)
        
        # Define models with explicit table names
        class User(db.Model):
            __tablename__ = 'user'
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(64), unique=True, nullable=False)
            email = db.Column(db.String(120), unique=True, nullable=False)
            password_hash = db.Column(db.String(256))
            full_name = db.Column(db.String(100))
            phone = db.Column(db.String(20))
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
            user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
            image_url = db.Column(db.String(500))
            analysis_result = db.Column(db.JSON)
            skin_type = db.Column(db.String(50))
            skin_concerns = db.Column(db.JSON)
            date_analyzed = db.Column(db.DateTime, default=datetime.utcnow)
        
        class Order(db.Model):
            __tablename__ = 'order'
            id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
            total_amount = db.Column(db.Float, nullable=False)
            status = db.Column(db.String(50), default='pending')
            shipping_address = db.Column(db.Text)
            phone_number = db.Column(db.String(20))
            payment_method = db.Column(db.String(50))
            date_created = db.Column(db.DateTime, default=datetime.utcnow)
        
        class OrderItem(db.Model):
            __tablename__ = 'order_item'
            id = db.Column(db.Integer, primary_key=True)
            order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
            product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
            quantity = db.Column(db.Integer, nullable=False)
            price = db.Column(db.Float, nullable=False)
        
        class Review(db.Model):
            __tablename__ = 'review'
            id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
            product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
            rating = db.Column(db.Integer, nullable=False)
            title = db.Column(db.String(200))
            content = db.Column(db.Text)
            date_created = db.Column(db.DateTime, default=datetime.utcnow)
        
        class BlogPost(db.Model):
            __tablename__ = 'blog_post'
            id = db.Column(db.Integer, primary_key=True)
            title = db.Column(db.String(200), nullable=False)
            content = db.Column(db.Text, nullable=False)
            excerpt = db.Column(db.Text)
            author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
            date_created = db.Column(db.DateTime, default=datetime.utcnow)
            is_published = db.Column(db.Boolean, default=False)
            tags = db.Column(db.String(500))
        
        class ChatMessage(db.Model):
            __tablename__ = 'chat_message'
            id = db.Column(db.Integer, primary_key=True)
            user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
            message = db.Column(db.Text, nullable=False)
            response = db.Column(db.Text)
            is_from_user = db.Column(db.Boolean, default=True)
            date_created = db.Column(db.DateTime, default=datetime.utcnow)
            session_id = db.Column(db.String(100))
        
        # Initialize database
        with app.app_context():
            print("Creating database tables...")
            db.create_all()
            
            # Verify tables created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Successfully created {len(tables)} tables:")
            for table in sorted(tables):
                print(f"  - {table}")
            
            # Check if we need to add sample data
            existing_users = db.session.execute(db.select(User)).scalars().first()
            
            if not existing_users:
                print("Adding sample data...")
                
                # Create admin user
                admin = User(
                    username='admin',
                    email='admin@beautyapp.com',
                    full_name='Beauty Admin',
                    phone='0123456789',
                    is_admin=True
                )
                admin.set_password('admin123')
                
                # Create test user
                test_user = User(
                    username='testuser',
                    email='user@example.com',
                    full_name='Test User',
                    phone='0987654321'
                )
                test_user.set_password('password123')
                
                # Create categories
                skincare_cat = Category(
                    name='Chăm sóc da',
                    description='Sản phẩm chăm sóc da mặt và cơ thể'
                )
                
                makeup_cat = Category(
                    name='Trang điểm',
                    description='Sản phẩm trang điểm và làm đẹp'
                )
                
                db.session.add_all([admin, test_user, skincare_cat, makeup_cat])
                db.session.commit()
                
                # Create products
                products = [
                    Product(
                        name='Sữa rửa mặt La Roche-Posay Effaclar',
                        description='Sữa rửa mặt dành cho da dầu mụn, làm sạch sâu',
                        price=250000,
                        brand='La Roche-Posay',
                        category_id=skincare_cat.id,
                        stock_quantity=50,
                        skin_type='oily',
                        image_url='https://via.placeholder.com/300x300?text=La+Roche+Posay',
                        is_active=True
                    ),
                    Product(
                        name='Kem chống nắng Anessa Perfect UV',
                        description='Kem chống nắng SPF 50+ PA++++, chống nước',
                        price=450000,
                        brand='Anessa',
                        category_id=skincare_cat.id,
                        stock_quantity=30,
                        skin_type='all',
                        image_url='https://via.placeholder.com/300x300?text=Anessa',
                        is_active=True
                    ),
                    Product(
                        name='Son môi MAC Ruby Woo',
                        description='Son lì màu đỏ ruby kinh điển, lâu trôi',
                        price=650000,
                        brand='MAC',
                        category_id=makeup_cat.id,
                        stock_quantity=40,
                        skin_type='all',
                        image_url='https://via.placeholder.com/300x300?text=MAC',
                        is_active=True
                    ),
                    Product(
                        name='Cushion Laneige Neo Nude',
                        description='Cushion trang điểm tự nhiên, che phủ hoàn hảo',
                        price=850000,
                        brand='Laneige',
                        category_id=makeup_cat.id,
                        stock_quantity=25,
                        skin_type='all',
                        image_url='https://via.placeholder.com/300x300?text=Laneige',
                        is_active=True
                    )
                ]
                
                db.session.add_all(products)
                db.session.commit()
                
                # Create blog post
                blog_post = BlogPost(
                    title='Hướng dẫn chăm sóc da cơ bản cho người mới bắt đầu',
                    content='''
                    Chăm sóc da là một quá trình quan trọng để duy trì làn da khỏe mạnh và rạng rỡ.
                    
                    Các bước cơ bản:
                    1. Làm sạch da hai lần mỗi ngày
                    2. Sử dụng toner để cân bằng độ pH
                    3. Thoa serum điều trị
                    4. Dưỡng ẩm với kem phù hợp
                    5. Bảo vệ da với kem chống nắng
                    
                    Hãy kiên trì và lựa chọn sản phẩm phù hợp với loại da của bạn.
                    ''',
                    excerpt='Hướng dẫn chi tiết các bước chăm sóc da cơ bản',
                    author_id=admin.id,
                    is_published=True,
                    tags='skincare, beginner, routine'
                )
                
                db.session.add(blog_post)
                db.session.commit()
                
                print("Sample data added successfully!")
                
                # Final verification
                user_count = len(db.session.execute(db.select(User)).scalars().all())
                product_count = len(db.session.execute(db.select(Product)).scalars().all())
                category_count = len(db.session.execute(db.select(Category)).scalars().all())
                
                print(f"Database populated with:")
                print(f"  - {user_count} users")
                print(f"  - {category_count} categories") 
                print(f"  - {product_count} products")
                print(f"  - 1 blog post")
                
            else:
                print("Database already contains data - skipping sample data creation")
                
                # Just show current counts
                user_count = len(db.session.execute(db.select(User)).scalars().all())
                product_count = len(db.session.execute(db.select(Product)).scalars().all())
                print(f"Current database contains {user_count} users and {product_count} products")
            
            print("Database setup completed successfully!")
            return True
            
    except Exception as e:
        print(f"Database setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = setup_database()
    sys.exit(0 if success else 1)
'''
    return script_content

def main():
    print("Beauty Analytics - Comprehensive Setup")
    print("=" * 50)
    
    # Step 1: Load environment
    print("Step 1: Loading environment configuration...")
    load_environment()
    
    # Step 2: Diagnose and fix DATABASE_URL
    print("\nStep 2: Diagnosing database configuration...")
    fixed_url = diagnose_database_url()
    if not fixed_url:
        print("Cannot proceed without valid DATABASE_URL")
        return False
    
    # Step 3: Test basic connectivity
    print("\nStep 3: Testing network connectivity...")
    if not test_basic_connectivity():
        print("Network connectivity issues detected. Please check:")
        print("1. Your internet connection")
        print("2. Supabase project status at https://supabase.com")
        print("3. DNS resolution (try restarting your router/computer)")
        return False
    
    # Step 4: Test database connection
    print("\nStep 4: Testing database connection...")
    test_script = create_minimal_db_test()
    
    with open('test_connection.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    try:
        result = subprocess.run([sys.executable, 'test_connection.py'], 
                              capture_output=True, text=True, timeout=45)
        
        if result.returncode == 0:
            print("Database connection test: PASSED")
            print(result.stdout)
        else:
            print("Database connection test: FAILED")
            print(result.stderr)
            print("\nPlease verify:")
            print("1. Supabase project is running")
            print("2. DATABASE_URL password is correct")
            print("3. Your IP is not blocked by firewall")
            return False
            
    except subprocess.TimeoutExpired:
        print("Database connection test timed out")
        return False
    finally:
        if os.path.exists('test_connection.py'):
            os.remove('test_connection.py')
    
    # Step 5: Set up database schema
    print("\nStep 5: Setting up database schema and data...")
    setup_script = create_isolated_database_setup()
    
    with open('database_setup.py', 'w', encoding='utf-8') as f:
        f.write(setup_script)
    
    try:
        result = subprocess.run([sys.executable, 'database_setup.py'], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("Database setup: SUCCESSFUL")
            print(result.stdout)
            
            print("\n" + "=" * 50)
            print("SETUP COMPLETED SUCCESSFULLY!")
            print("=" * 50)
            print("\nYour Beauty Analytics database is ready:")
            print("- All tables created in Supabase")
            print("- Sample data populated") 
            print("- Test accounts available")
            print("\nTest login credentials:")
            print("Admin: admin@beautyapp.com / admin123")
            print("User: user@example.com / password123")
            print("\nNext: Integrate this database with your full Flask application")
            
            return True
            
        else:
            print("Database setup: FAILED")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("Database setup timed out")
        return False
    finally:
        if os.path.exists('database_setup.py'):
            os.remove('database_setup.py')

if __name__ == '__main__':
    success = main()
    
    if not success:
        print("\n" + "=" * 50)
        print("SETUP FAILED - TROUBLESHOOTING GUIDE")
        print("=" * 50)
        print("1. Network Issues:")
        print("   - Check internet connection")
        print("   - Try mobile hotspot to test")
        print("   - Restart router/modem")
        
        print("\n2. Supabase Issues:")
        print("   - Verify project is active at supabase.com")
        print("   - Check DATABASE_URL format")
        print("   - Ensure password doesn't contain special characters")
        
        print("\n3. Environment Issues:")
        print("   - Restart VS Code/IDE")
        print("   - Deactivate and reactivate venv")
        print("   - Clear Python __pycache__ folders")
        
        print("\n4. Get Support:")
        print("   - Check Supabase status page")
        print("   - Try creating new Supabase project")
        print("   - Test with different network connection")
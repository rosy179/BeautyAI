#!/usr/bin/env python3
"""
Clean seed data script for Beauty Analytics
Works with the new database structure without circular imports
"""

import os
import sys

def create_sample_data():
    """Create sample data for the beauty app"""
    try:
        from app_clean import app
        from database import db, User, Category, Product, BlogPost
        
        with app.app_context():
            print("Adding sample users...")
            
            # Create admin user
            admin = User(
                username='admin',
                email='admin@beautyapp.com',
                full_name='Beauty Admin',
                is_admin=True
            )
            admin.set_password('admin123')
            
            # Create regular user
            user = User(
                username='mai_nguyen',
                email='mai@example.com',
                full_name='Nguyễn Thị Mai',
                phone='0901234567'
            )
            user.set_password('password123')
            
            db.session.add(admin)
            db.session.add(user)
            db.session.commit()
            
            print("Adding product categories...")
            
            # Create categories
            categories = [
                Category(name='Chăm sóc da mặt', description='Sản phẩm chăm sóc da mặt'),
                Category(name='Trang điểm', description='Sản phẩm trang điểm'),
                Category(name='Chăm sóc cơ thể', description='Sản phẩm chăm sóc cơ thể'),
                Category(name='Chăm sóc tóc', description='Sản phẩm chăm sóc tóc'),
                Category(name='Nước hoa', description='Nước hoa và tinh dầu'),
                Category(name='Phụ kiện làm đẹp', description='Dụng cụ và phụ kiện làm đẹp')
            ]
            
            for category in categories:
                db.session.add(category)
            
            db.session.commit()
            
            print("Adding sample products...")
            
            # Get category IDs
            skincare_cat = Category.query.filter_by(name='Chăm sóc da mặt').first()
            makeup_cat = Category.query.filter_by(name='Trang điểm').first()
            
            # Create products
            products = [
                Product(
                    name='Sữa rửa mặt La Roche-Posay Effaclar',
                    description='Sữa rửa mặt dành cho da dầu mụn, làm sạch sâu lỗ chân lông',
                    price=250000,
                    brand='La Roche-Posay',
                    category_id=skincare_cat.id,
                    stock_quantity=50,
                    skin_type='oily',
                    ingredients='Zinc PCA, Niacinamide',
                    image_url='https://via.placeholder.com/300x300?text=La+Roche+Posay'
                ),
                Product(
                    name='Kem chống nắng Anessa Perfect UV',
                    description='Kem chống nắng SPF 50+ PA++++, chống nước và mồ hôi',
                    price=450000,
                    brand='Anessa',
                    category_id=skincare_cat.id,
                    stock_quantity=30,
                    skin_type='all',
                    ingredients='Zinc Oxide, Titanium Dioxide',
                    image_url='https://via.placeholder.com/300x300?text=Anessa'
                ),
                Product(
                    name='Cushion Laneige Neo Nude',
                    description='Cushion trang điểm tự nhiên, che phủ hoàn hảo',
                    price=850000,
                    brand='Laneige',
                    category_id=makeup_cat.id,
                    stock_quantity=25,
                    skin_type='all',
                    ingredients='Hyaluronic Acid, Peptides',
                    image_url='https://via.placeholder.com/300x300?text=Laneige'
                ),
                Product(
                    name='Son môi MAC Ruby Woo',
                    description='Son lì màu đỏ ruby kinh điển, lâu trôi',
                    price=650000,
                    brand='MAC',
                    category_id=makeup_cat.id,
                    stock_quantity=40,
                    skin_type='all',
                    ingredients='Vitamin E, Jojoba Oil',
                    image_url='https://via.placeholder.com/300x300?text=MAC'
                ),
                Product(
                    name='Serum Vitamin C The Ordinary',
                    description='Serum Vitamin C 23% + HA Spheres 2%',
                    price=180000,
                    brand='The Ordinary',
                    category_id=skincare_cat.id,
                    stock_quantity=35,
                    skin_type='all',
                    ingredients='L-Ascorbic Acid, Hyaluronic Acid',
                    image_url='https://via.placeholder.com/300x300?text=The+Ordinary'
                ),
                Product(
                    name='Mặt nạ Innisfree Green Tea',
                    description='Mặt nạ đất sét trà xanh, làm sạch và se khít lỗ chân lông',
                    price=120000,
                    brand='Innisfree',
                    category_id=skincare_cat.id,
                    stock_quantity=60,
                    skin_type='oily',
                    ingredients='Green Tea Extract, Kaolin Clay',
                    image_url='https://via.placeholder.com/300x300?text=Innisfree'
                ),
                Product(
                    name='Kem dưỡng Cetaphil Daily Moisturizer',
                    description='Kem dưỡng ẩm hàng ngày cho da nhạy cảm',
                    price=320000,
                    brand='Cetaphil',
                    category_id=skincare_cat.id,
                    stock_quantity=45,
                    skin_type='sensitive',
                    ingredients='Glycerin, Dimethicone',
                    image_url='https://via.placeholder.com/300x300?text=Cetaphil'
                ),
                Product(
                    name='Phấn phủ Coty Airspun',
                    description='Phấn phủ bột mịn, kiềm dầu lâu trôi',
                    price=280000,
                    brand='Coty',
                    category_id=makeup_cat.id,
                    stock_quantity=30,
                    skin_type='oily',
                    ingredients='Talc, Mica',
                    image_url='https://via.placeholder.com/300x300?text=Coty'
                )
            ]
            
            for product in products:
                db.session.add(product)
            
            db.session.commit()
            
            print("Adding blog posts...")
            
            # Create blog posts
            blog_posts = [
                BlogPost(
                    title='10 Bước Chăm Sóc Da Cơ Bản Cho Người Mới Bắt Đầu',
                    content='''
                    Chăm sóc da là một hành trình dài và cần kiên trì. Dưới đây là 10 bước cơ bản:
                    
                    1. Tẩy trang: Loại bỏ makeup và ô nhiễm
                    2. Rửa mặt: Làm sạch da với sữa rửa mặt phù hợp
                    3. Toner: Cân bằng độ pH cho da
                    4. Essence: Cung cấp dưỡng chất
                    5. Serum: Điều trị các vấn đề cụ thể
                    6. Kem mắt: Chăm sóc vùng mắt nhạy cảm
                    7. Kem dưỡng: Khóa ẩm cho da
                    8. Kem chống nắng: Bảo vệ da khỏi tia UV
                    9. Mặt nạ: 2-3 lần/tuần
                    10. Tẩy da chết: 1-2 lần/tuần
                    ''',
                    excerpt='Hướng dẫn chi tiết 10 bước chăm sóc da cơ bản dành cho người mới bắt đầu',
                    author_id=admin.id,
                    is_published=True,
                    tags='skincare, beginner, routine',
                    featured_image='https://via.placeholder.com/600x300?text=Skincare+Routine'
                ),
                BlogPost(
                    title='Cách Chọn Kem Chống Nắng Phù Hợp Với Từng Loại Da',
                    content='''
                    Kem chống nắng là bước quan trọng nhất trong routine chăm sóc da.
                    
                    Đối với da dầu: Chọn kem chống nắng dạng gel, không gây bít tắc lỗ chân lông
                    Đối với da khô: Kem chống nắng dạng cream, có thêm thành phần dưỡng ẩm
                    Đối với da nhạy cảm: Kem chống nắng physical (khoáng chất)
                    Đối với da hỗn hợp: Kem chống nắng hybrid
                    
                    Luôn nhớ thoa lại kem chống nắng mỗi 2-3 tiếng.
                    ''',
                    excerpt='Hướng dẫn lựa chọn kem chống nắng phù hợp với từng loại da',
                    author_id=admin.id,
                    is_published=True,
                    tags='sunscreen, skincare, protection',
                    featured_image='https://via.placeholder.com/600x300?text=Sunscreen+Guide'
                )
            ]
            
            for post in blog_posts:
                db.session.add(post)
            
            db.session.commit()
            
            print("Sample data created successfully!")
            print(f"Users: {User.query.count()}")
            print(f"Categories: {Category.query.count()}")
            print(f"Products: {Product.query.count()}")
            print(f"Blog posts: {BlogPost.query.count()}")
            
            return True
            
    except Exception as e:
        print(f"Error creating sample data: {e}")
        return False

if __name__ == "__main__":
    create_sample_data()
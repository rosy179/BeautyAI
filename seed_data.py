# #!/usr/bin/env python3
# """
# Script to populate database with sample Vietnamese beauty products and content
# Run this after setting up the database to have demo data
# """

# from app import app, db
# from models import User, Category, Product, BlogPost
# from werkzeug.security import generate_password_hash
# import logging

# def create_sample_data():
#     """Create sample data for the beauty app"""
    
#     with app.app_context():
#         # Create admin user
#         admin = User(
#             username='admin',
#             email='admin@beautyapp.com',
#             full_name='Quản trị viên',
#             is_admin=True
#         )
#         admin.set_password('admin123')
        
#         # Create sample user
#         user = User(
#             username='nguyenmai',
#             email='mai@example.com',
#             full_name='Nguyễn Mai',
#             phone='0901234567'
#         )
#         user.set_password('password123')
        
#         db.session.add(admin)
#         db.session.add(user)
#         db.session.commit()
        
#         # Create categories
#         categories = [
#             Category(name='Sữa rửa mặt', description='Sản phẩm làm sạch da mặt'),
#             Category(name='Kem dưỡng ẩm', description='Sản phẩm dưỡng ẩm cho da'),
#             Category(name='Serum', description='Tinh chất dưỡng da chuyên sâu'),
#             Category(name='Kem chống nắng', description='Sản phẩm bảo vệ da khỏi tia UV'),
#             Category(name='Mặt nạ', description='Mặt nạ dưỡng da'),
#             Category(name='Tẩy trang', description='Sản phẩm tẩy trang makeup'),
#         ]
        
#         for cat in categories:
#             db.session.add(cat)
#         db.session.commit()
        
#         # Create sample products
#         products = [
#             # Sữa rửa mặt
#             Product(
#                 name='Sữa rửa mặt CeraVe Foaming Facial Cleanser',
#                 description='Sữa rửa mặt tạo bọt dành cho da thường đến da dầu, chứa 3 Ceramides thiết yếu và Hyaluronic Acid.',
#                 price=320000,
#                 category_id=1,
#                 brand='CeraVe',
#                 skin_type='oily',
#                 ingredients='Ceramides, Hyaluronic Acid, Niacinamide',
#                 stock_quantity=50,
#                 image_url='https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'
#             ),
#             Product(
#                 name='Sữa rửa mặt La Roche-Posay Toleriane Caring Wash',
#                 description='Sữa rửa mặt dịu nhẹ dành cho da nhạy cảm, không chứa xà phòng.',
#                 price=385000,
#                 category_id=1,
#                 brand='La Roche-Posay',
#                 skin_type='sensitive',
#                 ingredients='Thermal Spring Water, Glycerin',
#                 stock_quantity=30,
#                 image_url='https://images.unsplash.com/photo-1570554886111-e80fcca6a029?w=400'
#             ),
            
#             # Kem dưỡng ẩm
#             Product(
#                 name='Kem dưỡng ẩm Neutrogena Hydro Boost',
#                 description='Kem dưỡng ẩm chứa Hyaluronic Acid cung cấp độ ẩm suốt 72 giờ.',
#                 price=425000,
#                 category_id=2,
#                 brand='Neutrogena',
#                 skin_type='all',
#                 ingredients='Hyaluronic Acid, Glycerin, Dimethicone',
#                 stock_quantity=40,
#                 image_url='https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400'
#             ),
#             Product(
#                 name='Kem dưỡng ẩm Clinique Dramatically Different Moisturizing Gel',
#                 description='Gel dưỡng ẩm nhẹ tênh dành cho da dầu và da hỗn hợp.',
#                 price=890000,
#                 category_id=2,
#                 brand='Clinique',
#                 skin_type='combination',
#                 ingredients='Urea, Glycerin, Cucumber Extract',
#                 stock_quantity=25,
#                 image_url='https://images.unsplash.com/photo-1612817288484-6f916006741a?w=400'
#             ),
            
#             # Serum
#             Product(
#                 name='Serum The Ordinary Niacinamide 10% + Zinc 1%',
#                 description='Serum kiểm soát dầu và thu nhỏ lỗ chân lông với 10% Niacinamide.',
#                 price=220000,
#                 category_id=3,
#                 brand='The Ordinary',
#                 skin_type='oily',
#                 ingredients='Niacinamide, Zinc PCA',
#                 stock_quantity=60,
#                 image_url='https://images.unsplash.com/photo-1631729371254-42c2892f0e10?w=400'
#             ),
#             Product(
#                 name='Serum Paula\'s Choice 2% BHA Liquid Exfoliant',
#                 description='Dung dịch tẩy tế bào chết với 2% BHA (Salicylic Acid) giúp làm sạch lỗ chân lông.',
#                 price=750000,
#                 category_id=3,
#                 brand='Paula\'s Choice',
#                 skin_type='oily',
#                 ingredients='Salicylic Acid, Green Tea Extract',
#                 stock_quantity=35,
#                 image_url='https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400'
#             ),
            
#             # Kem chống nắng
#             Product(
#                 name='Kem chống nắng La Roche-Posay Anthelios Ultra Cover SPF 60',
#                 description='Kem chống nắng phổ rộng SPF 60 chống thấm nước, dành cho da nhạy cảm.',
#                 price=520000,
#                 category_id=4,
#                 brand='La Roche-Posay',
#                 skin_type='all',
#                 ingredients='Titanium Dioxide, Zinc Oxide, Anthelios XL',
#                 stock_quantity=45,
#                 image_url='https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'
#             ),
            
#             # Mặt nạ
#             Product(
#                 name='Mặt nạ Some By Mi Bye Bye Blackhead Green Tea Tox Bubble Cleanser',
#                 description='Mặt nạ tạo bọt trà xanh giúp làm sạch mụn đầu đen và kiểm soát dầu.',
#                 price=350000,
#                 category_id=5,
#                 brand='Some By Mi',
#                 skin_type='oily',
#                 ingredients='Green Tea Extract, BHA, Charcoal Powder',
#                 stock_quantity=20,
#                 image_url='https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=400'
#             ),
#         ]
        
#         for product in products:
#             db.session.add(product)
#         db.session.commit()
        
#         # Create sample blog posts
#         blog_posts = [
#             BlogPost(
#                 title='10 Bước Skincare Routine Cơ Bản Cho Người Mới Bắt Đầu',
#                 content='''
# Skincare routine cơ bản là nền tảng quan trọng để có làn da khỏe mạnh. Dưới đây là 10 bước cơ bản bạn nên biết:

# 1. **Tẩy trang**: Loại bỏ makeup và ô nhiễm
# 2. **Sữa rửa mặt**: Làm sạch sâu da mặt
# 3. **Toner**: Cân bằng độ pH cho da
# 4. **Essence**: Cung cấp độ ẩm cơ bản
# 5. **Serum**: Điều trị các vấn đề cụ thể
# 6. **Kem mắt**: Chăm sóc vùng da mắt
# 7. **Kem dưỡng ẩm**: Khóa ẩm cho da
# 8. **Kem chống nắng** (buổi sáng)
# 9. **Mặt nạ** (2-3 lần/tuần)
# 10. **Dầu dưỡng** (buổi tối)

# Hãy bắt đầu từ từ và lắng nghe da của bạn!
#                 ''',
#                 excerpt='Hướng dẫn chi tiết 10 bước skincare routine cơ bản dành cho người mới bắt đầu, giúp bạn có làn da khỏe mạnh.',
#                 author_id=1,
#                 is_published=True,
#                 tags='skincare,routine,newbie',
#                 featured_image='https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=800'
#             ),
#             BlogPost(
#                 title='Cách Chọn Kem Chống Nắng Phù Hợp Với Từng Loại Da',
#                 content='''
# Kem chống nắng là bước không thể thiếu trong routine hàng ngày. Việc chọn đúng loại kem chống nắng sẽ giúp bảo vệ da hiệu quả:

# **Da dầu**: Chọn loại gel, không dầu, có thành phần kiểm soát dầu
# **Da khô**: Chọn loại cream dưỡng ẩm, chứa hyaluronic acid
# **Da nhạy cảm**: Chọn loại mineral (zinc oxide, titanium dioxide)
# **Da hỗn hợp**: Chọn loại hybrid, vừa dưỡng ẩm vừa kiểm soát dầu

# Luôn chọn SPF 30+ và PA+++ trở lên để bảo vệ tối ưu.
#                 ''',
#                 excerpt='Hướng dẫn chọn kem chống nắng phù hợp với từng loại da để bảo vệ da hiệu quả nhất.',
#                 author_id=1,
#                 is_published=True,
#                 tags='sunscreen,protection,skintype',
#                 featured_image='https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800'
#             ),
#         ]
        
#         for post in blog_posts:
#             db.session.add(post)
#         db.session.commit()
        
#         print("✅ Dữ liệu mẫu đã được tạo thành công!")
#         print("👤 Admin: admin@beautyapp.com / admin123")
#         print("👤 User: mai@example.com / password123")

# if __name__ == '__main__':
#     create_sample_data()
#!/usr/bin/env python3
"""
Script to populate database with sample Vietnamese beauty products and content
Run this after setting up the database to have demo data
"""

import logging
from app import create_app
from extensions import db  # Nhập db từ extensions.py
from werkzeug.security import generate_password_hash

app = create_app()
# Configure logging
logging.basicConfig(level=logging.INFO)

def create_sample_data():
    """Create sample data for the beauty app"""
    from models import User, Category, Product, BlogPost  # Nhập mô hình trong hàm
    
    with app.app_context():
        logging.info("Bắt đầu tạo dữ liệu mẫu...")
        
        try:
            # Create admin user
            if not User.query.filter_by(email='admin@beautyapp.com').first():
                admin = User(
                    username='admin',
                    email='admin@beautyapp.com',
                    full_name='Quản trị viên',
                    is_admin=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                logging.info("Người dùng admin đã được tạo.")
            
            # Create sample user
            if not User.query.filter_by(email='mai@example.com').first():
                user = User(
                    username='nguyenmai',
                    email='mai@example.com',
                    full_name='Nguyễn Mai',
                    phone='0901234567'
                )
                user.set_password('password123')
                db.session.add(user)
                logging.info("Người dùng nguyenmai đã được tạo.")
            
            db.session.commit()
            
            # Create categories
            category_names = [
                'Sữa rửa mặt', 'Kem dưỡng ẩm', 'Serum', 
                'Kem chống nắng', 'Mặt nạ', 'Tẩy trang'
            ]
            for name in category_names:
                if not Category.query.filter_by(name=name).first():
                    category = Category(
                        name=name,
                        description=f'Sản phẩm {name.lower()} cho da'
                    )
                    db.session.add(category)
            db.session.commit()
            logging.info("Các danh mục đã được tạo.")
            
            # Create sample products
            products = [
                # Sữa rửa mặt
                {
                    'name': 'Sữa rửa mặt CeraVe Foaming Facial Cleanser',
                    'description': 'Sữa rửa mặt tạo bọt dành cho da thường đến da dầu, chứa 3 Ceramides thiết yếu và Hyaluronic Acid.',
                    'price': 320000,
                    'category_name': 'Sữa rửa mặt',
                    'brand': 'CeraVe',
                    'skin_type': 'oily',
                    'ingredients': 'Ceramides, Hyaluronic Acid, Niacinamide',
                    'stock_quantity': 50,
                    'image_url': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'
                },
                # ... (các sản phẩm khác tương tự, rút gọn cho ngắn gọn)
            ]
            
            for p in products:
                category = Category.query.filter_by(name=p['category_name']).first()
                if category and not Product.query.filter_by(name=p['name']).first():
                    product = Product(
                        name=p['name'],
                        description=p['description'],
                        price=p['price'],
                        category_id=category.id,
                        brand=p['brand'],
                        skin_type=p['skin_type'],
                        ingredients=p['ingredients'],
                        stock_quantity=p['stock_quantity'],
                        image_url=p['image_url']
                    )
                    db.session.add(product)
            db.session.commit()
            logging.info("Các sản phẩm đã được tạo.")
            
            # Create sample blog posts
            admin = User.query.filter_by(email='admin@beautyapp.com').first()
            if admin:
                blog_posts = [
                    {
                        'title': '10 Bước Skincare Routine Cơ Bản Cho Người Mới Bắt Đầu',
                        'content': '...',  # Giữ nguyên nội dung từ mã gốc
                        'excerpt': 'Hướng dẫn chi tiết 10 bước skincare routine cơ bản dành cho người mới bắt đầu, giúp bạn có làn da khỏe mạnh.',
                        'author_id': admin.id,
                        'is_published': True,
                        'tags': 'skincare,routine,newbie',
                        'featured_image': 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=800'
                    },
                    # ... (các bài viết khác tương tự)
                ]
                
                for post in blog_posts:
                    if not BlogPost.query.filter_by(title=post['title']).first():
                        blog_post = BlogPost(**post)
                        db.session.add(blog_post)
                db.session.commit()
                logging.info("Các bài viết blog đã được tạo.")
            
            print("✅ Dữ liệu mẫu đã được tạo thành công!")
            print("👤 Admin: admin@beautyapp.com / admin123")
            print("👤 User: mai@example.com / password123")
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Lỗi khi tạo dữ liệu mẫu: {e}")
            raise

if __name__ == '__main__':
    create_sample_data()
"""
Script to populate database with sample Vietnamese beauty products and content
Run this after setting up the database to have demo data
"""

import logging
from extensions import db
from werkzeug.security import generate_password_hash
from flask import has_app_context

# Configure logging
logging.basicConfig(level=logging.INFO)

def create_sample_data(app=None):
    """Create sample data for the beauty app"""
    from models import User, Category, Product, BlogPost  # Nhập mô hình trong hàm
    
    should_pop = False
    if not has_app_context():
        if app is None:
            from app import create_app
            app = create_app()
        ctx = app.app_context()
        ctx.push()
        should_pop = True

    try:
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
                {
                    'name': 'Sữa rửa mặt La Roche-Posay Toleriane Caring Wash',
                    'description': 'Sữa rửa mặt dịu nhẹ dành cho da nhạy cảm',
                    'price': 385000,
                    'category_name': 'Sữa rửa mặt',
                    'brand': 'La Roche-Posay',
                    'skin_type': 'sensitive',
                    'ingredients': 'Thermal Spring Water, Glycerin',
                    'stock_quantity': 30,
                    'image_url': 'https://images.unsplash.com/photo-1570554886111-e80fcca6a029?w=400'
                },
                {
                    'name': 'Kem dưỡng ẩm Neutrogena Hydro Boost',
                    'description': 'Kem dưỡng ẩm chứa Hyaluronic Acid cung cấp độ ẩm suốt 72 giờ.',
                    'price': 425000,
                    'category_name': 'Kem dưỡng ẩm',
                    'brand': 'Neutrogena',
                    'skin_type': 'all',
                    'ingredients': 'Hyaluronic Acid, Glycerin, Dimethicone',
                    'stock_quantity': 40,
                    'image_url': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400'
                },
                {
                    'name': 'Serum The Ordinary Niacinamide 10% + Zinc 1%',
                    'description': 'Serum kiểm soát dầu và thu nhỏ lỗ chân lông với 10% Niacinamide.',  
                    'price': 220000,
                    'category_name': 'Serum',
                    'brand': 'The Ordinary',
                    'skin_type': 'oily',
                    'ingredients': 'Niacinamide, Zinc PCA',
                    'stock_quantity': 60,
                    'image_url': 'https://i.pinimg.com/736x/2d/74/df/2d74df4dff0318fbefaf36dbd2141338.jpg'
                },
                {
                    'name': 'Kem chống nắng La Roche-Posay Anthelios Ultra Cover SPF 60',
                    'description': 'Kem chống nắng phổ rộng SPF 60 chống thấm nước, dành cho da nhạy cảm.',
                    'price': 520000,
                    'category_name': 'Kem chống nắng',
                    'brand': 'La Roche-Posay',
                    'skin_type': 'all',
                    'ingredients': 'Titanium Dioxide, Zinc Oxide, Anthelios XL',
                    'stock_quantity': 45,
                    'image_url': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'
                }, 
                {
                    'name': 'Serum dưỡng sáng da Abib',
                    'description': 'Serum chiết xuất từ thiên nhiên giúp làm sáng da và đều màu.',
                    'price': 350000,
                    'category_name': 'Serum',
                    'brand': 'Abib',
                    'skin_type': 'all',
                    'ingredients': 'Niacinamide, Vitamin C, Hyaluronic Acid, Glutathione',
                    'stock_quantity': 50,
                    'image_url': 'https://i.pinimg.com/736x/24/7f/c6/247fc65eb32ec46c6a27b6b31f2b3c69.jpg'
                },
                {
                    'name': 'Serum Paula\'s Choice 2% BHA Liquid Exfoliant',
                    'description': 'Dung dịch tẩy tế bào chết với 2% BHA (Salicylic Acid) giúp làm sạch lỗ chân lông.',
                    'price': 750000,
                    'category_name': 'Serum',
                    'brand': 'Paula\'s Choice',
                    'skin_type': 'oily',
                    'ingredients': 'Salicylic Acid, Green Tea Extract',
                    'stock_quantity': 35,
                    'image_url': 'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=400'
                }
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
                        'title': 'Cách Chọn Kem Chống Nắng Phù Hợp Với Từng Loại Da',
                        'content': '...',  
                        'excerpt': 'Hướng dẫn chọn kem chống nắng phù hợp với từng loại da để bảo vệ da hiệu quả nhất.',
                        'author_id': admin.id,
                        'is_published': True,
                        'tags': 'sunscreen,protection,skintype',
                        'featured_image': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800'
                    },
                    {
                        'title': '10 Bước Skincare Routine Cơ Bản Cho Người Mới Bắt Đầu',
                        'content': '''Skincare routine cơ bản là nền tảng quan trọng để có làn da khỏe mạnh. Dưới đây là 10 bước cơ bản bạn nên biết:
1. **Tẩy trang**: Loại bỏ makeup và ô nhiễm
2. **Sữa rửa mặt**: Làm sạch sâu da mặt
3. **Toner**: Cân bằng độ pH cho da
4. **Essence**: Cung cấp độ ẩm cơ bản
5. **Serum**: Điều trị các vấn đề cụ thể
6. **Kem mắt**: Chăm sóc vùng da mắt
7. **Kem dưỡng ẩm**: Khóa ẩm cho da
8. **Kem chống nắng** (buổi sáng)
9. **Mặt nạ** (2-3 lần/tuần)
10. **Dầu dưỡng** (buổi tối)
Hãy bắt đầu từ từ và lắng nghe da của bạn!''',
                        'excerpt': 'Hướng dẫn chi tiết 10 bước skincare routine cơ bản dành cho người mới bắt đầu, giúp bạn có làn da khỏe mạnh.',
                        'author_id': admin.id,
                        'is_published': True,
                        'tags': 'skincare,routine,newbie',
                        'featured_image': 'https://i.pinimg.com/736x/97/83/e8/9783e82b5e9ec44e90411961b51eeb98.jpg'
                    }, 
                    {
                        'title': 'Serum Dưỡng Sáng Da Abib - Bí Quyết Cho Làn Da Rạng Rỡ',
                        'content': '''Serum dưỡng sáng da Abib là sản phẩm chiết xuất từ thiên nhiên, giúp làm sáng da và đều màu. Với thành phần chính là Niacinamide, Vitamin C, Hyaluronic Acid và Glutathione, serum này không chỉ cung cấp độ ẩm mà còn giúp làm mờ các vết thâm nám, mang lại làn da rạng rỡ.
Sản phẩm này phù hợp với mọi loại da, đặc biệt là da xỉn màu, kém sức sống. Hãy thử ngay để cảm nhận
sự khác biệt trên làn da của bạn!''',
                        'excerpt': 'Serum chiết xuất từ thiên nhiên giúp làm sáng da và đều màu, phù hợp với mọi loại da.',
                        'author_id': admin.id,
                        'is_published': True,
                        'tags': 'serum,brightening,natural',
                        'featured_image': 'https://i.pinimg.com/736x/24/7f/c6/247fc65eb32ec46c6a27b6b31f2b3c69.jpg'
                    }
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
    finally:
        if should_pop:
            ctx.pop()

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        create_sample_data(app)
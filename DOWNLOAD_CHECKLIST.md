# Beauty Analytics - Download Checklist

## ✅ Files cần download (tất cả files sau)

### 📄 Hướng dẫn và cấu hình
- [ ] `README.md` - Hướng dẫn tổng quan
- [ ] `SETUP.md` - Hướng dẫn cài đặt chi tiết  
- [ ] `DOWNLOAD_GUIDE.md` - Hướng dẫn download và chạy
- [ ] `SUPABASE_SETUP.md` - Cài đặt Supabase database
- [ ] `PROJECT_STRUCTURE.md` - Cấu trúc thư mục
- [ ] `DOWNLOAD_CHECKLIST.md` - File này
- [ ] `.env.example` - Template cấu hình môi trường
- [ ] `dependencies.txt` - Danh sách Python packages

### 🐍 Python source code
- [ ] `main.py` - Entry point chính
- [ ] `app.py` - Flask app initialization
- [ ] `models.py` - Database models  
- [ ] `routes.py` - API endpoints
- [ ] `forms.py` - Form definitions
- [ ] `face_analysis.py` - Face++ integration
- [ ] `run_local.py` - Development server
- [ ] `deploy_config.py` - Deploy configuration
- [ ] `seed_data.py` - Sample data creation

### 🎨 Frontend assets
#### CSS
- [ ] `static/css/beauty.css` - Main stylesheet

#### JavaScript
- [ ] `static/js/main.js` - Core JavaScript
- [ ] `static/js/chat.js` - Chat functionality
- [ ] `static/js/skin-analysis.js` - Camera and analysis

#### Uploads folder
- [ ] `static/uploads/` - Folder for uploaded images (tạo thư mục trống)

### 🌐 HTML Templates
#### Main templates
- [ ] `templates/base.html` - Base layout
- [ ] `templates/index.html` - Homepage
- [ ] `templates/skin_analysis.html` - Skin analysis page
- [ ] `templates/products.html` - Product listing
- [ ] `templates/product_detail.html` - Product details
- [ ] `templates/cart.html` - Shopping cart
- [ ] `templates/checkout.html` - Checkout page
- [ ] `templates/chat.html` - Chat interface
- [ ] `templates/blog.html` - Blog listing
- [ ] `templates/blog_post.html` - Blog post details
- [ ] `templates/profile.html` - User profile

#### Auth templates
- [ ] `templates/auth/login.html` - Login page
- [ ] `templates/auth/register.html` - Registration page

## 🚀 Sau khi download xong

### 1. Tạo thư mục và copy files
```bash
mkdir beauty-analytics
cd beauty-analytics
# Copy tất cả files vào thư mục này theo đúng cấu trúc
```

### 2. Tạo thư mục cần thiết
```bash
mkdir -p static/uploads
mkdir -p instance
```

### 3. Cài đặt Python environment
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r dependencies.txt
```

### 4. Cấu hình môi trường
```bash
cp .env.example .env
# Chỉnh sửa .env với thông tin database và API keys của bạn
```

### 5. Khởi tạo database
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
python seed_data.py
```

### 6. Chạy ứng dụng
```bash
python run_local.py
```

## 🔑 API Keys cần có

### Bắt buộc (để phân tích da hoạt động)
- [ ] **FACEPP_API_KEY** - Đăng ký tại https://www.faceplusplus.com
- [ ] **FACEPP_API_SECRET** - Từ Face++ dashboard

### Database (chọn 1 trong 2)
- [ ] **Supabase**: DATABASE_URL từ https://supabase.com (khuyên dùng)
- [ ] **PostgreSQL local**: Cài PostgreSQL và tạo database

### Tùy chọn
- [ ] **STRIPE_SECRET_KEY** - Cho thanh toán (nếu cần)
- [ ] **OPENAI_API_KEY** - Cho chat AI nâng cao (nếu cần)

## ⚠️ Lưu ý quan trọng

1. **Không bỏ sót file nào** - Tất cả files trên đều cần thiết
2. **Giữ đúng cấu trúc thư mục** - Đặt files đúng vị trí
3. **Tạo file .env** - Copy từ .env.example và điền thông tin
4. **Cài đủ dependencies** - Chạy pip install -r dependencies.txt
5. **Khởi tạo database** - Chạy seed_data.py để có dữ liệu mẫu

## 🔧 Test sau khi cài đặt

```bash
# Test database connection
python -c "from app import db; print('Database OK')"

# Test Face++ API
python -c "from face_analysis import FaceAnalyzer; print('Face++ OK' if FaceAnalyzer().api_key else 'Missing API Key')"

# Run server
python run_local.py
```

Truy cập http://localhost:5000 để kiểm tra ứng dụng hoạt động.

## 📞 Hỗ trợ

Nếu gặp lỗi:
1. Kiểm tra file .env có đầy đủ thông tin
2. Đảm bảo đã cài đặt tất cả dependencies
3. Kiểm tra database connection
4. Xem logs trong terminal để debug
# Cấu trúc thư mục Beauty Analytics

## 📁 Cấu trúc hoàn chỉnh của project

```
beauty-analytics/
├── 📄 README.md                    # Hướng dẫn tổng quan
├── 📄 SETUP.md                     # Hướng dẫn cài đặt chi tiết
├── 📄 DOWNLOAD_GUIDE.md            # Hướng dẫn download và chạy
├── 📄 SUPABASE_SETUP.md            # Hướng dẫn cài đặt Supabase
├── 📄 PROJECT_STRUCTURE.md         # File này - cấu trúc project
│
├── 🔧 .env.example                 # Mẫu file cấu hình môi trường
├── 📄 dependencies.txt             # Danh sách Python packages
├── 🐍 run_local.py                 # Script chạy server development
├── 🐍 deploy_config.py             # Cấu hình deploy tự động
├── 🐍 seed_data.py                 # Script tạo dữ liệu mẫu
│
├── 🐍 main.py                      # Entry point chính
├── 🐍 app.py                       # Khởi tạo Flask app
├── 🐍 models.py                    # Database models
├── 🐍 routes.py                    # API endpoints và views
├── 🐍 forms.py                     # Form definitions (WTForms)
├── 🐍 face_analysis.py             # Face++ API integration
│
├── 📁 static/                      # Files tĩnh (CSS, JS, images)
│   ├── 📁 css/
│   │   └── 🎨 beauty.css          # CSS chính của ứng dụng
│   ├── 📁 js/
│   │   ├── 🔧 main.js             # JavaScript chính
│   │   ├── 💬 chat.js             # Chat functionality
│   │   └── 📸 skin-analysis.js    # Camera và phân tích da
│   └── 📁 uploads/                # Thư mục lưu ảnh upload
│       └── (ảnh do người dùng upload)
│
├── 📁 templates/                   # HTML templates (Jinja2)
│   ├── 🌐 base.html               # Template gốc
│   ├── 🏠 index.html              # Trang chủ
│   ├── 📸 skin_analysis.html      # Trang phân tích da
│   ├── 🛒 products.html           # Danh sách sản phẩm
│   ├── 🛒 product_detail.html     # Chi tiết sản phẩm
│   ├── 🛒 cart.html               # Giỏ hàng
│   ├── 💳 checkout.html           # Thanh toán
│   ├── 💬 chat.html               # Chat tư vấn
│   ├── 📝 blog.html               # Danh sách blog
│   ├── 📝 blog_post.html          # Chi tiết bài blog
│   ├── 👤 profile.html            # Trang cá nhân
│   └── 📁 auth/                   # Templates đăng nhập
│       ├── 🔐 login.html
│       └── 📝 register.html
│
└── 📁 instance/                   # Database files (SQLite nếu dùng local)
    └── beauty_app.db              # SQLite database (optional)
```

## 📋 Mô tả chi tiết các files

### 🔧 Files cấu hình

- **`.env.example`**: Template cho file `.env` với tất cả biến môi trường cần thiết
- **`dependencies.txt`**: Danh sách Python packages cần cài đặt
- **`deploy_config.py`**: Tự động detect và cấu hình database (Supabase/Local/Heroku)

### 🐍 Python files chính

- **`main.py`**: Entry point - chạy file này để start server
- **`app.py`**: Khởi tạo Flask app, database, login manager
- **`models.py`**: Định nghĩa database tables (User, Product, Order, etc.)
- **`routes.py`**: Tất cả API endpoints và view functions
- **`forms.py`**: Form validation với WTForms
- **`face_analysis.py`**: Tích hợp Face++ API cho phân tích da

### 🎨 Frontend files

- **`static/css/beauty.css`**: Styles chính với Bootstrap theme
- **`static/js/main.js`**: JavaScript utilities và interactions
- **`static/js/chat.js`**: Chat functionality với AI
- **`static/js/skin-analysis.js`**: Camera capture và skin analysis

### 🌐 Templates

- **`base.html`**: Layout chung với navigation, footer
- **`skin_analysis.html`**: Trang phân tích da với camera và upload
- **`products.html`**: E-commerce product listing
- **`chat.html`**: AI beauty consultation chatbot

### 🗄️ Database

- Hỗ trợ cả Supabase (cloud) và PostgreSQL local
- Auto-migration khi chạy lần đầu
- Sample data với sản phẩm mỹ phẩm Việt Nam

## 🚀 Cách download và chạy

### Bước 1: Download project

Tải toàn bộ thư mục `beauty-analytics/` về máy tính

### Bước 2: Cài đặt dependencies

```bash
cd beauty-analytics
python -3.11 -m venv venv
venv\Scripts\activate  # Windows
pip install -r dependencies.txt
```

### Bước 3: Cấu hình database

```bash
# Tạo file .env từ mẫu
cp .env.example .env
# Chỉnh sửa .env với thông tin database và API keys
```

### Bước 4: Khởi tạo database

```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
python seed_data.py  # Tạo dữ liệu mẫu
```

### Bước 5: Chạy server

```bash
python run_local.py
# Hoặc
python main.py
```

Truy cập: http://localhost:5000

## 🔑 API Keys cần thiết

### Bắt buộc:

- **FACEPP_API_KEY**: Đăng ký tại faceplusplus.com
- **FACEPP_API_SECRET**: Từ Face++ dashboard
- **DATABASE_URL**: Supabase hoặc PostgreSQL local

### Tùy chọn:

- **STRIPE_SECRET_KEY**: Cho thanh toán online
- **OPENAI_API_KEY**: Cho chat AI nâng cao

## 📦 Packages chính được sử dụng

```
Flask==2.3.3              # Web framework
Flask-SQLAlchemy==3.0.5   # ORM database
Flask-Login==0.6.3        # User authentication
Flask-WTF==1.1.1          # Form handling
psycopg2-binary==2.9.7    # PostgreSQL adapter
requests==2.31.0          # HTTP client cho APIs
gunicorn==21.2.0          # WSGI server
python-dotenv==1.0.0      # Environment variables
```

## 🎯 Tính năng chính

1. **Phân tích da AI** - Face++ integration với camera/upload
2. **E-commerce** - Sản phẩm mỹ phẩm, giỏ hàng, thanh toán
3. **Chat tư vấn** - AI beauty advisor
4. **Blog làm đẹp** - Content management system
5. **User management** - Đăng ký, đăng nhập, profile
6. **Admin panel** - Quản lý sản phẩm, đơn hàng

## 🔧 Customization

### Thêm sản phẩm mới:

Chỉnh sửa `seed_data.py` hoặc thêm qua admin panel

### Thay đổi giao diện:

Chỉnh sửa `static/css/beauty.css` và templates

### Thêm tính năng mới:

1. Thêm route trong `routes.py`
2. Tạo template mới trong `templates/`
3. Thêm JavaScript nếu cần trong `static/js/`

Project này sẵn sàng để deploy lên Heroku, Railway, hoặc VPS với Supabase database!

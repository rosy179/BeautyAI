# Hướng dẫn Cài đặt Chi tiết - Beauty Analytics

## 🔧 Cài đặt Nhanh (Quick Setup)

### Bước 1: Tải về project
```bash
# Tải về từ GitHub hoặc giải nén file zip
git clone <repository-url>
cd beauty-analytics
```

### Bước 2: Cài đặt Python dependencies
```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Cài đặt từ file dependencies.txt
pip install -r dependencies.txt
```

### Bước 3: Cấu hình Database
```bash
# Cài đặt PostgreSQL (nếu chưa có)
# Windows: Tải từ https://www.postgresql.org/download/windows/
# macOS: brew install postgresql
# Ubuntu: sudo apt install postgresql postgresql-contrib

# Tạo database
createdb beauty_app

# Hoặc qua psql:
psql -U postgres
CREATE DATABASE beauty_app;
\q
```

### Bước 4: Cấu hình môi trường
```bash
# Sao chép file cấu hình
cp .env.example .env

# Chỉnh sửa file .env với editor yêu thích
nano .env
```

### Bước 5: Khởi tạo database
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Thêm dữ liệu mẫu (tùy chọn)
python seed_data.py
```

### Bước 6: Chạy ứng dụng
```bash
python main.py
```

## 🔑 Cấu hình API Keys Chi tiết

### 1. Face++ API (Bắt buộc cho phân tích da)

1. **Đăng ký tài khoản**:
   - Truy cập: https://www.faceplusplus.com
   - Click "Sign Up" ở góc phải trên
   - Điền thông tin và xác nhận email

2. **Tạo Application**:
   - Đăng nhập vào Console
   - Click "Create a new App"
   - Điền tên app: "Beauty Analytics"
   - Chọn loại: "Non-Commercial"

3. **Lấy API Keys**:
   - Trong Dashboard, copy API Key và API Secret
   - Thêm vào file `.env`:
   ```
   FACEPP_API_KEY=your_api_key_here
   FACEPP_API_SECRET=your_api_secret_here
   ```

4. **Test API**:
   ```bash
   python -c "
   import os
   print('API Key:', os.environ.get('FACEPP_API_KEY', 'Not found'))
   print('API Secret:', os.environ.get('FACEPP_API_SECRET', 'Not found'))
   "
   ```

### 2. Stripe Payment (Tùy chọn cho thanh toán)

1. **Đăng ký Stripe**:
   - Truy cập: https://stripe.com
   - Click "Start now" và đăng ký

2. **Lấy Test Keys**:
   - Vào Dashboard → Developers → API keys
   - Copy "Secret key" (bắt đầu với `sk_test_`)
   - Thêm vào `.env`:
   ```
   STRIPE_SECRET_KEY=sk_test_your_secret_key_here
   ```

### 3. OpenAI API (Tùy chọn cho chatbot nâng cao)

1. **Đăng ký OpenAI**:
   - Truy cập: https://platform.openai.com
   - Đăng ký và xác nhận tài khoản

2. **Tạo API Key**:
   - Vào API keys section
   - Click "Create new secret key"
   - Copy và thêm vào `.env`:
   ```
   OPENAI_API_KEY=sk-your_openai_key_here
   ```

## 🗃️ Cấu hình Database Chi tiết

### PostgreSQL Local

Cấu hình database local trong file `.env`:

```bash
# Database PostgreSQL cục bộ
DATABASE_URL=postgresql://username:password@localhost:5432/beauty_app
PGHOST=localhost
PGPORT=5432
PGUSER=postgres
PGPASSWORD=your_postgres_password
PGDATABASE=beauty_app
```

### PostgreSQL Cloud (Heroku/Railway/Supabase)

Nếu sử dụng cloud database, chỉ cần thay `DATABASE_URL`:

```bash
# Ví dụ Heroku
DATABASE_URL=postgres://user:pass@host:5432/dbname

# Ví dụ Supabase
DATABASE_URL=postgresql://postgres:password@db.project.supabase.co:5432/postgres
```

## 🚀 Deploy Production

### Heroku

```bash
# Cài đặt Heroku CLI
# Tạo app
heroku create beauty-analytics-app

# Set environment variables
heroku config:set FACEPP_API_KEY=your_key
heroku config:set FACEPP_API_SECRET=your_secret
heroku config:set FLASK_SECRET_KEY=your_secret

# Deploy
git push heroku main
```

### VPS/Server

```bash
# Cài đặt dependencies
sudo apt update
sudo apt install python3-pip postgresql nginx

# Clone project
git clone <repository>
cd beauty-analytics

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r dependencies.txt

# Setup nginx
sudo nano /etc/nginx/sites-available/beauty-analytics
# [Cấu hình nginx proxy]

# Run with gunicorn
gunicorn --bind 0.0.0.0:8000 main:app
```

## 🔧 Troubleshooting

### Lỗi thường gặp

1. **Database connection failed**:
   ```bash
   # Kiểm tra PostgreSQL
   sudo service postgresql status
   sudo service postgresql start
   ```

2. **Face++ API không hoạt động**:
   - Kiểm tra API keys trong `.env`
   - Kiểm tra kết nối internet
   - Kiểm tra quota API

3. **Camera không hoạt động**:
   - Dùng HTTPS trong production
   - Cho phép camera access trên browser
   - Kiểm tra camera không bị chiếm dụng

4. **File upload không hoạt động**:
   ```bash
   # Tạo thư mục uploads
   mkdir -p static/uploads
   chmod 755 static/uploads
   ```

### Kiểm tra hệ thống

```bash
# Test database connection
python -c "from app import db; print('Database OK' if db else 'Database Error')"

# Test Face++ API
python -c "
from face_analysis import FaceAnalyzer
analyzer = FaceAnalyzer()
print('Face++ OK' if analyzer.api_key else 'Face++ Missing')
"
```

## 📝 Scripts Hữu ích

### Reset Database
```bash
python -c "
from app import app, db
with app.app_context():
    db.drop_all()
    db.create_all()
print('Database reset complete')
"
```

### Create Admin User
```bash
python -c "
from app import app, db
from models import User
with app.app_context():
    admin = User(username='admin', email='admin@example.com', is_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
print('Admin user created')
"
```

### Backup Database
```bash
pg_dump beauty_app > backup_$(date +%Y%m%d).sql
```

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra logs trong console
2. Xem file README.md
3. Kiểm tra cấu hình trong file `.env`
4. Tạo issue trên GitHub repository
# Hướng dẫn Download và Cài đặt Beauty Analytics

## 📥 Tải về Project

### Phương án 1: Download ZIP (Khuyên dùng)
1. Tải file ZIP chứa toàn bộ source code
2. Giải nén vào thư mục mong muốn
3. Mở terminal/command prompt tại thư mục đó

### Phương án 2: Git Clone
```bash
git clone <repository-url>
cd beauty-analytics
```

## 🛠️ Cài đặt Nhanh (5 phút)

### Bước 1: Cài đặt Python packages
```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Cài đặt dependencies
pip install -r dependencies.txt
```

### Bước 2: Chọn Database (2 tùy chọn)

#### Tùy chọn A: Supabase (Khuyên dùng - Miễn phí, Cloud)
1. Đăng ký tại: https://supabase.com
2. Tạo project mới với tên "Beauty Analytics"
3. Chọn region Singapore (gần Việt Nam)
4. Tạo password mạnh cho database
5. Copy connection string từ Settings → Database
6. Xem chi tiết trong file `SUPABASE_SETUP.md`

#### Tùy chọn B: PostgreSQL Local
**Windows:**
- Tải PostgreSQL từ: https://www.postgresql.org/download/windows/
- Chạy installer và nhớ mật khẩu postgres

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Linux:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo service postgresql start
```

### Bước 3: Cấu hình Database Connection

#### Với Supabase:
```bash
# Trong file .env, sử dụng connection string từ Supabase:
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

#### Với PostgreSQL Local:
```bash
# Tạo database local
createdb beauty_app

# Trong file .env:
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/beauty_app
```

### Bước 4: Cấu hình môi trường
```bash
# Sao chép file mẫu
cp .env.example .env

# Chỉnh sửa file .env bằng notepad/editor
notepad .env    # Windows
nano .env       # Linux/macOS
```

**Cập nhật thông tin trong .env:**

#### Với Supabase Database:
```bash
# Supabase Database - thay [YOUR-PASSWORD] và [PROJECT-REF] bằng thông tin từ Supabase
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
PGHOST=db.[PROJECT-REF].supabase.co
PGUSER=postgres
PGPASSWORD=[YOUR-PASSWORD]
PGDATABASE=postgres

# Flask secrets - tạo mật khẩu mạnh
FLASK_SECRET_KEY=your-super-secret-key-here
SESSION_SECRET=another-secret-key

# Face++ API (xem hướng dẫn dưới)
FACEPP_API_KEY=your_api_key
FACEPP_API_SECRET=your_api_secret

# Stripe (tùy chọn)
STRIPE_SECRET_KEY=sk_test_your_key
```

#### Với PostgreSQL Local:
```bash
# Local Database - thay YOUR_PASSWORD bằng password PostgreSQL của bạn
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/beauty_app
PGHOST=localhost
PGUSER=postgres
PGPASSWORD=YOUR_PASSWORD
PGDATABASE=beauty_app

# Các phần khác giống như trên...
```

### Bước 5: Khởi tạo Database
```bash
# Tạo bảng database
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Thêm dữ liệu mẫu (sản phẩm, user demo)
python seed_data.py
```

### Bước 6: Chạy ứng dụng
```bash
python run_local.py
```

Truy cập: http://localhost:5000

## 🔑 Lấy API Keys

### Face++ API (Bắt buộc cho phân tích da)

1. **Đăng ký tại**: https://www.faceplusplus.com
2. **Tạo tài khoản miễn phí** và xác nhận email
3. **Tạo App mới**:
   - Vào Console
   - "Create a new App"
   - Tên: "Beauty Analytics"
   - Loại: Non-Commercial
4. **Copy API Keys** từ dashboard
5. **Paste vào file .env**:
   ```
   FACEPP_API_KEY=your_key_here
   FACEPP_API_SECRET=your_secret_here
   ```

### Stripe Payment (Tùy chọn)

1. **Đăng ký tại**: https://stripe.com
2. **Lấy Test API Key** từ Dashboard → Developers → API keys
3. **Copy Secret Key** (bắt đầu với sk_test_)
4. **Thêm vào .env**:
   ```
   STRIPE_SECRET_KEY=sk_test_your_key
   ```

## 🎯 Test Ứng dụng

### Tài khoản Demo (sau khi chạy seed_data.py)
- **Admin**: admin@beautyapp.com / admin123
- **User**: mai@example.com / password123

### Kiểm tra các tính năng:
1. **Đăng nhập** với tài khoản demo
2. **Phân tích da** - upload ảnh hoặc chụp camera
3. **Xem sản phẩm** và thêm vào giỏ hàng
4. **Chat tư vấn** làm đẹp
5. **Đọc blog** và bình luận

## 🔧 Xử lý lỗi thường gặp

### Database không kết nối được
```bash
# Kiểm tra PostgreSQL chạy chưa
# Windows:
net start postgresql-x64-13

# Linux/macOS:
sudo service postgresql status
sudo service postgresql start
```

### Face++ API không hoạt động
- Kiểm tra API keys trong file .env
- Đảm bảo có kết nối internet
- Kiểm tra quota miễn phí (1000 requests/tháng)

### Camera không hoạt động
- Cho phép quyền camera trên trình duyệt
- Đảm bảo camera không bị ứng dụng khác sử dụng
- Sử dụng HTTPS khi deploy production

### Upload ảnh lỗi
```bash
# Tạo thư mục uploads
mkdir static/uploads
chmod 755 static/uploads  # Linux/macOS
```

## 📱 Deploy lên Internet

### Heroku (Miễn phí)
```bash
# Cài Heroku CLI
heroku login
heroku create your-app-name

# Set environment variables
heroku config:set FACEPP_API_KEY=your_key
heroku config:set FACEPP_API_SECRET=your_secret

# Deploy
git push heroku main
```

### Railway (Miễn phí)
1. Kết nối GitHub repo với Railway
2. Thêm PostgreSQL addon
3. Set environment variables
4. Deploy tự động

## 📞 Hỗ trợ

### Files quan trọng cần kiểm tra:
- `.env` - Cấu hình database và API keys
- `dependencies.txt` - Danh sách packages cần cài
- `seed_data.py` - Tạo dữ liệu mẫu
- `run_local.py` - Chạy server development

### Logs và Debug:
```bash
# Xem logs chi tiết
python run_local.py

# Test database connection
python -c "from app import db; print('DB OK' if db else 'DB Error')"

# Test Face++ API
python -c "from face_analysis import FaceAnalyzer; print('API OK' if FaceAnalyzer().api_key else 'API Missing')"
```

Nếu vẫn gặp vấn đề, hãy kiểm tra terminal/command prompt để xem thông báo lỗi chi tiết.
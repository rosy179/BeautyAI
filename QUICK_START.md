# Beauty Analytics - Hướng dẫn khởi động nhanh

## 🚀 Cách nhanh nhất để chạy project

### Bước 1: Download tất cả files
Tải về tất cả files theo cấu trúc thư mục trong `PROJECT_STRUCTURE.md`

### Bước 2: Chọn database (Khuyên dùng Supabase)

#### Option A: Supabase (Dễ nhất - Khuyên dùng)
1. Đăng ký tài khoản miễn phí tại https://supabase.com
2. Tạo project mới
3. Lấy DATABASE_URL từ Settings > Database
4. Xem chi tiết trong `SUPABASE_SETUP.md`

#### Option B: PostgreSQL Local
1. Cài PostgreSQL theo hướng dẫn trong `POSTGRESQL_SETUP.md`
2. Tạo database và user
3. Cấu hình DATABASE_URL

### Bước 3: Cài đặt Python dependencies

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Cài đặt packages
pip install -r dependencies.txt
```

### Bước 4: Cấu hình môi trường

```bash
# Copy file mẫu
cp .env.example .env

# Chỉnh sửa .env với thông tin của bạn
```

**Nội dung file .env tối thiểu:**
```env
# Database (Chọn Supabase hoặc Local PostgreSQL)
DATABASE_URL=postgresql://your_database_url

# Face++ API (Bắt buộc cho phân tích da)
FACEPP_API_KEY=your_facepp_api_key
FACEPP_API_SECRET=your_facepp_api_secret

# Flask Secret Key
FLASK_SECRET_KEY=your_random_secret_key_123456789
```

### Bước 5: Khởi tạo database

```bash
# Tạo database tables
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Tạo dữ liệu mẫu
python seed_data.py
```

### Bước 6: Chạy server

```bash
python run_local.py
```

**Truy cập:** http://localhost:5000

## 🔑 Lấy API Keys

### Face++ API (Bắt buộc)
1. Đăng ký tại: https://www.faceplusplus.com
2. Vào Console > API Key & Secret
3. Copy API Key và API Secret vào file .env

### Stripe (Tùy chọn - cho thanh toán)
1. Đăng ký tại: https://stripe.com
2. Vào Developers > API Keys
3. Copy Secret Key vào file .env

## 📱 Tính năng chính

- **Trang chủ:** http://localhost:5000
- **Phân tích da:** http://localhost:5000/skin-analysis
- **Sản phẩm:** http://localhost:5000/products
- **Chat tư vấn:** http://localhost:5000/chat
- **Blog làm đẹp:** http://localhost:5000/blog

## ❓ Gặp lỗi?

### Lỗi database connection
- Kiểm tra DATABASE_URL trong .env
- Đảm bảo database service đang chạy

### Lỗi Face++ API
- Kiểm tra FACEPP_API_KEY và FACEPP_API_SECRET
- Đảm bảo có kết nối internet

### Lỗi dependencies
```bash
pip install --upgrade pip
pip install -r dependencies.txt
```

### Xem logs chi tiết
```bash
python run_local.py
# Xem terminal để debug
```

Xem thêm chi tiết trong `POSTGRESQL_SETUP.md` và `SUPABASE_SETUP.md`.
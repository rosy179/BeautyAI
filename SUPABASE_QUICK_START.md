# Hướng dẫn Nhanh - Kết nối Supabase cho Beauty Analytics

## 🎯 Các bước chính xác để chạy web app với Supabase

### Bước 1: Chuẩn bị Supabase Database

1. **Tạo tài khoản Supabase**:
   - Truy cập: https://supabase.com
   - Đăng ký/đăng nhập

2. **Tạo project mới**:
   - Click "New Project"
   - Name: `Beauty Analytics`
   - Database Password: Tạo mật khẩu mạnh (VD: `MyPass123!@#`)
   - Region: `Southeast Asia (Singapore)`
   - Click "Create new project"

3. **Lấy connection string**:
   - Đợi project khởi tạo xong (2-3 phút)
   - Vào Settings → Database
   - Copy "Connection string" URI
   - Sẽ có dạng: `postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres`

### Bước 2: Cấu hình Project

1. **Tạo file .env từ template**:
```bash
cp .env.example .env
```

2. **Chỉnh sửa file .env**:
```bash
# Thay [PASSWORD] và [REF] bằng thông tin thực của bạn
DATABASE_URL=postgresql://postgres:MyPass123!@#@db.abcdefg.supabase.co:5432/postgres

# Flask secret key (bất kỳ chuỗi mạnh nào)
FLASK_SECRET_KEY=my-super-secret-key-2024

# Face++ API keys (đăng ký tại faceplusplus.com)
FACEPP_API_KEY=your_api_key_here
FACEPP_API_SECRET=your_api_secret_here

# Optional - Stripe for payments
STRIPE_SECRET_KEY=sk_test_...
```

### Bước 3: Cài đặt Dependencies

```bash
# Kích hoạt virtual environment (nếu chưa có)
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Cài đặt packages
pip install -r dependencies.txt
```

### Bước 4: Khởi tạo Database

```bash
# Tạo tables trong Supabase
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Thêm dữ liệu mẫu
python seed_data.py
```

### Bước 5: Test Kết nối

```bash
# Chạy script test
python test_supabase.py
```

Kết quả mong đợi:
```
✅ Supabase connection successful!

📋 Tables in database:
  - user
  - category  
  - product
  - order
  - order_item
  - review
  - blog_post
  - skin_analysis
  - chat_message

👥 Users in database: 2
🛍️ Products in database: 8
```

### Bước 6: Chạy Web App

```bash
python run_local.py
```

Kết quả mong đợi:
```
Environment variables loaded from .env file
Starting Beauty Analytics development server...
Application will be available at: http://localhost:5000
Make sure your .env file is configured with API keys
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

## 🔧 Xử lý lỗi thường gặp

### Lỗi 1: "Connection refused"
```bash
# Kiểm tra connection string
python -c "import os; print('DB URL:', os.environ.get('DATABASE_URL', 'NOT SET'))"
```
**Giải pháp**: Kiểm tra lại PASSWORD và PROJECT-REF trong DATABASE_URL

### Lỗi 2: "Authentication failed"
**Giải pháp**: 
- Password sai → Reset password trong Supabase Settings
- Thêm ký tự đặc biệt cần encode URL

### Lỗi 3: "SSL required"
**Giải pháp**: Thêm `?sslmode=require` vào cuối DATABASE_URL:
```bash
DATABASE_URL=postgresql://postgres:pass@db.ref.supabase.co:5432/postgres?sslmode=require
```

### Lỗi 4: "Module not found"
```bash
# Cài lại dependencies
pip install --upgrade -r dependencies.txt
```

## 📱 Test Features Sau Khi Chạy

1. **Truy cập**: http://localhost:5000
2. **Test đăng ký**: Tạo tài khoản mới
3. **Test đăng nhập**: Login với:
   - Email: `admin@beautyapp.com`
   - Password: `admin123`
4. **Test phân tích da**: Upload ảnh khuôn mặt
5. **Test sản phẩm**: Xem danh sách, thêm vào giỏ hàng
6. **Test chat**: Hỏi tư vấn làm đẹp

## 🎯 URLs quan trọng

- Homepage: http://localhost:5000
- Phân tích da: http://localhost:5000/skin-analysis  
- Sản phẩm: http://localhost:5000/products
- Chat tư vấn: http://localhost:5000/chat
- Blog: http://localhost:5000/blog
- Đăng nhập: http://localhost:5000/auth/login

## 📊 Quản lý Database qua Supabase

1. **Xem dữ liệu**: Supabase Dashboard → Table Editor
2. **Chạy SQL**: Supabase Dashboard → SQL Editor
3. **Backup**: Settings → Database → Download backup

Với hướng dẫn này, bạn sẽ có web app hoạt động hoàn chỉnh với Supabase database!
# Hướng dẫn Cài đặt với Supabase Database

## 🚀 Cài đặt Supabase Database

### Bước 1: Tạo project Supabase

1. **Truy cập**: https://supabase.com
2. **Đăng ký/Đăng nhập** tài khoản
3. **Tạo project mới**:
   - Click "New Project"
   - Chọn Organization (hoặc tạo mới)
   - Điền thông tin:
     - **Name**: Beauty Analytics
     - **Database Password**: Tạo mật khẩu mạnh (lưu lại)
     - **Region**: Singapore/Southeast Asia (gần Việt Nam nhất)
   - Click "Create new project"

### Bước 2: Lấy thông tin kết nối Database

1. **Vào project dashboard**
2. **Click Settings** (biểu tượng bánh răng) ở sidebar
3. **Click Database** trong phần Settings
4. **Tìm phần "Connection string"**
5. **Copy "URI" connection string**

Chuỗi kết nối sẽ có dạng:
```
postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### Bước 3: Cấu hình file .env

Mở file `.env` và cập nhật thông tin Supabase:

```bash
# Supabase Database Configuration
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
PGHOST=db.[PROJECT-REF].supabase.co
PGPORT=5432
PGUSER=postgres
PGPASSWORD=[YOUR-PASSWORD]
PGDATABASE=postgres

# Thay thế [YOUR-PASSWORD] và [PROJECT-REF] bằng thông tin thực của bạn
```

**Ví dụ thực tế:**
```bash
# Ví dụ với project có ref "abcdefghijk" và password "mypassword123"
DATABASE_URL=postgresql://postgres:mypassword123@db.abcdefghijk.supabase.co:5432/postgres
PGHOST=db.abcdefghijk.supabase.co
PGPORT=5432
PGUSER=postgres
PGPASSWORD=mypassword123
PGDATABASE=postgres
```

### Bước 4: Cài đặt và chạy ứng dụng

```bash
# Cài đặt dependencies
pip install -r dependencies.txt

# Khởi tạo database tables
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# Thêm dữ liệu mẫu
python seed_data.py

# Chạy ứng dụng
python run_local.py
```

## 🔧 Ưu điểm của Supabase

### So với PostgreSQL local:
- ✅ **Không cần cài PostgreSQL** trên máy tính
- ✅ **Database cloud** - truy cập từ mọi nơi
- ✅ **Backup tự động** - không lo mất dữ liệu
- ✅ **Miễn phí** - 500MB storage, 2GB bandwidth/tháng
- ✅ **Dashboard quản lý** - xem dữ liệu trực quan
- ✅ **Dễ deploy** - khi đưa lên production

### Dashboard Supabase:
- **Table Editor**: Xem và chỉnh sửa dữ liệu trực tiếp
- **SQL Editor**: Chạy câu lệnh SQL
- **Authentication**: Quản lý user (nếu cần)
- **Storage**: Lưu trữ file (nếu cần)

## 🔍 Kiểm tra kết nối

### Test kết nối database:
```bash
python -c "
from app import app, db
with app.app_context():
    try:
        db.engine.execute('SELECT 1')
        print('✅ Supabase connection successful!')
    except Exception as e:
        print(f'❌ Connection failed: {e}')
"
```

### Xem tables đã tạo:
```bash
python -c "
from app import app, db
with app.app_context():
    print('Tables in database:')
    for table in db.metadata.tables:
        print(f'  - {table}')
"
```

## 🛠️ Quản lý dữ liệu qua Supabase Dashboard

### Xem dữ liệu:
1. Vào project Supabase
2. Click **Table Editor** ở sidebar
3. Chọn table muốn xem (users, products, etc.)
4. Xem và chỉnh sửa dữ liệu trực tiếp

### Chạy SQL queries:
1. Click **SQL Editor** ở sidebar
2. Viết câu lệnh SQL:
```sql
-- Xem tất cả users
SELECT * FROM "user";

-- Xem tất cả products
SELECT * FROM product;

-- Đếm số lượng sản phẩm
SELECT COUNT(*) FROM product;
```

### Backup dữ liệu:
1. Vào Settings → Database
2. Scroll xuống **Database backups**
3. Click **Download backup**

## 🚀 Deploy với Supabase

### Heroku + Supabase:
```bash
# Set Supabase URL làm DATABASE_URL
heroku config:set DATABASE_URL="postgresql://postgres:password@db.project.supabase.co:5432/postgres"

# Set các API keys khác
heroku config:set FACEPP_API_KEY=your_key
heroku config:set FACEPP_API_SECRET=your_secret
```

### Railway + Supabase:
1. Connect GitHub repo
2. Set environment variables:
   - `DATABASE_URL`: Supabase connection string
   - `FACEPP_API_KEY`: Face++ API key
   - `FACEPP_API_SECRET`: Face++ API secret
3. Deploy

## 🔧 Troubleshooting

### Lỗi kết nối thường gặp:

**1. "Connection refused":**
- Kiểm tra connection string có đúng không
- Kiểm tra password có đúng không
- Kiểm tra project reference trong URL

**2. "Authentication failed":**
- Password sai hoặc bị thay đổi
- Vào Supabase Settings → Database → Reset password

**3. "SSL required":**
- Thêm `?sslmode=require` vào cuối DATABASE_URL:
```bash
DATABASE_URL=postgresql://postgres:password@db.project.supabase.co:5432/postgres?sslmode=require
```

**4. "Too many connections":**
- Supabase miễn phí giới hạn 60 connections
- Restart application để giải phóng connections

### Debug connection:
```bash
# Test với psql (nếu có cài)
psql "postgresql://postgres:password@db.project.supabase.co:5432/postgres"

# Test với Python
python -c "
import psycopg2
try:
    conn = psycopg2.connect('postgresql://postgres:password@db.project.supabase.co:5432/postgres')
    print('✅ Direct connection OK')
    conn.close()
except Exception as e:
    print(f'❌ Connection error: {e}')
"
```

## 💡 Tips sử dụng Supabase

### Tối ưu performance:
- Tạo indexes cho các cột thường query
- Sử dụng connection pooling
- Đóng connections sau khi dùng

### Bảo mật:
- Không share connection string publicly
- Sử dụng Row Level Security (RLS) nếu cần
- Regularly backup dữ liệu quan trọng

### Monitoring:
- Theo dõi usage trong Supabase dashboard
- Check logs khi có lỗi
- Monitor connection count

Với Supabase, bạn không cần cài đặt PostgreSQL local và có thể truy cập database từ mọi nơi!
# Hướng dẫn cài đặt PostgreSQL cho Beauty Analytics

## 🗄️ Tại sao cần PostgreSQL?

Beauty Analytics project hỗ trợ 2 loại database:
1. **Supabase** (Cloud - Khuyên dùng) - Không cần cài đặt gì
2. **PostgreSQL Local** - Cần cài đặt trên máy tính

## 🎯 Khuyến nghị: Dùng Supabase (Dễ nhất)

**Supabase là PostgreSQL cloud miễn phí, không cần cài đặt:**
- ✅ Miễn phí 500MB database 
- ✅ Không cần cài đặt phần mềm
- ✅ Tự động backup
- ✅ Kết nối internet là đủ

👉 **Xem hướng dẫn trong file `SUPABASE_SETUP.md`**

---

## 🔧 Nếu muốn dùng PostgreSQL Local

### Windows

#### Cách 1: PostgreSQL Official Installer (Khuyên dùng)

1. **Download PostgreSQL:**
   - Truy cập: https://www.postgresql.org/download/windows/
   - Chọn phiên bản mới nhất (PostgreSQL 15 hoặc 16)
   - Download file `.exe` installer

2. **Cài đặt:**
   ```
   - Chạy file installer
   - Chọn Install Location: C:\Program Files\PostgreSQL\15
   - Chọn Data Directory: C:\Program Files\PostgreSQL\15\data
   - Nhập password cho user 'postgres' (ghi nhớ password này!)
   - Port: 5432 (mặc định)
   - Locale: Default locale
   - Bỏ qua Stack Builder khi cài xong
   ```

3. **Tạo Database cho project:**
   ```cmd
   # Mở Command Prompt as Administrator
   cd "C:\Program Files\PostgreSQL\15\bin"
   
   # Đăng nhập PostgreSQL
   psql -U postgres
   # Nhập password đã đặt ở bước 2
   
   # Tạo database và user
   CREATE DATABASE beauty_analytics;
   CREATE USER beauty_user WITH PASSWORD 'beauty_password_123';
   GRANT ALL PRIVILEGES ON DATABASE beauty_analytics TO beauty_user;
   \q
   ```

4. **Tạo DATABASE_URL cho .env:**
   ```
   DATABASE_URL=postgresql://beauty_user:beauty_password_123@localhost:5432/beauty_analytics
   ```

#### Cách 2: Sử dụng Docker (Cho developers)

```cmd
# Cài Docker Desktop trước
# Chạy PostgreSQL container
docker run --name beauty-postgres -e POSTGRES_PASSWORD=beauty_password_123 -e POSTGRES_DB=beauty_analytics -p 5432:5432 -d postgres:15

# DATABASE_URL cho .env:
DATABASE_URL=postgresql://postgres:beauty_password_123@localhost:5432/beauty_analytics
```

### macOS

#### Cách 1: Homebrew (Khuyên dùng)

```bash
# Cài Homebrew nếu chưa có
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Cài PostgreSQL
brew install postgresql@15
brew services start postgresql@15

# Tạo database
createdb beauty_analytics

# Tạo user (optional - có thể dùng user mặc định)
psql beauty_analytics
CREATE USER beauty_user WITH PASSWORD 'beauty_password_123';
GRANT ALL PRIVILEGES ON DATABASE beauty_analytics TO beauty_user;
\q
```

**DATABASE_URL cho .env:**
```
# Dùng user mặc định
DATABASE_URL=postgresql://$(whoami)@localhost:5432/beauty_analytics

# Hoặc dùng user tự tạo
DATABASE_URL=postgresql://beauty_user:beauty_password_123@localhost:5432/beauty_analytics
```

#### Cách 2: Postgres.app

1. Download Postgres.app từ: https://postgresapp.com/
2. Kéo vào Applications folder và chạy
3. Click "Initialize" để tạo server
4. Database URL sẽ là: `postgresql://localhost:5432/postgres`

### Ubuntu/Linux

```bash
# Update packages
sudo apt update

# Cài PostgreSQL
sudo apt install postgresql postgresql-contrib

# Khởi động service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Tạo database và user
sudo -u postgres psql
CREATE DATABASE beauty_analytics;
CREATE USER beauty_user WITH PASSWORD 'beauty_password_123';
GRANT ALL PRIVILEGES ON DATABASE beauty_analytics TO beauty_user;
\q
```

**DATABASE_URL cho .env:**
```
DATABASE_URL=postgresql://beauty_user:beauty_password_123@localhost:5432/beauty_analytics
```

## ⚙️ Cấu hình sau khi cài đặt

### 1. Kiểm tra kết nối

```bash
# Test kết nối database
python -c "
import psycopg2
from urllib.parse import urlparse

DATABASE_URL = 'postgresql://beauty_user:beauty_password_123@localhost:5432/beauty_analytics'
url = urlparse(DATABASE_URL)
conn = psycopg2.connect(
    host=url.hostname,
    port=url.port,
    user=url.username,
    password=url.password,
    database=url.path[1:]
)
print('✅ Database connection successful!')
conn.close()
"
```

### 2. Cập nhật file .env

```env
# Database Configuration (Chọn 1 trong 2)

# Option 1: Supabase (Cloud - Khuyên dùng)
# DATABASE_URL=postgresql://postgres:[password]@db.[project-id].supabase.co:5432/postgres

# Option 2: PostgreSQL Local
DATABASE_URL=postgresql://beauty_user:beauty_password_123@localhost:5432/beauty_analytics

# API Keys (Bắt buộc)
FACEPP_API_KEY=your_facepp_api_key
FACEPP_API_SECRET=your_facepp_api_secret
FLASK_SECRET_KEY=your_random_secret_key_here_12345

# Optional APIs
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
OPENAI_API_KEY=sk-your_openai_api_key
```

### 3. Khởi tạo database cho project

```bash
cd beauty-analytics

# Kích hoạt virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Cài dependencies
pip install -r dependencies.txt

# Tạo tables
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✅ Tables created!')"

# Tạo dữ liệu mẫu
python seed_data.py
```

### 4. Chạy project

```bash
python run_local.py
```

Truy cập: http://localhost:5000

## 🔍 Troubleshooting

### Lỗi thường gặp:

#### 1. "psycopg2-binary not found"
```bash
pip install psycopg2-binary
```

#### 2. "connection to server failed"
- Kiểm tra PostgreSQL service đã chạy chưa
- Kiểm tra port 5432 có bị chiếm không
- Kiểm tra username/password trong DATABASE_URL

#### 3. "database does not exist"
```sql
# Đăng nhập PostgreSQL và tạo database
psql -U postgres
CREATE DATABASE beauty_analytics;
```

#### 4. "permission denied"
```sql
# Cấp quyền cho user
GRANT ALL PRIVILEGES ON DATABASE beauty_analytics TO beauty_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO beauty_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO beauty_user;
```

## 🎯 So sánh: Supabase vs PostgreSQL Local

| Tiêu chí | Supabase | PostgreSQL Local |
|----------|----------|------------------|
| **Cài đặt** | Không cần | Cần cài phần mềm |
| **Chi phí** | Miễn phí 500MB | Miễn phí hoàn toàn |
| **Hiệu năng** | Phụ thuộc internet | Nhanh hơn |
| **Backup** | Tự động | Phải tự làm |
| **Bảo mật** | SSL/TLS sẵn có | Phải tự cấu hình |
| **Khuyến nghị** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 💡 Khuyến nghị cuối cùng

**Cho người mới bắt đầu:** Dùng Supabase (xem SUPABASE_SETUP.md)
**Cho developers:** PostgreSQL Local hoặc Docker
**Cho production:** Supabase hoặc managed PostgreSQL services

Supabase sẽ giúp bạn tiết kiệm thời gian và tránh được nhiều vấn đề về cấu hình database!
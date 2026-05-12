# BeautyAI - Ứng dụng Phân tích Da và Mỹ phẩm

Ứng dụng web toàn diện cho phân tích da, tư vấn sản phẩm mỹ phẩm và thương mại điện tử được xây dựng bằng Flask.

## ✨ Tính năng chính

- **🔍 Phân tích da AI**: Sử dụng Face++ API để phân tích loại da, tuổi và các vấn đề về da
- **📸 Chụp ảnh trực tiếp**: Tích hợp camera để chụp ảnh khuôn mặt ngay trên trình duyệt
- **💄 Cửa hàng mỹ phẩm**: Hệ thống thương mại điện tử đầy đủ với giỏ hàng và thanh toán
- **💬 Chatbot tư vấn**: AI tư vấn làm đẹp và chăm sóc da
- **📝 Blog làm đẹp**: Hệ thống blog với bình luận và tương tác
- **⭐ Đánh giá sản phẩm**: Người dùng có thể đánh giá và nhận xét sản phẩm
- **💳 Thanh toán Stripe**: Tích hợp thanh toán trực tuyến an toàn

## 🚀 Hướng dẫn cài đặt

### 1. Yêu cầu hệ thống

- Python 3.8+
- MySQL
- Git

### 2. Tải về và cài đặt

```bash
# Clone repository
git clone <my-repository-url>
cd beautyAI

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

### 3. Cấu hình cơ sở dữ liệu

## MySQL:

CREATE DATABASE beauty_app;
\q

### 4. Cấu hình biến môi trường

Sao chép file `.env.example` thành `.env` và cập nhật thông tin:

```bash
cp .env.example .env
```

Chỉnh sửa file `.env` với thông tin của bạn (xem chi tiết bên dưới).

### 5. Khởi tạo database

```bash
# Test kết nối database
python test_mysql.py

# Thêm dữ liệu mẫu (tùy chọn)
python seed_data.py
```

### 6. Chạy ứng dụng

## Development mode

python main.py

Ứng dụng sẽ chạy tại: http://localhost:5000

## 🔧 Cấu hình API Keys

### Face++ API (Phân tích da)

1. Truy cập: https://www.faceplusplus.com
2. Đăng ký tài khoản miễn phí
3. Tạo ứng dụng và lấy API Key & API Secret
4. Thêm vào file `.env`:

```

FACEPP_API_KEY=your_api_key_here
FACEPP_API_SECRET=your_api_secret_here

```

### Stripe Payment (Thanh toán)

1. Truy cập: https://stripe.com
2. Đăng ký tài khoản
3. Lấy Secret Key từ Dashboard
4. Thêm vào file `.env`:

```

STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key

```

### OpenAI API (Chatbot - Tùy chọn)

1. Truy cập: https://platform.openai.com
2. Tạo API Key
3. Thêm vào file `.env`:

```

OPENAI_API_KEY=your_openai_api_key
```

## 📁 Cấu trúc thư mục

```

beautyAI/
├── app.py # Khởi tạo Flask app
├── extensions.py # Khởi tạo SQLAlchemy
├── main.py # Entry point
├── models.py # Database models
├── routes.py # API endpoints
├── forms.py # Form definitions
├── face_analysis.py # Face++ integration
├── test_mysql.py # Test database connection
├── static/ # CSS, JS, images
│ ├── css/
│ ├── js/
│ └── uploads/
├── templates/ # HTML templates
├── instance/ # Database files
└── dependencies.txt # Python dependencies

```

## 🛠️ Troubleshooting

### Lỗi Face++ API

- Kiểm tra API credentials trong file `.env`
- Đảm bảo có kết nối internet
- Kiểm tra quota API (tài khoản miễn phí có giới hạn)

### Lỗi Camera không hoạt động

- Cho phép quyền truy cập camera trên trình duyệt
- Sử dụng HTTPS trong production
- Kiểm tra camera có được sử dụng bởi ứng dụng khác không

## 📦 Dependencies chính

- **Flask**: Web framework
- **SQLAlchemy**: ORM database
- **Flask-Login**: Quản lý đăng nhập
- **Requests**: HTTP client cho API calls

## 🤝 Đóng góp
1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📽️ Web Demo
https://beauty-webapp.onrender.com/
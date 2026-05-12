<div align="center">
  <img src="https://img.icons8.com/?size=100&id=aW2I8WvA6eHk&format=png&color=000000" alt="BeautyAI Logo" width="100"/>
  <h1>🌸 BeautyAI</h1>
  <p><strong>Ứng dụng Phân tích Da và Mỹ phẩm Thông minh tích hợp Trí tuệ Nhân tạo</strong></p>
  
  <a href="https://beauty-webapp.onrender.com/"><strong>🌎 Xem Web Demo Trực Tuyến</strong></a>

  <br><br>

  [![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
  [![Flask](https://img.shields.io/badge/flask-v2.0+-lightgrey.svg)](https://flask.palletsprojects.com/)
  [![Face++](https://img.shields.io/badge/AI-Face++-orange.svg)](https://www.faceplusplus.com/)
  [![Stripe](https://img.shields.io/badge/Payment-Stripe-indigo.svg)](https://stripe.com/)
</div>

<hr/>

BeautyAI là một nền tảng web toàn diện mang lại trải nghiệm cá nhân hóa cho người dùng trong việc chăm sóc sắc đẹp. Ứng dụng kết hợp sức mạnh của trí tuệ nhân tạo (AI) để phân tích da, tư vấn liệu trình chăm sóc, đồng thời tích hợp một hệ thống thương mại điện tử chuyên nghiệp để mua sắm mỹ phẩm.

## ✨ Tính năng nổi bật

- 🔍 **Phân tích da bằng AI**: Sử dụng công nghệ nhận diện khuôn mặt tiên tiến từ Face++ để chẩn đoán tình trạng da (mụn, đốm nâu, nếp nhăn,...), dự đoán độ tuổi và loại da.
- 📸 **Camera trực tuyến**: Hỗ trợ chụp ảnh khuôn mặt và phân tích ngay trên trình duyệt mà không cần tải file.
- 💄 **Cửa hàng Mỹ phẩm**: Hệ thống E-commerce hoàn chỉnh với giỏ hàng, quản lý đơn hàng và gợi ý sản phẩm theo tình trạng da.
- 💬 **Trợ lý Ảo (Chatbot)**: Tích hợp AI tư vấn lộ trình chăm sóc da chuẩn y khoa và giải đáp các thắc mắc về làm đẹp.
- 📝 **Cộng đồng & Blog**: Nơi người dùng có thể chia sẻ kinh nghiệm, đọc các bài viết về skincare và tương tác qua hệ thống bình luận.
- ⭐ **Đánh giá & Review**: Tính năng rating và feedback giúp người dùng đưa ra quyết định mua hàng thông minh hơn.
- 💳 **Thanh toán An toàn**: Tích hợp cổng thanh toán quốc tế Stripe, hỗ trợ thanh toán thẻ nhanh chóng và bảo mật.

---

## 🚀 Hướng dẫn cài đặt (Local Development)

### 1. Yêu cầu hệ thống

- **Python** 3.8 trở lên
- **MySQL** (Hoặc MariaDB)
- **Git**

### 2. Clone mã nguồn & Cài đặt môi trường

```bash
# Clone repository về máy
git clone <my-repository-url>
cd beautyAI

# Tạo môi trường ảo (Virtual Environment)
python -m venv venv

# Kích hoạt môi trường ảo
# Trên Windows:
venv\Scripts\activate
# Trên macOS/Linux:
source venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install -r dependencies.txt
```

### 3. Cấu hình Database (MySQL)

Truy cập MySQL console và tạo database:
```sql
CREATE DATABASE beauty_app;
```

### 4. Thiết lập Biến môi trường

Nhân bản file `.env.example` thành `.env`:
```bash
cp .env.example .env
```
Mở file `.env` và điền các API keys tương ứng (xem phần Cấu hình API Keys bên dưới).

### 5. Khởi tạo dữ liệu

```bash
# Kiểm tra kết nối tới Database và khởi tạo các bảng (tables)
python test_mysql.py

# Thêm dữ liệu mẫu (Sản phẩm, User test...) vào hệ thống
python seed_data.py
```

### 6. Khởi chạy Ứng dụng

```bash
python main.py
```
🎉 Ứng dụng sẽ chạy tại địa chỉ: **http://localhost:5000**

---

## 🔑 Cấu hình API Keys

Để các tính năng AI và thanh toán hoạt động, bạn cần đăng ký và thiết lập các khóa API sau trong file `.env`:

<details>
<summary><strong>1. Face++ API (Dùng cho Phân tích da)</strong></summary>

1. Truy cập [Face++ (Megvii)](https://www.faceplusplus.com) và đăng ký tài khoản.
2. Tạo ứng dụng mới để lấy **API Key** và **API Secret**.
3. Cập nhật vào `.env`:
   ```env
   FACEPP_API_KEY=your_api_key_here
   FACEPP_API_SECRET=your_api_secret_here
   ```
</details>

<details>
<summary><strong>2. Stripe API (Dùng cho Thanh toán)</strong></summary>

1. Truy cập [Stripe Dashboard](https://stripe.com) và đăng ký tài khoản.
2. Chuyển sang chế độ Test mode và lấy **Secret Key**.
3. Cập nhật vào `.env`:
   ```env
   STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
   ```
</details>

<details>
<summary><strong>3. OpenAI API (Dùng cho Chatbot - Tùy chọn)</strong></summary>

1. Truy cập [OpenAI Platform](https://platform.openai.com).
2. Tạo một khóa API (API Key) mới.
3. Cập nhật vào `.env`:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```
</details>

---

## 📁 Cấu trúc Dự án

```text
beautyAI/
├── ⚙️ app.py                # Khởi tạo và cấu hình ứng dụng Flask
├── 🔗 routes.py             # Quản lý Routing và Controller
├── 🗄️ models.py             # Định nghĩa Database Schema (SQLAlchemy)
├── 📝 forms.py              # Các form dữ liệu (WTForms)
├── 🧠 face_analysis.py      # Logic tích hợp API Face++ xử lý hình ảnh
├── 🚀 main.py               # File entry point chạy ứng dụng
├── 📂 static/               # Tệp tĩnh (CSS, JS, Images, Uploads)
│   ├── css/
│   ├── js/
│   └── uploads/
├── 🖼️ templates/            # Giao diện HTML (Jinja2)
└── 📦 dependencies.txt      # Danh sách thư viện Python
```

---

## 🛠️ Xử lý Sự cố thường gặp (Troubleshooting)

| Lỗi / Sự cố | Cách khắc phục |
| :--- | :--- |
| **Không thể phân tích da** | - Kiểm tra `FACEPP_API_KEY` trong file `.env`<br>- Đảm bảo máy có kết nối Internet<br>- Kiểm tra quota (giới hạn) API của tài khoản Face++ miễn phí |
| **Camera không bật được** | - Cấp quyền truy cập Camera cho trình duyệt<br>- Trình duyệt yêu cầu **HTTPS** để dùng Camera (trừ khi chạy `localhost`)<br>- Đảm bảo không có ứng dụng nào khác (Zoom, Meet...) đang chiếm dụng Camera |

---

## 🤝 Đóng góp (Contributing)

Chúng tôi luôn hoan nghênh mọi đóng góp để phát triển dự án này!
1. **Fork** repository này
2. Tạo một **branch** mới cho tính năng của bạn (`git checkout -b feature/AmazingFeature`)
3. **Commit** thay đổi (`git commit -m 'Thêm một tính năng tuyệt vời'`)
4. **Push** lên branch đó (`git push origin feature/AmazingFeature`)
5. Mở một **Pull Request**

---
<div align="center">
  <i>Được xây dựng với ❤️ bằng Python & Flask</i>
</div>
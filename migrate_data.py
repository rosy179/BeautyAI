import os
from sqlalchemy import create_engine, MetaData, Table, select, insert, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# --- CẤU HÌNH ---
# 1. Link MySQL Local (lấy từ .env)
LOCAL_DB_URL = os.environ.get("DATABASE_URL") 

# 2. Link PostgreSQL Render (HÃY DÁN LINK EXTERNAL CỦA BẠN VÀO ĐÂY)
# Link của bạn sẽ có dạng: postgres://user:pass@hostname.render.com/db
REMOTE_DB_URL = "postgresql://rosy:tuqzOgAyZDdw2GWjXqCWlHa6qJeBSi9l@dpg-d7u8k2l7vvec73bikdk0-a.singapore-postgres.render.com/database_4yxb"

# Fix prefix if needed
if REMOTE_DB_URL.startswith("postgres://"):
    REMOTE_DB_URL = REMOTE_DB_URL.replace("postgres://", "postgresql://", 1)

def migrate():
    # Clear PG environment variables that might interfere with the connection
    # (Especially PGPORT=3306 in the .env file)
    for env_var in ['PGHOST', 'PGPORT', 'PGUSER', 'PGPASSWORD', 'PGDATABASE']:
        if env_var in os.environ:
            del os.environ[env_var]

    if "DÁN_LINK" in REMOTE_DB_URL:
        print("❌ LỖI: Bạn chưa dán link External Database URL vào script!")
        return

    print("🚀 Bắt đầu quá trình di chuyển dữ liệu...")
    
    try:
        # Tạo kết nối
        local_engine = create_engine(LOCAL_DB_URL)
        remote_engine = create_engine(REMOTE_DB_URL)
        
        local_meta = MetaData()
        local_meta.reflect(bind=local_engine)
        
        # Danh sách các bảng cần di chuyển
        tables_to_migrate = ['category', 'user', 'product', 'blog_post', 'skin_analysis']
        
        # 1. XÓA DỮ LIỆU CŨ TRƯỚC (Theo thứ tự ngược lại để tránh lỗi khóa ngoại)
        print("🧹 Đang dọn dẹp dữ liệu cũ trên remote...")
        with remote_engine.connect() as conn:
            for table_name in reversed(tables_to_migrate):
                if table_name in local_meta.tables:
                    conn.execute(local_meta.tables[table_name].delete())
            conn.commit()
        print("✅ Đã dọn dẹp xong.")

        # 2. DI CHUYỂN DỮ LIỆU MỚI
        for table_name in tables_to_migrate:
            if table_name not in local_meta.tables:
                print(f"⚠️ Bỏ qua bảng '{table_name}' vì không tìm thấy ở local.")
                continue
                
            print(f"📦 Đang chuyển bảng: {table_name}...")
            
            # Đọc dữ liệu từ local
            table = local_meta.tables[table_name]
            with local_engine.connect() as conn:
                data = conn.execute(select(table)).fetchall()
                
            if not data:
                print(f"ℹ️ Bảng '{table_name}' trống, bỏ qua.")
                continue
                
            # Chuyển đổi dữ liệu sang list of dicts và xử lý kiểu Boolean
            rows = []
            for row in data:
                row_dict = dict(row._mapping)
                # Tự động chuyển 0/1 sang False/True cho các cột Boolean
                for key, value in row_dict.items():
                    if key in ['is_admin', 'is_published', 'is_active']:
                        if value is not None:
                            row_dict[key] = bool(value)
                rows.append(row_dict)
            
            # Đẩy dữ liệu lên remote
            with remote_engine.connect() as conn:
                # Chèn dữ liệu mới
                conn.execute(insert(table), rows)
                
                # 3. Cập nhật Sequence (chỉ dành cho PostgreSQL)
                try:
                    conn.execute(text(f"SELECT setval(pg_get_serial_sequence('\"{table_name}\"', 'id'), (SELECT MAX(id) FROM \"{table_name}\"))"))
                except Exception:
                    pass
                    
                conn.commit()
                
            print(f"✅ Đã chuyển xong {len(rows)} dòng của bảng '{table_name}'.")

        print("\n✨ CHÚC MỪNG! Dữ liệu đã được chuyển lên Render thành công.")
        print("Giờ bạn có thể truy cập website trên Render để kiểm tra.")

    except Exception as e:
        print(f"❌ CÓ LỖI XẢY RA: {e}")

if __name__ == "__main__":
    migrate()

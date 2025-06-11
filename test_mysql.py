import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL not set")

try:
    engine = create_engine(database_url)
    with engine.connect() as connection:
        print("Kết nối MySQL thành công!")
except Exception as e:
    print(f"Lỗi kết nối MySQL: {e}")
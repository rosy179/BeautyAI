import os
import logging
import cloudinary
import cloudinary.uploader
from flask import Flask
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv
from extensions import db

# Only load .env if not running on Render
if not os.environ.get("RENDER"):
    load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)

def test_db_connection(uri, timeout=3):
    """Test whether a database URI can be reached within a short timeout."""
    from sqlalchemy import create_engine
    try:
        connect_args = {}
        if "postgres" in uri or "mysql" in uri:
            connect_args["connect_timeout"] = timeout
        test_engine = create_engine(uri, connect_args=connect_args)
        with test_engine.connect() as conn:
            pass
        test_engine.dispose()
        return True
    except Exception as e:
        safe_info = uri.split('@')[-1] if '@' in uri else uri.split(':')[0]
        logging.warning(f"Could not connect to database ({safe_info}): {e}")
        return False

def resolve_database_uri(app):
    is_render = bool(os.environ.get("RENDER"))
    database_url = os.environ.get("DATABASE_URL", "").strip()

    def get_sqlite_uri():
        os.makedirs(app.instance_path, exist_ok=True)
        sqlite_file = os.path.join(app.instance_path, "beautyai.db").replace("\\", "/")
        return f"sqlite:///{sqlite_file}"

    # If running on Render:
    if is_render:
        is_localhost = bool(database_url and ("localhost" in database_url.lower() or "127.0.0.1" in database_url))
        
        # If DATABASE_URL is empty or points to localhost, search for alternative remote DB env vars
        if not database_url or is_localhost:
            logging.warning("DATABASE_URL on Render is empty or points to localhost. Searching for remote DB alternatives...")
            found_alt = None
            for key, val in os.environ.items():
                if key != "DATABASE_URL" and any(proto in val.lower() for proto in ["postgresql://", "postgres://", "mysql://", "mysql+pymysql://"]):
                    if "localhost" not in val.lower() and "127.0.0.1" not in val:
                        found_alt = val
                        logging.info(f"Found alternative database URL in {key}")
                        break
            if found_alt:
                database_url = found_alt
            else:
                logging.warning("No accessible remote database configured on Render. Falling back to SQLite.")
                return get_sqlite_uri()

    # If no URL is provided anywhere, use SQLite
    if not database_url:
        logging.info("No DATABASE_URL configured. Falling back to SQLite.")
        return get_sqlite_uri()

    # Force PostgreSQL driver and fix prefix for Render/SQLAlchemy compatibility
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg2://", 1)

    # On Render, if remote DB is unreachable (e.g., expired or incorrect credentials), fallback to SQLite to prevent crashing
    if is_render:
        safe_info = database_url.split('@')[-1] if '@' in database_url else database_url.split(':')[0]
        logging.info(f"Testing remote database connection: {safe_info}")
        if not test_db_connection(database_url, timeout=3):
            logging.warning("Remote database connection failed (may be expired or network-restricted). Falling back to SQLite.")
            return get_sqlite_uri()

    return database_url

def create_app():
    logging.basicConfig(level=logging.INFO)
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs('static/uploads', exist_ok=True)

    database_url = resolve_database_uri(app)
    logging.info(f"Connecting to database type: {database_url.split(':')[0]}")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    with app.app_context():
        from models import User, Product, Category, BlogPost, SkinAnalysis, Order, Review, ChatMessage, OrderItem, BlogComment
        db.create_all()

        # Automatically seed sample data if database is empty
        try:
            if Category.query.first() is None:
                from seed_data import create_sample_data
                logging.info("Database is empty. Populating with initial sample data...")
                create_sample_data(app)
        except Exception as seed_err:
            logging.warning(f"Auto-seed note: {seed_err}")

        from routes import main_bp, auth_bp, products_bp, chat_bp, blog_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(products_bp, url_prefix='/products')
        app.register_blueprint(chat_bp, url_prefix='/chat')
        app.register_blueprint(blog_bp, url_prefix='/blog')
    
    return app



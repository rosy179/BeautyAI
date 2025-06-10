# Files to Delete for Clean Setup

## ❌ Delete These Files (Safe to Remove)

### Documentation Files (9 files)
```
README.md
SETUP.md
DOWNLOAD_GUIDE.md
SUPABASE_SETUP.md
SUPABASE_QUICK_START.md
PROJECT_STRUCTURE.md
DOWNLOAD_CHECKLIST.md
COMPLETE_FILE_LIST.md
FINAL_DOWNLOAD_PACKAGE.md
ESSENTIAL_FILES.md
CLEANUP_INSTRUCTIONS.md (this file)
```

### Test/Setup Scripts (6 files)
```
test_supabase.py
init_database.py
setup_database.py
quick_setup.py
create_tables.py
run_local.py (replaced by start.py)
```

### Temporary/Cache Files
```
__pycache__/ (folder)
instance/ (folder - only if using Supabase)
attached_assets/ (folder)
```

## ✅ Keep These Files (24 files only)

### Core Python (6 files)
```
app.py
models.py
routes.py
forms.py
face_analysis.py
main.py
seed_data.py
start.py (new single startup script)
```

### Configuration (2 files)
```
.env (your environment config)
dependencies.txt
```

### Frontend (4 files)
```
static/css/beauty.css
static/js/main.js
static/js/chat.js
static/js/skin-analysis.js
```

### Templates (12 files)
```
templates/base.html
templates/index.html
templates/skin_analysis.html
templates/products.html
templates/product_detail.html
templates/cart.html
templates/checkout.html
templates/chat.html
templates/blog.html
templates/blog_post.html
templates/profile.html
templates/auth/login.html
templates/auth/register.html
```

## 🚀 After Cleanup - Simple Commands

```bash
# Setup (once)
cp .env.example .env
# Edit .env with your database info
pip install -r dependencies.txt
mkdir -p static/uploads

# Run (always)
python start.py
```

The new `start.py` does everything automatically:
- Loads environment
- Creates database tables
- Adds sample data if needed
- Starts the server

Much cleaner and no more conflicts!
import os
from datetime import timedelta

class Config:
    # ── Security ───────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

    # ── Database ───────────────────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Aniket%402004@localhost:3306/faculty_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }

    # ── File Uploads ───────────────────────────────────────────────────
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

    # ── Session ────────────────────────────────────────────────────────
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax
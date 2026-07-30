import os
from datetime import timedelta

class Config:
    # ── Security ───────────────────────────────────────────────────────
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')


import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-2025'
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True

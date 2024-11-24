import os


class Config:
    """
    Базовая конфигурация приложения.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mykey'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

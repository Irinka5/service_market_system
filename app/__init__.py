from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Создание экземпляров расширений
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()


# Функция для создания экземпляра приложения
def create_app():
    app = Flask(__name__)

    # Конфигурация приложения
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация расширений с приложением
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Настройка менеджера логинов
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Регистрация Blueprints (модулей)
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app

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
    app.config.from_object('app.config.Config')

    # Инициализация расширений с приложением
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Настройка менеджера логинов
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Регистрация Blueprints
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
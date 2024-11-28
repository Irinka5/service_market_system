from . import db
from flask_login import UserMixin
from datetime import datetime


# Модель пользователя
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('Application', backref='user', lazy=True)


# Модель услуги
class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    sub_services = db.relationship('SubService', backref='category', lazy=True)


# Модель подкатегории услуги
class SubService(db.Model):
    __tablename__ = 'sub_services'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)  # Связь с таблицей services
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)


# Модель заявки
class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    sub_service = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    street = db.Column(db.String(150), nullable=False)
    house_number = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(20), nullable=True)
    contact_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.Time, nullable=True)
    budget = db.Column(db.Float, nullable=False)
    additional_requirements = db.Column(db.Text, nullable=True)
    payment_method = db.Column(db.String(50), nullable=False)
    comments = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='Создана', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# Модель завершенных заказов
class CompletedOrder(db.Model):
    __tablename__ = 'completed_orders'

    id = db.Column(db.Integer, primary_key=True)
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Исполнитель
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Пользователь, создавший заявку
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)  # Заявка
    executor_comment = db.Column(db.Text, nullable=True)  # Комментарий от исполнителя
    completion_date = db.Column(db.DateTime, default=datetime.utcnow)  # Дата завершения
    work_duration = db.Column(db.Interval, nullable=True)  # Время выполнения (можно передавать timedelta)
    rating = db.Column(db.Integer, default=0)  # Оценка, 0 означает отсутствие оценки
    success = db.Column(db.Boolean, default=True)  # Успешность выполнения

    # Связи с пользователями и заявками
    executor = db.relationship('User', foreign_keys=[executor_id], backref='completed_orders_as_executor')
    requester = db.relationship('User', foreign_keys=[requester_id], backref='completed_orders_as_requester')
    application = db.relationship('Application', backref='completed_order', uselist=False)

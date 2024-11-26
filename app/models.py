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

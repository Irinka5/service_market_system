from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, StringField, DateField, TimeField, FloatField, BooleanField
from wtforms.validators import DataRequired, Optional, Length, EqualTo, ValidationError, Email
from .models import User


# Форма регистрации пользователя
class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=4, max=25, message='Имя пользователя должно содержать от 4 до 25 символов')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=6, message='Пароль должен содержать не менее 6 символов')
    ])
    confirm = PasswordField('Подтвердите пароль', validators=[
        DataRequired(),
        EqualTo('password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Зарегистрироваться')

    # Валидация имени пользователя (проверка на уникальность)
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято. Пожалуйста, выберите другое.')


# Форма входа пользователя
class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=4, max=25)
    ])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


# Форма создания заявки
class ApplicationForm(FlaskForm):
    service_type = SelectField('Категория услуги', coerce=int, validators=[DataRequired()])
    sub_service = SelectField('Подкатегория или конкретная услуга', coerce=int, validators=[DataRequired()])
    description = TextAreaField('Подробное описание задачи', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    street = StringField('Улица', validators=[DataRequired()])
    house_number = StringField('Номер дома/квартиры', validators=[DataRequired()])
    postal_code = StringField('Почтовый индекс', validators=[])
    contact_name = StringField('Имя', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    preferred_date = DateField('Предпочтительная дата', format='%Y-%m-%d', validators=[DataRequired()])
    preferred_time = TimeField('Предпочтительное время', validators=[])
    budget = FloatField('Бюджет', validators=[DataRequired()])
    additional_requirements = TextAreaField('Дополнительные пожелания или требования')
    payment_method = SelectField('Способ оплаты', choices=[('cash', 'Наличные'), ('card', 'Банковская карта'), ('online', 'Онлайн-платеж')], validators=[DataRequired()])
    comments = TextAreaField('Комментарии')
    submit = SubmitField('Создать заявку')

class ApplicationFilterForm(FlaskForm):
    service_type = SelectField('Категория услуги', choices=[], coerce=int)
    sub_service = SelectField('Подкатегория услуги', choices=[], coerce=int)
    user_only = BooleanField('Только мои заявки', default=True)
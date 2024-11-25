from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
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
    service_id = SelectField('Выберите услугу', coerce=int, validators=[DataRequired()])
    description = StringField('Описание заявки', validators=[DataRequired()])
    submit = SubmitField('Создать заявку')

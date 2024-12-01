from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, StringField, DateField, \
    TimeField, FloatField, BooleanField
from wtforms.validators import DataRequired, Optional, Length, EqualTo, ValidationError, Email, Regexp, NumberRange
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
    service_type = SelectField('Тип услуги', validators=[DataRequired()], coerce=int)
    sub_service = SelectField('Подуслуга', validators=[DataRequired()], coerce=int)
    description = TextAreaField('Описание', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    street = StringField('Улица', validators=[Optional()])
    house_number = StringField('Номер дома', validators=[Optional()])
    postal_code = StringField('Почтовый индекс', validators=[Optional()])
    contact_name = StringField('Имя', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[
        DataRequired(),
        Regexp(r'^\+?\d{10,15}$', message="Некорректный номер телефона.")
    ])
    email = StringField('Электронная почта', validators=[DataRequired(), Email()])
    preferred_date = DateField('Предпочтительная дата', validators=[Optional()])
    preferred_time = TimeField('Предпочтительное время', validators=[Optional()])
    budget = FloatField('Бюджет', validators=[
        DataRequired(),
        NumberRange(min=0, message="Бюджет должен быть положительным числом.")
    ])
    additional_requirements = TextAreaField('Дополнительные требования', validators=[Optional()])
    payment_method = SelectField('Способ оплаты', validators=[DataRequired()],
                                 choices=[('cash', 'Наличные'), ('card', 'Банковская карта'), ('online', 'Онлайн-платеж')])
    comments = TextAreaField('Комментарии', validators=[Optional()])


class ApplicationFilterForm(FlaskForm):
    service_type = SelectField('Категория услуги', choices=[], coerce=int)
    sub_service = SelectField('Подкатегория услуги', choices=[], coerce=int)
    user_only = BooleanField('Только мои заявки', default=True)


# Форма для подтверждения взятия заявки в исполнение
class TakeOrderForm(FlaskForm):
    confirm = BooleanField('Подтвердить взятие заявки в исполнение', validators=[DataRequired()])
    submit = SubmitField('Взять в исполнение')


# Форма для завершения заявки исполнителем
class CompleteOrderForm(FlaskForm):
    comment = TextAreaField('Комментарий исполнителя', validators=[DataRequired(), Length(min=10, max=500)])
    successful = SelectField('Успешность выполнения', choices=[('успешно', 'Успешно'), ('неуспешно', 'Неуспешно')],
                             validators=[DataRequired()])
    rating = SelectField('Оценка (от 1 до 5)', choices=[(str(i), str(i)) for i in range(1, 6)],
                         validators=[DataRequired()])
    submit = SubmitField('Завершить заказ')

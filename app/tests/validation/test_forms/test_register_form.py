import unittest
from flask import Flask
from app.forms import RegistrationForm
from app import db
from app.models import User
from wtforms import validators

class RegisterFormTestCase(unittest.TestCase):

    def setUp(self):
        """Инициализация тестового клиента и валидных данных для формы"""
        self.app = Flask(__name__)
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SECRET_KEY'] = 'testsecret'
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
        self.valid_data = {
            'username': 'validuser',
            'password': 'validpassword',
            'confirm': 'validpassword'
        }

    def tearDown(self):
        """Удаление данных тестовой базы данных"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_valid_register_form(self):
        """Тест на валидность формы с корректными данными"""
        with self.app.test_request_context():
            form = RegistrationForm(data=self.valid_data)
            self.assertTrue(form.validate(), "Форма должна быть валидной при корректных данных")

    def test_missing_username(self):
        """Тест на отсутствие имени пользователя"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            del invalid_data['username']
            form = RegistrationForm(data=invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при отсутствии имени пользователя")
            self.assertIn('This field is required.', form.username.errors)

    def test_missing_password(self):
        """Тест на отсутствие пароля"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            del invalid_data['password']
            form = RegistrationForm(data=invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при отсутствии пароля")
            self.assertIn('This field is required.', form.password.errors)

    def test_missing_confirm_password(self):
        """Тест на отсутствие подтверждения пароля"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            del invalid_data['confirm']
            form = RegistrationForm(data=invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при отсутствии подтверждения пароля")
            self.assertIn('This field is required.', form.confirm.errors)

    def test_passwords_do_not_match(self):
        """Тест на несовпадение паролей"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            invalid_data['confirm'] = 'differentpassword'
            form = RegistrationForm(data=invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной, если пароли не совпадают")
            self.assertIn('Пароли должны совпадать', form.confirm.errors)

    def test_username_too_short(self):
        """Тест на слишком короткое имя пользователя"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            invalid_data['username'] = 'usr'
            form = RegistrationForm(data=invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при слишком коротком имени пользователя")

    def test_password_too_short(self):
        """Тест на слишком короткий пароль"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            invalid_data['password'] = 'pass'
            invalid_data['confirm'] = 'pass'
            form = RegistrationForm(data=invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при слишком коротком пароле")

    def test_username_already_taken(self):
        """Тест на уже существующее имя пользователя"""
        with self.app.app_context():
            # Добавляем пользователя с таким же именем
            user = User(username=self.valid_data['username'], password='somepassword', role='client')
            db.session.add(user)
            db.session.commit()

            with self.app.test_request_context():
                form = RegistrationForm(data=self.valid_data)
                self.assertFalse(form.validate(), "Форма должна быть невалидной, если имя пользователя уже занято")
                self.assertIn('Это имя пользователя уже занято. Пожалуйста, выберите другое.', form.username.errors)

if __name__ == '__main__':
    unittest.main()

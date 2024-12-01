import unittest
from flask import Flask
from app.forms import LoginForm
from wtforms import validators


class LoginFormTestCase(unittest.TestCase):

    def setUp(self):
        """Инициализация тестового клиента и валидных данных для формы"""
        self.app = Flask(__name__)
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.valid_data = {
            'username': 'validuser',
            'password': 'validpassword'
        }

    def test_valid_login_form(self):
        """Тест на валидность формы с корректными данными"""
        with self.app.test_request_context():
            form = LoginForm(data=self.valid_data)
            self.assertTrue(form.validate(), "Форма должна быть валидной при корректных данных")

    def test_missing_username(self):
        """Тест на отсутствие имени пользователя"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            del invalid_data['username']
            form = LoginForm(data=invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при отсутствии имени пользователя")
            self.assertIn('This field is required.', form.username.errors)

    def test_missing_password(self):
        """Тест на отсутствие пароля"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            del invalid_data['password']
            form = LoginForm(data=invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при отсутствии пароля")
            self.assertIn('This field is required.', form.password.errors)

    def test_empty_username(self):
        """Тест на пустое поле имени пользователя"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            invalid_data['username'] = ''
            form = LoginForm(data=invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при пустом имени пользователя")
            self.assertIn('This field is required.', form.username.errors)

    def test_empty_password(self):
        """Тест на пустое поле пароля"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            invalid_data['password'] = ''
            form = LoginForm(data=invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при пустом пароле")
            self.assertIn('This field is required.', form.password.errors)

    def test_invalid_username_format(self):
        """Тест на некорректный формат имени пользователя (например, слишком короткое имя)"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            invalid_data['username'] = 'inv'
            form = LoginForm(data=invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при слишком коротком имени пользователя")


if __name__ == '__main__':
    unittest.main()

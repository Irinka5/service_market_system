import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

class AuthRoutesTestCase(unittest.TestCase):
    def setUp(self):
        """Инициализация тестового клиента и тестовой базы данных"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Используем in-memory базу данных для тестов
        self.app.config['WTF_CSRF_ENABLED'] = False  # Отключаем CSRF защиту для тестов
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Создаем тестового пользователя
        self.username = 'testuser'
        self.password = 'password123'
        hashed_password = generate_password_hash(self.password, method='pbkdf2:sha256', salt_length=8)
        self.user = User(username=self.username, password=hashed_password, role='client')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Удаление данных тестовой базы данных"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        """Тест успешной регистрации нового пользователя"""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'password': 'newpassword',
            'confirm': 'newpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(User.query.filter_by(username='newuser').first())

    def test_login_success(self):
        """Тест успешного входа в систему"""
        response = self.client.post('/login', data={
            'username': self.username,
            'password': self.password
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Ожидаем успешный вход с кодом 200
        self.assertIn('Вы успешно вошли в систему.', response.data.decode('utf-8'))

    def test_login_failure_wrong_password(self):
        """Тест неудачного входа с неправильным паролем"""
        response = self.client.post('/login', data={
            'username': self.username,
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Ожидаем, что страница перезагрузится с кодом 200
        self.assertIn('Неверное имя пользователя или пароль.', response.data.decode('utf-8'))

    def test_login_failure_nonexistent_user(self):
        """Тест неудачного входа с отсутствующим пользователем"""
        response = self.client.post('/login', data={
            'username': 'nonexistent',
            'password': 'password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Ожидаем, что страница перезагрузится с кодом 200
        self.assertIn('Неверное имя пользователя или пароль.', response.data.decode('utf-8'))

    def test_logout(self):
        """Тест выхода из системы"""
        # Сначала логинимся
        self.client.post('/login', data={
            'username': self.username,
            'password': self.password
        })
        # Затем тестируем выход
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Ожидаем страницу после выхода
        self.assertIn('Вы успешно вышли из системы.', response.data.decode('utf-8'))

    if __name__ == '__main__':
        unittest.main()

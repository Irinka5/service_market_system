import unittest
from flask import url_for
from app import create_app, db
from app.models import User

class UserAuthFunctionalTestCase(unittest.TestCase):
    def setUp(self):
        """Инициализация тестового клиента и тестовой базы данных"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Используем in-memory базу данных для тестов
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Создание тестового пользователя
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User(username=self.username, password=self.password, role='client')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Удаление данных тестовой базы данных"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_login_logout(self):
        """Тест регистрации, входа и выхода пользователя"""
        # Регистрация
        response = self.client.post('/register', data={
            'username': 'newuser',
            'password': 'newpassword',
            'confirm': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Регистрация прошла успешно!', response.data.decode())

        # Вход
        response = self.client.post('/login', data={
            'username': 'newuser',
            'password': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Вы успешно вошли в систему.', response.data.decode())

        # Выход
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Вы успешно вышли из системы.', response.data.decode())

if __name__ == '__main__':
    unittest.main()

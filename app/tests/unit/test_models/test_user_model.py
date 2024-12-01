import unittest
from app import db, create_app
from app.models import User
from app.utils import hash_password


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        """Настройка тестового окружения."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Добавляем тестового пользователя
        self.user = User(username='testuser', password='password123', role='client')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        """Очистка тестового окружения."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_user(self):
        """Тест создания пользователя."""
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'client')

    def test_password_storage(self):
        """Тест хранения пароля пользователя."""
        user = User.query.filter_by(username='testuser').first()
        self.assertNotEqual(user.password, hash_password('password123'))

    def test_unique_username(self):
        """Тест уникальности имени пользователя."""
        with self.assertRaises(Exception):
            duplicate_user = User(username='testuser', password='password456', role='executor')
            db.session.add(duplicate_user)
            db.session.commit()

    def test_role_assignment(self):
        """Тест назначения роли пользователю."""
        user = User.query.filter_by(username='testuser').first()
        self.assertEqual(user.role, 'client')

    def test_user_relationships(self):
        """Тест связи пользователя с заявками и завершенными заказами."""
        self.assertEqual(len(self.user.applications), 0)
        self.assertEqual(len(self.user.completed_orders_as_executor), 0)
        self.assertEqual(len(self.user.completed_orders_as_requester), 0)


if __name__ == '__main__':
    unittest.main()

import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Service, SubService
from werkzeug.security import generate_password_hash


class ApplicationWorkflowFunctionalTestCase(unittest.TestCase):
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

        # Создание тестового пользователя
        self.username = 'testuser'
        self.password = 'password123'
        hashed_password = generate_password_hash(self.password, method='pbkdf2:sha256', salt_length=8)
        self.user = User(username=self.username, password=hashed_password, role='client')
        db.session.add(self.user)

        # Создание тестовых данных для сервисов и подкатегорий
        self.service = Service(name='Ремонт', description='Ремонтные работы')
        db.session.add(self.service)
        db.session.commit()

        # Проверим, что сервис был создан и сохранён
        self.service = Service.query.filter_by(name='Ремонт').first()
        if not self.service:
            raise ValueError("Ошибка при создании Service")

        self.sub_service = SubService(service_id=self.service.id, name='Сантехника', description='Сантехнические работы')
        db.session.add(self.sub_service)
        db.session.commit()

        # Проверим, что подкатегория была создана и сохранена
        self.sub_service = SubService.query.filter_by(name='Сантехника').first()
        if not self.sub_service:
            raise ValueError("Ошибка при создании SubService")

    def tearDown(self):
        """Удаление данных тестовой базы данных"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_edit_delete_application(self):
        """Тест создания, редактирования и удаления заявки"""
        # Логинимся
        response = self.client.post('/login', data={'username': self.username, 'password': self.password}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Вы успешно вошли в систему.', response.data.decode())

        # Создание заявки
        response = self.client.post('/application/new', data={
            'service_type': self.service.id,
            'sub_service': self.sub_service.id,
            'description': 'Ремонт сантехники',
            'city': 'Москва',
            'street': 'Ленина',
            'house_number': '10',
            'postal_code': '',
            'contact_name': 'Иван Иванов',
            'phone': '89991112233',
            'email': 'test@example.com',
            'preferred_date': '',
            'preferred_time': '',
            'budget': 5000.0,
            'additional_requirements': '',
            'payment_method': 'cash',
            'comments': ''
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Ваша заявка успешно создана!', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()

import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Service, SubService, Application
from werkzeug.security import generate_password_hash


class MainRoutesTestCase(unittest.TestCase):
    def setUp(self):
        """Инициализация тестового клиента и тестовой базы данных"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Создаем тестового пользователя и администратора
        self.user_username = 'testuser'
        self.user_password = 'password123'
        self.user = User(username=self.user_username, password=generate_password_hash(self.user_password),
                         role='client')
        db.session.add(self.user)

        self.admin_username = 'adminuser'
        self.admin_password = 'adminpassword'
        self.admin_user = User(username=self.admin_username,
                               password=generate_password_hash(self.admin_password), role='admin')
        db.session.add(self.admin_user)

        # Создаем тестовую услугу и подуслугу
        self.service = Service(name="Ремонт", description="Услуги по ремонту")
        db.session.add(self.service)
        db.session.commit()

        self.sub_service = SubService(name="Электрика", service_id=self.service.id,
                                      description="Ремонт электрических систем")
        db.session.add(self.sub_service)
        db.session.commit()

        # Создаем тестовую заявку
        self.application = Application(
            user_id=self.user.id,
            service_type=self.service.id,
            sub_service=self.sub_service.id,
            description="Ремонт электрики в доме",
            city="Москва",
            street="Ленина",
            house_number="10",
            contact_name="Иван Иванов",  # Указываем contact_name для удовлетворения ограничения NOT NULL
            phone="89991112233",
            email="test@example.com",
            budget=10000.0,
            payment_method="Наличные"
        )
        db.session.add(self.application)
        db.session.commit()

    def tearDown(self):
        """Удаление данных тестовой базы данных"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login_user(self):
        """Вход в систему как пользователь"""
        self.client.post('/login', data={
            'username': self.user_username,
            'password': self.user_password
        })

    def login_admin(self):
        """Вход в систему как администратор"""
        self.client.post('/login', data={
            'username': self.admin_username,
            'password': self.admin_password
        })

    def test_index_page(self):
        """Тест главной страницы"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Service Market System', response.data.decode('utf-8'))

    def test_new_application(self):
        """Тест создания новой заявки"""
        self.login_user()
        response = self.client.post('/application/new', data={
            'service_type': self.service.id,
            'sub_service': self.sub_service.id,
            'description': 'Ремонт сантехники',
            'city': 'Москва',
            'street': 'Тверская',
            'house_number': '15',
            'postal_code': '123456',
            'contact_name': 'Петр Петров',
            'phone': '89991112234',
            'email': 'test2@example.com',
            'preferred_date': '2024-12-01',  # Добавили корректную дату
            'preferred_time': '12:00',  # Добавили предпочтительное время (если нужно)
            'budget': 20000.0,
            'payment_method': 'card',  # Изменили значение на одно из допустимых
            'comments': 'Срочный ремонт'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ваша заявка успешно создана!', response.data.decode('utf-8'))
        self.assertIsNotNone(Application.query.filter_by(description='Ремонт сантехники').first())

    def test_get_applications_list(self):
        """Тест получения всех заявок текущего пользователя"""
        self.login_user()
        response = self.client.get('/applications')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Мои заявки', response.data.decode('utf-8'))

    def test_get_application_details(self):
        """Тест получения деталей заявки"""
        self.login_user()
        response = self.client.get(f'/api/application/{self.application.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['description'], 'Ремонт электрики в доме')
        self.assertEqual(data['contact_name'], 'Иван Иванов')


if __name__ == '__main__':
    unittest.main()

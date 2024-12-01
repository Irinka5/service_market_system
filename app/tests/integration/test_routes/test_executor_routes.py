import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Application, Service, SubService
from werkzeug.security import generate_password_hash


class ExecutorRoutesTestCase(unittest.TestCase):
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

        # Создаем тестового исполнителя и пользователя
        self.executor_username = 'executoruser'
        self.executor_password = 'executorpassword'
        self.executor_user = User(username=self.executor_username,
                                  password=generate_password_hash(self.executor_password), role='executor')
        db.session.add(self.executor_user)

        self.user_username = 'testuser'
        self.user_password = 'password123'
        self.user = User(username=self.user_username, password=generate_password_hash(self.user_password),
                         role='client')
        db.session.add(self.user)

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

    def login_executor(self):
        """Вход в систему как исполнитель"""
        self.client.post('/login', data={
            'username': self.executor_username,
            'password': self.executor_password
        })

    def test_get_executor_applications(self):
        """Тест получения доступных заявок исполнителем"""
        self.login_executor()
        response = self.client.get('/executor/applications')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Ремонт электрики в доме', response.data.decode('utf-8'))

    def test_take_order(self):
        """Тест взятия заявки исполнителем"""
        self.login_executor()
        response = self.client.post(f'/take_order/{self.application.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        self.assertEqual(Application.query.get(self.application.id).executor_id, self.executor_user.id)

    def test_get_taken_orders(self):
        """Тест получения списка взятых исполнителем заявок"""
        self.login_executor()
        # Сначала берем заявку в работу
        self.client.post(f'/take_order/{self.application.id}')

        response = self.client.get('/get_taken_orders')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['orders']), 1)
        self.assertEqual(data['orders'][0]['description'], 'Ремонт электрики в доме')

    def test_take_already_taken_order(self):
        """Тест попытки взять уже взятую в работу заявку"""
        # Сначала логинимся исполнителем и берем заявку
        self.login_executor()
        self.client.post(f'/take_order/{self.application.id}')

        # Создаем другого исполнителя
        new_executor = User(username='newexecutor', password=generate_password_hash('password456'), role='executor')
        db.session.add(new_executor)
        db.session.commit()

        # Пытаемся взять ту же заявку вторым исполнителем
        self.client.post('/login', data={
            'username': 'newexecutor',
            'password': 'password456'
        })

        response = self.client.post(f'/take_order/{self.application.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('Заявка уже взята или недоступна.', data['error'])


if __name__ == '__main__':
    unittest.main()

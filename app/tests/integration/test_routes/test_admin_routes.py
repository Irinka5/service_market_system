import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Application, Service, SubService
from werkzeug.security import generate_password_hash


class AdminRoutesTestCase(unittest.TestCase):
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

        # Создаем тестового администратора и обычного пользователя
        self.admin_username = 'adminuser'
        self.admin_password = 'adminpassword'
        self.admin_user = User(username=self.admin_username,
                               password=generate_password_hash(self.admin_password), role='admin')
        db.session.add(self.admin_user)

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

    def login_admin(self):
        """Вход в систему как администратор"""
        self.client.post('/login', data={
            'username': self.admin_username,
            'password': self.admin_password
        })

    def test_get_admin_panel(self):
        """Тест получения панели администратора"""
        self.login_admin()
        response = self.client.get('/admin/panel')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Панель администратора', response.data.decode('utf-8'))

    def test_get_all_applications(self):
        """Тест получения всех заявок администратором"""
        self.login_admin()
        response = self.client.get('/admin/get_applications')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['applications']), 1)
        self.assertEqual(data['applications'][0]['description'], 'Ремонт электрики в доме')

    def test_edit_application(self):
        """Тест редактирования заявки администратором"""
        self.login_admin()
        updated_description = "Обновленное описание заявки"
        updated_status = "В работе"
        response = self.client.post(f'/admin/edit_application/{self.application.id}', json={
            'description': updated_description,
            'status': updated_status
        })

        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Заявка успешно обновлена')

        updated_application = Application.query.get(self.application.id)
        self.assertEqual(updated_application.description, updated_description)
        self.assertEqual(updated_application.status, updated_status)

    def test_delete_application(self):
        """Тест удаления заявки администратором"""
        self.login_admin()
        response = self.client.delete(f'/admin/delete_application/{self.application.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('{"success":true}', response.data.decode('utf-8'))

        # Проверяем, что заявка была удалена
        deleted_application = Application.query.get(self.application.id)
        self.assertIsNone(deleted_application)

    def test_get_completed_orders(self):
        """Тест получения завершенных заказов администратором"""
        self.login_admin()
        response = self.client.get('/admin/get_completed_orders')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # Ожидаем, что завершенные заказы будут пустыми
        self.assertEqual(len(data['orders']), 0)

if __name__ == '__main__':
    unittest.main()

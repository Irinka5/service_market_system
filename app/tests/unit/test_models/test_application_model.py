import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models import Application, User, Service, SubService
from app.utils import hash_password


class ApplicationModelTestCase(unittest.TestCase):

    def setUp(self):
        """Инициализация тестового приложения и базы данных"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Используем in-memory базу данных
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Создание тестовых данных
        self.user = User(username="testuser", password=hash_password("password123"), role="customer")
        self.executor = User(username="executor", password=hash_password("password456"), role="executor")
        db.session.add(self.user)
        db.session.add(self.executor)

        self.service = Service(name="Ремонт", description="Услуги по ремонту")
        db.session.add(self.service)
        db.session.commit()  # Нам нужно коммитнуть, чтобы service.id был доступен

        # Используем service_id для создания SubService
        self.sub_service = SubService(name="Электрика", service_id=self.service.id, description="Описание подуслуги")
        db.session.add(self.sub_service)
        db.session.commit()

    def tearDown(self):
        """Очистка ресурсов после каждого теста"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_application(self):
        """Тест на создание заявки"""
        application = Application(
            user_id=self.user.id,
            service_type=self.service.id,
            sub_service=self.sub_service.id,
            description="Требуется замена проводки",
            city="Москва",
            street="Пушкина",
            house_number="10",
            postal_code="123456",
            contact_name="Иван Петров",
            phone="1234567890",
            email="ivan@example.com",
            preferred_date=datetime.utcnow().date(),
            preferred_time=datetime.utcnow().time(),
            budget=10000.0,
            additional_requirements="Необходимы качественные материалы",
            payment_method="Наличные",
            status="Создана",
            created_at=datetime.utcnow()
        )
        db.session.add(application)
        db.session.commit()

        self.assertIsNotNone(application.id)
        self.assertEqual(application.creator.username, "testuser")
        self.assertEqual(application.service.name, "Ремонт")
        self.assertEqual(application.subservice.name, "Электрика")
        self.assertEqual(application.description, "Требуется замена проводки")
        self.assertEqual(application.city, "Москва")

    def test_update_application(self):
        """Тест на обновление заявки"""
        application = Application(
            user_id=self.user.id,
            service_type=self.service.id,
            sub_service=self.sub_service.id,
            description="Требуется замена проводки",
            city="Москва",
            street="Пушкина",
            house_number="10",
            postal_code="123456",
            contact_name="Иван Петров",
            phone="1234567890",
            email="ivan@example.com",
            budget=10000.0,
            payment_method="Наличные",
            status="Создана",
            created_at=datetime.utcnow()
        )
        db.session.add(application)
        db.session.commit()

        # Обновление заявки
        application.description = "Требуется ремонт щитка"
        application.city = "Санкт-Петербург"
        db.session.commit()

        self.assertEqual(application.description, "Требуется ремонт щитка")
        self.assertEqual(application.city, "Санкт-Петербург")

    def test_delete_application(self):
        """Тест на удаление заявки"""
        application = Application(
            user_id=self.user.id,
            service_type=self.service.id,
            sub_service=self.sub_service.id,
            description="Требуется замена проводки",
            city="Москва",
            street="Пушкина",
            house_number="10",
            postal_code="123456",
            contact_name="Иван Петров",
            phone="1234567890",
            email="ivan@example.com",
            budget=10000.0,
            payment_method="Наличные",
            status="Создана",
            created_at=datetime.utcnow()
        )
        db.session.add(application)
        db.session.commit()

        # Удаление заявки
        db.session.delete(application)
        db.session.commit()

        # Проверяем, что заявка не существует в базе данных
        self.assertIsNone(Application.query.get(application.id))

    def test_application_relationships(self):
        """Тест на проверку отношений модели Application"""
        application = Application(
            user_id=self.user.id,
            executor_id=self.executor.id,
            service_type=self.service.id,
            sub_service=self.sub_service.id,
            description="Тестовые отношения",
            city="Москва",
            street="Ленина",
            house_number="20",
            contact_name="Сергей Иванов",
            phone="9876543210",
            email="sergey@example.com",
            budget=15000.0,
            payment_method="Карта",
            status="В работе",
            created_at=datetime.utcnow()
        )
        db.session.add(application)
        db.session.commit()

        # Проверка связи с пользователем, категорией и подкатегорией
        self.assertEqual(application.creator.username, "testuser")
        self.assertEqual(application.assigned_executor.username, "executor")
        self.assertEqual(application.service.name, "Ремонт")
        self.assertEqual(application.subservice.name, "Электрика")


if __name__ == '__main__':
    unittest.main()

import unittest
from app import db, create_app
from app.models import User, Application, CompletedOrder, Service, SubService
from app.utils import hash_password
from datetime import datetime, timedelta


class CompletedOrderModelTestCase(unittest.TestCase):

    def setUp(self):
        """Инициализация тестового приложения и базы данных"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Используем in-memory базу данных
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Создание тестовых пользователей
        self.requester = User(username="customer1", password=hash_password("customerpassword"), role="customer")
        self.executor = User(username="executor1", password=hash_password("executorpassword"), role="executor")
        db.session.add(self.requester)
        db.session.add(self.executor)
        db.session.commit()

        # Создание тестовой услуги и подуслуги
        self.service = Service(name="Ремонт", description="Ремонтные услуги")
        db.session.add(self.service)
        db.session.commit()

        self.sub_service = SubService(name="Электрика", service_id=self.service.id,
                                      description="Электромонтажные работы")
        db.session.add(self.sub_service)
        db.session.commit()

        # Создание тестовой заявки
        self.application = Application(
            user_id=self.requester.id,
            service_type=self.service.id,
            sub_service=self.sub_service.id,
            description="Требуется ремонт электрической проводки",
            city="Москва",
            street="Ленина",
            house_number="25",
            contact_name="Иван Иванов",
            phone="+7 123 456 7890",
            email="ivanov@example.com",
            budget=15000.0,
            payment_method="Наличный расчет"
        )
        db.session.add(self.application)
        db.session.commit()

    def tearDown(self):
        """Удаление контекста приложения и базы данных"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_completed_order(self):
        """Тестирование создания завершенного заказа"""
        completed_order = CompletedOrder(
            executor_id=self.executor.id,
            requester_id=self.requester.id,
            application_id=self.application.id,
            executor_comment="Работа выполнена качественно.",
            completion_date=datetime.utcnow(),
            work_duration=timedelta(hours=2),
            rating=5,
            success=True
        )
        db.session.add(completed_order)
        db.session.commit()

        order = CompletedOrder.query.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.executor_id, self.executor.id)
        self.assertEqual(order.requester_id, self.requester.id)
        self.assertEqual(order.application_id, self.application.id)
        self.assertEqual(order.executor_comment, "Работа выполнена качественно.")
        self.assertEqual(order.rating, 5)
        self.assertTrue(order.success)

    def test_relationships(self):
        """Тестирование связей завершенного заказа с другими моделями"""
        completed_order = CompletedOrder(
            executor_id=self.executor.id,
            requester_id=self.requester.id,
            application_id=self.application.id,
            executor_comment="Отличная работа!",
            completion_date=datetime.utcnow(),
            work_duration=timedelta(hours=3),
            rating=4,
            success=True
        )
        db.session.add(completed_order)
        db.session.commit()

        order = CompletedOrder.query.first()
        self.assertEqual(order.executor.username, "executor1")
        self.assertEqual(order.requester.username, "customer1")
        self.assertEqual(order.application.description, "Требуется ремонт электрической проводки")

    def test_invalid_data(self):
        """Тестирование ошибок в данных завершенного заказа"""
        # Попробуем создать заказ без связанного исполнителя
        invalid_order = CompletedOrder(
            requester_id=self.requester.id,
            application_id=self.application.id,
            executor_comment="Не хватает исполнителя"
        )
        db.session.add(invalid_order)
        with self.assertRaises(Exception):
            db.session.commit()

    def test_update_completed_order(self):
        """Тестирование обновления завершенного заказа"""
        completed_order = CompletedOrder(
            executor_id=self.executor.id,
            requester_id=self.requester.id,
            application_id=self.application.id,
            executor_comment="Изначальный комментарий",
            completion_date=datetime.utcnow(),
            work_duration=timedelta(hours=1),
            rating=3,
            success=True
        )
        db.session.add(completed_order)
        db.session.commit()

        # Обновление завершенного заказа
        order = CompletedOrder.query.first()
        order.executor_comment = "Обновленный комментарий"
        order.rating = 5
        db.session.commit()

        updated_order = CompletedOrder.query.first()
        self.assertEqual(updated_order.executor_comment, "Обновленный комментарий")
        self.assertEqual(updated_order.rating, 5)


if __name__ == "__main__":
    unittest.main()

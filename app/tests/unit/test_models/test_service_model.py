import unittest
from app import db, create_app
from app.models import Service, SubService
from datetime import datetime


class ServiceModelTestCase(unittest.TestCase):

    def setUp(self):
        """Инициализация тестового приложения и базы данных"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Создание тестовой услуги
        self.service = Service(name="Ремонт", description="Ремонтные услуги")
        db.session.add(self.service)
        db.session.commit()

        # Создание тестовых подкатегорий
        self.sub_service_1 = SubService(name="Сантехника", service_id=self.service.id, description="Ремонт сантехники")
        self.sub_service_2 = SubService(name="Электрика", service_id=self.service.id,
                                        description="Электромонтажные работы")
        db.session.add(self.sub_service_1)
        db.session.add(self.sub_service_2)
        db.session.commit()

    def tearDown(self):
        """Удаление контекста приложения и базы данных"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_service(self):
        """Тестирование создания услуги"""
        service = Service.query.first()
        self.assertIsNotNone(service)
        self.assertEqual(service.name, "Ремонт")
        self.assertEqual(service.description, "Ремонтные услуги")

    def test_service_subservices_relationship(self):
        """Тестирование связей между услугой и подкатегориями"""
        service = Service.query.first()
        self.assertEqual(len(service.sub_services), 2)  # Услуга Ремонт должна иметь две подкатегории

        sub_service_names = [sub_service.name for sub_service in service.sub_services]
        self.assertIn("Сантехника", sub_service_names)
        self.assertIn("Электрика", sub_service_names)

    def test_add_new_subservice(self):
        """Тестирование добавления новой подкатегории к услуге"""
        new_sub_service = SubService(name="Отделочные работы", service_id=self.service.id,
                                     description="Работы по отделке")
        db.session.add(new_sub_service)
        db.session.commit()

        service = Service.query.first()
        self.assertEqual(len(service.sub_services), 3)  # Теперь должно быть три подкатегории
        sub_service_names = [sub_service.name for sub_service in service.sub_services]
        self.assertIn("Отделочные работы", sub_service_names)

    def test_delete_subservice(self):
        """Тестирование удаления подкатегории из услуги"""
        sub_service_to_delete = SubService.query.filter_by(name="Сантехника").first()
        db.session.delete(sub_service_to_delete)
        db.session.commit()

        service = Service.query.first()
        self.assertEqual(len(service.sub_services), 1)  # Ожидаем, что останется только одна подкатегория
        sub_service_names = [sub_service.name for sub_service in service.sub_services]
        self.assertNotIn("Сантехника", sub_service_names)


if __name__ == "__main__":
    unittest.main()

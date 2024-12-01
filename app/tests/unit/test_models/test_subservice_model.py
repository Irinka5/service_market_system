import unittest
from app import db, create_app
from app.models import Service, SubService


class SubServiceModelTestCase(unittest.TestCase):

    def setUp(self):
        """Инициализация тестового приложения и базы данных"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Используем in-memory базу данных
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.service = Service(name="Ремонт", description="Ремонтные услуги")
        db.session.add(self.service)
        db.session.commit()

        self.sub_service = SubService(name="Сантехника", service_id=self.service.id, description="Ремонт сантехники")
        db.session.add(self.sub_service)
        db.session.commit()

    def tearDown(self):
        """Удаление контекста приложения и базы данных"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_subservice(self):
        """Тестирование создания подкатегории"""
        sub_service = SubService.query.first()
        self.assertIsNotNone(sub_service)
        self.assertEqual(sub_service.name, "Сантехника")
        self.assertEqual(sub_service.description, "Ремонт сантехники")

    def test_subservice_relationship_with_service(self):
        """Тестирование связи подкатегории с услугой"""
        sub_service = SubService.query.first()
        self.assertIsNotNone(sub_service.category)
        self.assertEqual(sub_service.category.name, "Ремонт")

    def test_update_subservice(self):
        """Тестирование обновления подкатегории"""
        sub_service = SubService.query.first()
        sub_service.description = "Обновлённое описание"
        db.session.commit()

        updated_sub_service = SubService.query.first()
        self.assertEqual(updated_sub_service.description, "Обновлённое описание")

    def test_delete_subservice(self):
        """Тестирование удаления подкатегории"""
        sub_service_to_delete = SubService.query.first()
        db.session.delete(sub_service_to_delete)
        db.session.commit()

        remaining_sub_services = SubService.query.all()
        self.assertEqual(len(remaining_sub_services), 0)

    def test_service_subservice_relationship(self):
        """Тестирование добавления нескольких подкатегорий к услуге"""
        new_sub_service = SubService(name="Электрика", service_id=self.service.id,
                                     description="Электромонтажные работы")
        db.session.add(new_sub_service)
        db.session.commit()

        service = Service.query.first()
        self.assertEqual(len(service.sub_services), 2)
        sub_service_names = [sub_service.name for sub_service in service.sub_services]
        self.assertIn("Сантехника", sub_service_names)
        self.assertIn("Электрика", sub_service_names)


if __name__ == "__main__":
    unittest.main()

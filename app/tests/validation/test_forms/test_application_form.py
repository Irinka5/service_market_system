import unittest
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, FloatField, TextAreaField, DateField, TimeField, validators
from flask import url_for
from app import create_app
from app.forms import ApplicationForm


class ApplicationFormTestCase(unittest.TestCase):
    def setUp(self):
        """Инициализация тестового клиента и тестовой конфигурации"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Отключаем CSRF защиту для тестов
        self.client = self.app.test_client()

        # Данные для инициализации формы
        self.valid_data = {
            'service_type': 1,
            'sub_service': 1,
            'description': 'Ремонт сантехники',
            'city': 'Москва',
            'street': 'Ленина',
            'house_number': '10',
            'postal_code': '123456',
            'contact_name': 'Иван Иванов',
            'phone': '89991112233',
            'email': 'test@example.com',
            'preferred_date': '2024-12-01',
            'preferred_time': '12:30',
            'budget': 10000.0,
            'additional_requirements': 'Без запаха',
            'payment_method': 'cash',
            'comments': 'Требуется быстрое выполнение',
        }

    def _get_initialized_form(self, data):
        """Функция для инициализации формы с допустимыми choices"""
        form = ApplicationForm(data=data)

        # Устанавливаем доступные варианты для SelectField
        form.service_type.choices = [(1, 'Ремонт'), (2, 'Уборка')]
        form.sub_service.choices = [(1, 'Электрика'), (2, 'Сантехника')]
        form.payment_method.choices = [('cash', 'Наличные'), ('card', 'Банковская карта'), ('online', 'Онлайн-платеж')]

        return form

    def tearDown(self):
        """Очистка конфигурации после каждого теста"""
        pass

    def test_valid_form(self):
        """Тест на валидность формы с корректными данными"""
        with self.app.test_request_context():
            form = self._get_initialized_form(self.valid_data)
            self.assertTrue(form.validate(), "Форма должна быть валидной при корректных данных")

    def test_missing_required_fields(self):
        """Тест на отсутствие обязательных полей"""
        with self.app.test_request_context():
            required_fields = ['service_type', 'sub_service', 'description', 'city', 'contact_name', 'phone', 'email',
                               'budget', 'payment_method']

            for field in required_fields:
                invalid_data = self.valid_data.copy()
                del invalid_data[field]
                form = self._get_initialized_form(invalid_data)
                self.assertFalse(form.validate(),
                                 f"Форма должна быть невалидной при отсутствии обязательного поля '{field}'")
                self.assertIn(field, form.errors, f"Поле '{field}' должно вызвать ошибку")

    def test_invalid_email_format(self):
        """Тест на некорректный формат email"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            invalid_data['email'] = 'invalid-email'
            form = self._get_initialized_form(invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при некорректном email")
            self.assertIn('email', form.errors, "Поле 'email' должно вызвать ошибку при некорректном значении")

    def test_invalid_phone_number(self):
        """Тест на некорректный номер телефона"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            invalid_data['phone'] = 'invalid-phone'
            form = self._get_initialized_form(invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при некорректном номере телефона")
            self.assertIn('phone', form.errors, "Поле 'phone' должно вызвать ошибку при некорректном значении")

    def test_negative_budget(self):
        """Тест на отрицательный бюджет"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            invalid_data['budget'] = -1000.0
            form = self._get_initialized_form(invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при отрицательном бюджете")
            self.assertIn('budget', form.errors, "Поле 'budget' должно вызвать ошибку при отрицательном значении")

    def test_invalid_payment_method(self):
        """Тест на некорректный способ оплаты"""
        with self.app.test_request_context():
            invalid_data = self.valid_data.copy()
            invalid_data['payment_method'] = 'invalid-method'
            form = self._get_initialized_form(invalid_data)
            self.assertFalse(form.validate(), "Форма должна быть невалидной при некорректном значении 'payment_method'")
            self.assertIn('payment_method', form.errors,
                          "Поле 'payment_method' должно вызвать ошибку при некорректном значении")

    def test_empty_optional_fields(self):
        """Тест формы без заполнения необязательных полей"""
        with self.app.test_request_context():
            optional_fields = ['postal_code', 'additional_requirements', 'comments', 'preferred_date', 'preferred_time']
            invalid_data = self.valid_data.copy()

            for field in optional_fields:
                invalid_data[field] = ''

            form = self._get_initialized_form(invalid_data)
            self.assertTrue(form.validate(), "Форма должна быть валидной даже если необязательные поля не заполнены")


if __name__ == '__main__':
    unittest.main()

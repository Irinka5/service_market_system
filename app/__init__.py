from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Создание экземпляров расширений
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

# Функция для создания экземпляра приложения
def create_app():
    app = Flask(__name__)

    # Конфигурация приложения
    app.config.from_object('app.config.Config')

    # Инициализация расширений с приложением
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Настройка менеджера логинов
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Регистрация Blueprints
    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .executor import executor as exec_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(exec_blueprint)


    with app.app_context():
        db.create_all()

        from .models import Service, SubService

        if Service.query.count() == 0:
            initial_services = [
                Service(name="Ремонт", description="Услуги по ремонту оборудования и помещений"),
                Service(name="Уборка", description="Профессиональная уборка жилых и нежилых помещений"),
                Service(name="IT", description="Информационные технологии и поддержка"),
                Service(name="Строительство", description="Строительные и монтажные работы"),
                Service(name="Красота и здоровье", description="Услуги в сфере красоты и здоровья"),
                Service(name="Транспорт", description="Услуги транспортировки и логистики"),
                Service(name="Образование", description="Курсы и тренинги для повышения квалификации"),
                Service(name="Домашние питомцы", description="Уход и забота о домашних животных"),
                Service(name="Переезды и перевозки", description="Организация переездов и перевозок"),
                Service(name="Финансовые услуги", description="Консультации и поддержка в финансовой сфере")
            ]
            db.session.bulk_save_objects(initial_services)
            db.session.commit()

        # Добавление начальных данных для SubService (подкатегорий)
        if SubService.query.count() == 0:
            initial_sub_services = [
                # Подкатегории для категории "Ремонт"
                SubService(name="Сантехника", service_id=1,
                           description="Услуги по ремонту сантехнического оборудования"),
                SubService(name="Электрика", service_id=1, description="Ремонт и монтаж электропроводки"),
                SubService(name="Ремонт бытовой техники", service_id=1,
                           description="Ремонт мелкой и крупной бытовой техники"),
                SubService(name="Ремонт мебели", service_id=1, description="Ремонт мебели любой сложности"),
                SubService(name="Ремонт полов", service_id=1, description="Ремонт паркета, ламината и плитки"),
                SubService(name="Ремонт стен", service_id=1, description="Штукатурка, покраска и оклейка обоев"),
                SubService(name="Ремонт окон", service_id=1, description="Ремонт пластиковых и деревянных окон"),
                SubService(name="Ремонт дверей", service_id=1, description="Ремонт межкомнатных и входных дверей"),
                SubService(name="Отделочные работы", service_id=1, description="Услуги по отделке помещений"),
                SubService(name="Ремонт крыш", service_id=1, description="Ремонт кровли и устранение протечек"),

                # Подкатегории для категории "Уборка"
                SubService(name="Уборка квартир", service_id=2, description="Генеральная и ежедневная уборка квартир"),
                SubService(name="Уборка офисов", service_id=2, description="Уборка офисных помещений"),
                SubService(name="Уборка после ремонта", service_id=2,
                           description="Уборка после строительных и ремонтных работ"),
                SubService(name="Мытье окон", service_id=2, description="Профессиональная мойка окон и витражей"),
                SubService(name="Химчистка мебели", service_id=2, description="Химчистка диванов, кресел и ковров"),
                SubService(name="Уборка на даче", service_id=2, description="Уборка домов и участков на даче"),
                SubService(name="Уборка снега", service_id=2, description="Уборка снега с территории"),
                SubService(name="Мытье фасадов", service_id=2, description="Промышленная мойка фасадов зданий"),
                SubService(name="Уборка лестничных клеток", service_id=2,
                           description="Уборка подъездов и лестничных клеток"),
                SubService(name="Санитарная обработка", service_id=2,
                           description="Дезинфекция и санитарная обработка помещений"),

                # Подкатегории для категории "IT"
                SubService(name="Настройка компьютеров", service_id=3,
                           description="Настройка операционных систем и программного обеспечения"),
                SubService(name="Ремонт ПК и ноутбуков", service_id=3,
                           description="Ремонт и обслуживание персональных компьютеров"),
                SubService(name="Настройка сети", service_id=3, description="Настройка домашней и офисной сети"),
                SubService(name="Разработка сайтов", service_id=3, description="Создание и разработка веб-сайтов"),
                SubService(name="Поддержка пользователей", service_id=3,
                           description="Техническая поддержка пользователей"),
                SubService(name="Интеграция ПО", service_id=3,
                           description="Интеграция программного обеспечения для бизнеса"),
                SubService(name="Резервное копирование данных", service_id=3,
                           description="Настройка систем резервного копирования"),
                SubService(name="Удаление вирусов", service_id=3,
                           description="Антивирусная проверка и удаление вредоносных программ"),
                SubService(name="Настройка серверов", service_id=3,
                           description="Настройка и администрирование серверов"),
                SubService(name="Облачные сервисы", service_id=3,
                           description="Настройка и поддержка облачных сервисов"),

                # Подкатегории для категории "Строительство"
                SubService(name="Фундаментные работы", service_id=4,
                           description="Закладка фундамента для зданий и сооружений"),
                SubService(name="Кладка кирпича", service_id=4, description="Кирпичная кладка для стен и перегородок"),
                SubService(name="Монтаж каркаса", service_id=4,
                           description="Монтаж металлических и деревянных каркасов"),
                SubService(name="Кровельные работы", service_id=4, description="Монтаж и ремонт кровли"),
                SubService(name="Бетонные работы", service_id=4,
                           description="Работы с бетоном и железобетонными конструкциями"),
                SubService(name="Монтаж инженерных систем", service_id=4,
                           description="Монтаж водопровода, канализации и отопления"),
                SubService(name="Укладка плитки", service_id=4, description="Укладка керамической плитки и мозаики"),
                SubService(name="Снос зданий", service_id=4, description="Демонтаж и снос старых зданий и построек"),
                SubService(name="Армирование конструкций", service_id=4,
                           description="Армирование железобетонных конструкций"),
                SubService(name="Монтаж окон и дверей", service_id=4, description="Установка оконных и дверных блоков"),

                # Подкатегории для категории "Красота и здоровье"
                SubService(name="Косметология", service_id=5,
                           description="Услуги по уходу за кожей и косметологические процедуры"),
                SubService(name="Массаж", service_id=5,
                           description="Различные виды массажа для расслабления и оздоровления"),
                SubService(name="Парикмахерские услуги", service_id=5,
                           description="Стрижки, укладки и окрашивание волос"),
                SubService(name="Маникюр и педикюр", service_id=5, description="Уход за ногтями и ногами"),
                SubService(name="Фитнес и тренировки", service_id=5,
                           description="Персональные тренировки и групповые занятия"),
                SubService(name="Диетология", service_id=5, description="Консультации по питанию и составление диет"),
                SubService(name="СПА-процедуры", service_id=5, description="Расслабляющие и оздоровительные процедуры"),
                SubService(name="Йога и медитация", service_id=5,
                           description="Занятия йогой и медитацией для гармонии тела и духа"),
                SubService(name="Пластическая хирургия", service_id=5,
                           description="Хирургические вмешательства для коррекции внешности"),
                SubService(name="Психологическая помощь", service_id=5,
                           description="Консультации психологов и психотерапевтов"),
                # Подкатегории для категории "Транспорт"
                SubService(name="Такси", service_id=6, description="Услуги такси и трансферы"),
                SubService(name="Аренда автомобилей", service_id=6,
                           description="Аренда автомобилей на короткий и длительный срок"),
                SubService(name="Грузоперевозки", service_id=6,
                           description="Перевозка грузов по городу и за его пределы"),
                SubService(name="Эвакуатор", service_id=6,
                           description="Услуги эвакуатора для транспортировки автомобилей"),
                SubService(name="Ремонт автомобилей", service_id=6, description="Ремонт и обслуживание автомобилей"),
                SubService(name="Автомойка", service_id=6, description="Мойка и чистка автомобилей"),
                SubService(name="Шиномонтаж", service_id=6, description="Услуги по замене и ремонту шин"),
                SubService(name="Автострахование", service_id=6, description="Страхование автомобилей и водителей"),
                SubService(name="Аренда велосипедов", service_id=6,
                           description="Аренда велосипедов для прогулок и поездок"),
                SubService(name="Транспортировка животных", service_id=6, description="Перевозка домашних животных"),
                # Подкатегории для категории "Образование"
                SubService(name="Курсы иностранных языков", service_id=7, description="Обучение иностранным языкам"),
                SubService(name="Компьютерные курсы", service_id=7,
                           description="Обучение работе на компьютере и программированию"),
                SubService(name="Бизнес-тренинги", service_id=7, description="Тренинги по развитию бизнес-навыков"),
                SubService(name="Репетиторство", service_id=7, description="Индивидуальные занятия с репетиторами"),
                SubService(name="Курсы повышения квалификации", service_id=7, description="Обучение для профессионалов"),
                SubService(name="Детские кружки", service_id=7, description="Кружки и секции для детей"),
                SubService(name="Онлайн-курсы", service_id=7, description="Обучение через интернет"),
                SubService(name="Курсы по искусству", service_id=7,
                           description="Обучение рисованию, музыке и другим видам искусства"),
                SubService(name="Курсы по кулинарии", service_id=7, description="Обучение приготовлению различных блюд"),
                SubService(name="Курсы по фитнесу", service_id=7,
                           description="Обучение фитнесу и здоровому образу жизни"),
                # Подкатегории для категории "Домашние питомцы"
                SubService(name="Ветеринарные услуги", service_id=8,
                           description="Медицинская помощь и консультации для животных"),
                SubService(name="Груминг", service_id=8, description="Уход за шерстью и когтями животных"),
                SubService(name="Дрессировка", service_id=8, description="Обучение и дрессировка собак"),
                SubService(name="Приют для животных", service_id=8,
                           description="Временное размещение и уход за животными"),
                SubService(name="Прогулки с собаками", service_id=8, description="Услуги выгула собак"),
                SubService(name="Кормление и уход", service_id=8, description="Уход за животными на дому"),
                SubService(name="Транспортировка животных", service_id=8, description="Перевозка животных"),
                SubService(name="Зоомагазин", service_id=8, description="Продажа товаров для животных"),
                SubService(name="Консультации по уходу", service_id=8,
                           description="Советы и рекомендации по уходу за животными"),
                SubService(name="Фотосессии с животными", service_id=8,
                           description="Профессиональные фотосессии с домашними питомцами"),
                # Подкатегории для категории "Переезды и перевозки"
                SubService(name="Переезд квартир", service_id=9, description="Организация переезда квартир"),
                SubService(name="Переезд офисов", service_id=9, description="Организация переезда офисов"),
                SubService(name="Междугородние переезды", service_id=9, description="Переезды между городами"),
                SubService(name="Международные переезды", service_id=9, description="Переезды за границу"),
                SubService(name="Упаковка и разборка мебели", service_id=9,
                           description="Услуги по упаковке и разборке мебели"),
                SubService(name="Аренда грузовиков", service_id=9, description="Аренда грузовиков для перевозки вещей"),
                SubService(name="Хранение вещей", service_id=9, description="Хранение вещей на складе"),
                SubService(name="Перевозка мебели", service_id=9,
                           description="Перевозка мебели и крупногабаритных предметов"),
                SubService(name="Перевозка пианино", service_id=9, description="Специализированная перевозка пианино"),
                SubService(name="Перевозка автомобилей", service_id=9,
                           description="Перевозка автомобилей на эвакуаторе"),
                # Подкатегории для категории "Финансовые услуги"
                SubService(name="Кредитование", service_id=10, description="Предоставление кредитов и займов"),
                SubService(name="Инвестиции", service_id=10, description="Консультации по инвестициям"),
                SubService(name="Страхование", service_id=10, description="Страхование имущества и жизни"),
                SubService(name="Бухгалтерские услуги", service_id=10, description="Ведение бухгалтерского учета"),
                SubService(name="Налоговое консультирование", service_id=10, description="Консультации по налогам"),
                SubService(name="Финансовое планирование", service_id=10, description="Планирование личных финансов"),
                SubService(name="Аудит", service_id=10, description="Проведение финансового аудита"),
                SubService(name="Консультации по банкротству", service_id=10,
                           description="Помощь в процессе банкротства"),
                SubService(name="Управление активами", service_id=10, description="Управление финансовыми активами"),
                SubService(name="Финансовое образование", service_id=10,
                           description="Обучение основам финансовой грамотности")
            ]
            db.session.bulk_save_objects(initial_sub_services)
            db.session.commit()

        from .models import User
        from .utils import hash_password
        from datetime import datetime

        if User.query.count() == 0:
            initial_users = [
                User(
                    username="admin",
                    password=hash_password("admin123"),
                    role="admin",
                    created_at=datetime.utcnow()
                ),
                User(
                    username="customer",
                    password=hash_password("customer123"),
                    role="customer",
                    created_at=datetime.utcnow()
                ),
                User(
                    username="executor",
                    password=hash_password("executor123"),
                    role="executor",
                    created_at=datetime.utcnow()
                ),
            ]
            db.session.bulk_save_objects(initial_users)
            db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
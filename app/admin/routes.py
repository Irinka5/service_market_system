from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Application, CompletedOrder, User, Service, SubService
from . import admin
from functools import wraps
from ..forms import ApplicationForm, CompleteOrderForm

# Проверка роли администратора
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({"error": "У вас нет прав доступа."}), 403
        return f(*args, **kwargs)

    return decorated_function


# Эндпоинт для отображения панели администратора
@admin.route('/admin/panel', methods=['GET'])
@admin_required
def admin_panel():
    return render_template('admin.html')


# Эндпоинт для получения всех заявок
@admin.route('/admin/get_applications', methods=['GET'])
@admin_required
def get_applications_admin():
    applications = Application.query.all()
    applications_list = [
        {
            "id": app.id,
            "creator_username": User.query.get(app.user_id).username if app.user_id else "Неизвестно",
            "service_type": Service.query.get(app.service_type).name if app.service_type else "Не указано",
            "sub_service": SubService.query.get(app.sub_service).name if app.sub_service else "Не указано",
            "description": app.description,
            "city": app.city,
            "budget": app.budget,
            "status": app.status,
        }
        for app in applications
    ]
    return jsonify({"applications": applications_list})


# Эндпоинт для получения данных заявки для редактирования
@admin.route('/admin/get_application_admin/<int:application_id>', methods=['GET'])
@admin_required
def get_application_admin(application_id):
    application = Application.query.get_or_404(application_id)
    application_data = {
        "id": application.id,
        "description": application.description,
        "status": application.status,
        "service_type": Service.query.get(application.service_type).name if application.service_type else "Не указано",
        "sub_service": SubService.query.get(application.sub_service).name if application.sub_service else "Не указано",
        "city": application.city,
        "budget": application.budget
    }
    return jsonify({"application": application_data})



# Эндпоинт для получения всех завершённых заказов
@admin.route('/admin/get_completed_orders', methods=['GET'])
@admin_required
def get_completed_orders_admin():
    completed_orders = CompletedOrder.query.all()
    orders_list = [
        {
            "id": order.id,
            "executor_username": User.query.get(order.executor_id).username if order.executor_id else "Неизвестно",
            "customer_username": User.query.get(order.requester_id).username if order.requester_id else "Неизвестно",
            "application_id": order.application_id,
            "executor_comment": order.executor_comment,
            "completion_date": order.completion_date.strftime('%Y-%m-%d %H:%M:%S') if order.completion_date else "Не указано",
            "success": order.success
        }
        for order in completed_orders
    ]
    return jsonify({"orders": orders_list})


# Эндпоинт для редактирования заявки
@admin.route('/admin/edit_application/<int:application_id>', methods=['POST'])
@admin_required
def edit_application(application_id):
    application = Application.query.get_or_404(application_id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "Данные для редактирования заявки отсутствуют"}), 400

    # Обновляем поля заявки, если они присутствуют в данных запроса
    if "description" in data:
        application.description = data["description"]
    if "status" in data:
        application.status = data["status"]

    db.session.commit()
    return jsonify({"success": True, "message": "Заявка успешно обновлена"})

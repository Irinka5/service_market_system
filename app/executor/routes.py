from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Application, Service, SubService, CompletedOrder
from ..forms import ApplicationForm
from . import executor
from datetime import datetime


# Эндпоинт для отображения всех доступных заявок исполнителю
@executor.route('/executor/applications', methods=['GET'])
@login_required
def executor_applications():
    if current_user.role != 'executor':
        return "У вас нет прав доступа к этой странице.", 403

    applications = Application.query.filter_by(status='Создана').all()  # Берём все заявки со статусом 'Создана'
    services = Service.query.all()  # Список категорий услуг

    return render_template('application_executor_list.html', applications=applications, services=services)


# Эндпоинт для получения подкатегорий для выбранной категории услуги
@executor.route('/get_sub_services/<int:service_id>', methods=['GET'])
@login_required
def get_sub_services(service_id):
    sub_services = SubService.query.filter_by(service_id=service_id).all()
    sub_services_list = [{"id": sub_service.id, "name": sub_service.name} for sub_service in sub_services]

    return jsonify({"sub_services": sub_services_list})


# Эндпоинт для взятия заявки в исполнение
@executor.route('/take_order/<int:application_id>', methods=['POST'])
@login_required
def take_order(application_id):
    application = Application.query.get_or_404(application_id)
    if application.status != 'Создана':
        return jsonify({"error": "Заявка уже взята или недоступна."}), 400

    application.executor_id = current_user.id
    application.status = 'В работе'
    db.session.commit()

    return jsonify({"success": True})


# Эндпоинт для получения списка взятых исполнителем заказов
@executor.route('/get_taken_orders', methods=['GET'])
@login_required
def get_taken_orders():
    """
    Возвращает список заявок, взятых текущим исполнителем.
    """
    taken_orders = Application.query.filter_by(executor_id=current_user.id, status='В работе').all()

    orders_list = [
        {
            "id": order.id,
            "service_type": order.service.name if order.service else None,
            "sub_service": SubService.query.get(order.sub_service).name if order.sub_service else None,
            "description": order.description,
            "city": order.city,
            "contact_name": order.contact_name,
            "phone": order.phone,
            "email": order.email,
            "budget": order.budget,
            "preferred_date": order.preferred_date.strftime('%Y-%m-%d') if order.preferred_date else None,
            "preferred_time": order.preferred_time.strftime('%H:%M') if order.preferred_time else None,
            "status": order.status,
        }
        for order in taken_orders
    ]

    return jsonify({"orders": orders_list})


# Эндпоинт для завершения заказа
@executor.route('/complete_order/<int:application_id>', methods=['POST'])
@login_required
def complete_order(application_id):
    if current_user.role != 'executor':
        return jsonify({"error": "У вас нет прав на выполнение этой операции."}), 403

    application = Application.query.get_or_404(application_id)

    if application.executor_id != current_user.id:
        return jsonify({"error": "Вы не можете завершить этот заказ, так как вы его не выполняете."}), 403

    if application.status != 'В работе':
        return jsonify({"error": "Только заявки в статусе 'В работе' могут быть завершены."}), 400

    data = request.get_json()
    executor_comment = data.get('executor_comment')
    success = data.get('success')

    # Обновляем статус заявки и создаем запись о завершении заказа
    application.status = 'Завершена'

    completed_order = CompletedOrder(
        executor_id=current_user.id,
        requester_id=application.user_id,
        application_id=application.id,
        executor_comment=executor_comment,
        success=True if success == 'true' else False,
        completion_date=datetime.utcnow()
    )

    db.session.add(completed_order)
    db.session.commit()

    return jsonify({"success": True, "message": "Заказ успешно завершен!"})


# Эндпоинт для получения списка завершённых исполнителем заказов
@executor.route('/get_completed_orders', methods=['GET'])
@login_required
def get_completed_orders():
    if current_user.role != 'executor':
        return jsonify({"error": "У вас нет прав на выполнение этой операции."}), 403

    completed_orders = CompletedOrder.query.filter_by(executor_id=current_user.id).all()

    orders_list = [
        {
            "id": order.application_id,
            "customer_username": order.requester.username,
            "service_type": order.application.service.name if order.application.service else None,
            "sub_service": SubService.query.get(
                order.application.sub_service).name if order.application.sub_service else None,
            "description": order.application.description,
            "city": order.application.city,
            "budget": order.application.budget,
            "success": order.success,
            "executor_comment": order.executor_comment,
        }
        for order in completed_orders
    ]

    return jsonify({"orders": orders_list})

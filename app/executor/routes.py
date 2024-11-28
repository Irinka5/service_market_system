from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Application, Service, SubService, CompletedOrder
from ..forms import ApplicationForm
from . import executor

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
    """
    Взять заявку в исполнение.
    """
    application = Application.query.get_or_404(application_id)

    # Проверяем, что заявка еще не была взята в работу
    if application.status != 'Создана':
        flash('Эту заявку уже кто-то взял в работу.', 'warning')
        return redirect(url_for('executor.application_executor_list'))

    # Обновляем заявку, добавляем исполнителя
    application.executor_id = current_user.id
    application.status = 'В работе'
    db.session.commit()
    flash('Вы успешно взяли заявку в исполнение!', 'success')
    return redirect(url_for('executor.application_executor_list'))


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
            "sub_service": order.sub_service.name if order.sub_service else None,
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

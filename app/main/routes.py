from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import Service, Application, SubService
from ..forms import ApplicationForm
from . import main


@main.route('/')
def index():
    services = Service.query.all()
    return render_template('index.html', services=services)


@main.route('/application/new', methods=['GET', 'POST'])
@login_required
def new_application():
    form = ApplicationForm()

    services = Service.query.all()
    form.service_type.choices = [(service.id, service.name) for service in services]

    if form.service_type.data:
        sub_services = SubService.query.filter_by(service_id=form.service_type.data).all()
        form.sub_service.choices = [(sub_service.id, sub_service.name) for sub_service in sub_services]
    else:
        form.sub_service.choices = []

    # Проверка на валидность формы
    if form.validate_on_submit():
        application = Application(
            user_id=current_user.id,
            service_type=form.service_type.data,
            sub_service=form.sub_service.data,
            description=form.description.data,
            city=form.city.data,
            street=form.street.data,
            house_number=form.house_number.data,
            postal_code=form.postal_code.data,
            contact_name=form.contact_name.data,
            phone=form.phone.data,
            email=form.email.data,
            preferred_date=form.preferred_date.data,
            preferred_time=form.preferred_time.data,
            budget=form.budget.data,
            additional_requirements=form.additional_requirements.data,
            payment_method=form.payment_method.data,
            comments=form.comments.data,
        )
        db.session.add(application)
        db.session.commit()
        flash('Ваша заявка успешно создана!', 'success')
        return redirect(url_for('main.index'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Ошибка в поле {field}: {error}")

    return render_template('application_form.html', form=form, services=services)


@main.route('/applications', methods=['GET'])
@login_required
def application_list():
    return render_template('application_list.html')


@main.route('/api/applications', methods=['GET'])
@login_required
def get_applications():
    """
    Возвращает список заявок (все или только текущего пользователя) в формате JSON.
    """
    # Определяем тип фильтра (все заявки или только пользователя)
    user_only = request.args.get('user_only', default='true', type=str).lower() == 'true'
    query = Application.query

    if user_only:
        query = query.filter_by(user_id=current_user.id)

    applications = query.all()
    application__list = [
        {
            "id": application.id,
            "username": application.user.username if not user_only else None,
            "service_type": application.service_type,
            "sub_service": application.sub_service,
            "description": application.description,
            "city": application.city,
            "budget": application.budget,
        }
        for application in applications
    ]

    return jsonify({"applications": application__list})


@main.route('/api/application/<int:application_id>', methods=['GET'])
@login_required
def get_application_details(application_id):
    application = Application.query.get_or_404(application_id)

    # Convert datetime and time fields to string format before returning JSON
    return jsonify({
        'username': application.user.username,
        'service_type': application.service_type,
        'sub_service': application.sub_service,
        'description': application.description,
        'city': application.city,
        'budget': application.budget,
        'contact_name': application.contact_name,
        'phone': application.phone,
        'email': application.email,
        'preferred_date': application.preferred_date.strftime('%Y-%m-%d') if application.preferred_date else None,
        'preferred_time': application.preferred_time.strftime('%H:%M') if application.preferred_time else None
    })


@main.route('/application/<int:application_id>/update', methods=['GET', 'POST'])
@login_required
def update_application(application_id):
    application = Application.query.get_or_404(application_id)
    if current_user.role not in ['manager', 'admin']:
        flash('У вас нет прав на редактирование этой заявки.', 'danger')
        return redirect(url_for('main.applications'))

    form = ApplicationForm()
    services = Service.query.all()
    form.service_id.choices = [(service.id, service.name) for service in services]

    if form.validate_on_submit():
        application.service_id = form.service_id.data
        application.status = form.status.data
        db.session.commit()
        flash('Заявка успешно обновлена!', 'success')
        return redirect(url_for('main.applications'))

    return render_template('application_form.html', form=form)


@main.route('/application/<int:application_id>/delete', methods=['POST'])
@login_required
def delete_application(application_id):
    application = Application.query.get_or_404(application_id)
    if current_user.role not in ['manager', 'admin']:
        flash('У вас нет прав на удаление этой заявки.', 'danger')
        return redirect(url_for('main.applications'))

    db.session.delete(application)
    db.session.commit()
    flash('Заявка успешно удалена.', 'success')
    return redirect(url_for('main.applications'))


@main.route('/get_sub_services/<int:service_id>', methods=['GET'])
def get_sub_services(service_id):
    sub_services = SubService.query.filter_by(service_id=service_id).all()
    sub_services_data = [{"id": sub_service.id, "name": sub_service.name} for sub_service in sub_services]
    return jsonify(sub_services=sub_services_data)

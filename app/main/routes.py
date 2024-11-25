from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .. import db
from ..models import Service, Application
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
    form.service_id.choices = [(service.id, service.name) for service in services]

    if form.validate_on_submit():
        application = Application(user_id=current_user.id, service_id=form.service_id.data, description=form.description.data)
        db.session.add(application)
        db.session.commit()
        flash('Ваша заявка успешно создана!', 'success')
        return redirect(url_for('main.index'))

    return render_template('application_form.html', form=form)

@main.route('/applications')
@login_required
def applications():
    if current_user.role == 'client':
        applications = Application.query.filter_by(user_id=current_user.id).all()
    elif current_user.role in ['manager', 'admin']:
        applications = Application.query.all()
    else:
        applications = []
    return render_template('application_list.html', applications=applications)

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

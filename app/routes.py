from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User, Service, Application
from .forms import RegistrationForm, LoginForm, ApplicationForm
from . import create_app

app = create_app()


@app.route('/')
def index():
    pass


@app.route('/register', methods=['GET', 'POST'])
def register():
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/logout')
@login_required
def logout():
    pass


@app.route('/application/new', methods=['GET', 'POST'])
@login_required
def new_application():
    pass


@app.route('/applications')
@login_required
def applications():
    pass


@app.route('/application/<int:application_id>/update', methods=['GET', 'POST'])
@login_required
def update_application(application_id):
    pass


@app.route('/application/<int:application_id>/delete', methods=['POST'])
@login_required
def delete_application(application_id):
    pass

import os

from flask import render_template, redirect, url_for, Blueprint
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.utils import secure_filename

from app import db
from app.admin_mod.views import media_prefix_uuid
from app.main.forms import LoginForm, RegistrationForm, EditForm
from app.models import User, Anime

# Define the blueprint: 'main', set its url prefix: app.url/
from config import STATIC

main = Blueprint('main', __name__, url_prefix='/')


@main.route('/', methods=['GET'])
def home():
	animes = Anime.query.all()
	return render_template('main/index.html', title='Home', animes=animes)


@main.route('/user/<int:id>')
def profile(id: id):
	user = User.query.filter_by(id=id).first_or_404()
	return render_template('main/user_profile.html', title=user.username, user=user)


@main.route('/user/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditForm()
	if form.validate_on_submit():
		return redirect(url_for('main.profile', id=current_user.id))
	form.email.data = current_user.email
	return render_template('main/edit_profile.html', title='Editar Prefil', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			return redirect(url_for('main.login'))

		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('main.home'))
	return render_template('main/login.html', title='Sign In', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('main.login'))
	return render_template('main/register.html', title='Register', form=form)


@main.route('/logout', methods=['GET'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('main.home'))

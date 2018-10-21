from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_s3 import FlaskS3
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_htmlmin import HTMLMIN
from flask_talisman import Talisman

from config import CSP

login = LoginManager()
csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
admin = Admin()
s3 = FlaskS3()


def create_app():

	app = Flask(__name__)
	app.config.from_object('config')
	csrf.init_app(app)
	s3.init_app(app)
	login.init_app(app)

	db.init_app(app)
	migrate.init_app(app, db)
	HTMLMIN(app)
	Talisman(app, content_security_policy=CSP)

	class MyAdminIndexView(AdminIndexView):
		@expose('/')
		def index(self):
			if not current_user.is_authenticated:
				return redirect(url_for('main.login'))
			if current_user.is_admin:
				return super(MyAdminIndexView, self).index()
			else:
				return redirect(url_for("main.home"))

	admin.init_app(app, index_view=MyAdminIndexView())
	admin.name = 'Anime Galaxy'
	admin.template_mode = 'bootstrap3'

	from app.admin_mod import views
	from app.main.controllers import main
	from app.anime_mod.controllers import anime_mod

	app.register_blueprint(main)
	app.register_blueprint(anime_mod)

	@app.errorhandler(404)
	def page_not_found(e):
		return render_template('404.html'), 404

	return app

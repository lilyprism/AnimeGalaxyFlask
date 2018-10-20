from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView, expose
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_htmlmin import HTMLMIN

app = Flask(__name__)
app.config.from_object('config')
login = LoginManager(app)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
HTMLMIN(app)


class MyAdminIndexView(AdminIndexView):
	@expose('/')
	def index(self):
		if not current_user.is_authenticated:
			return redirect(url_for('main.login'))
		if current_user.is_admin:
			return super(MyAdminIndexView, self).index()
		else:
			return redirect(url_for("main.home"))


admin = Admin(app, name='Anime Galaxy', template_mode='bootstrap3', index_view=MyAdminIndexView())

from app.admin_mod import views
from app.main.controllers import main
from app.anime_mod.controllers import anime_mod

app.register_blueprint(main)
app.register_blueprint(anime_mod)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

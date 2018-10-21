import uuid

from flask import url_for, redirect, request
from flask_admin.contrib.fileadmin.s3 import S3FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_admin import form, expose
from flask_login import current_user
from werkzeug.utils import secure_filename
from wtforms import PasswordField
from wtforms.validators import DataRequired

import config
from app import admin, db
from app.models import User, Anime, Genre, Episode, Quality, Video
from app.utils import S3ImageUploadField

from config import STATIC


def media_prefix_uuid(obj, file_data):
	return "media/" + secure_filename(f"{uuid.uuid4()}.jpg")


# File View Class to add permission checking, prevent users from seeing page
class FileView(S3FileAdmin):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_admin

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('main.login', next=request.url))


# Custom Model View to add permission checking
class CModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_admin

	def inaccessible_callback(self, name, **kwargs):
		# redirect to login page if user doesn't have access
		return redirect(url_for('main.login', next=request.url))


# Custom Genre View
class GenreView(CModelView):
	def get_edit_form(self):
		return super(GenreView, self).get_edit_form()

	form_excluded_columns = ('animes',)


# Custom Quality View
class QualityView(CModelView):
	column_list = ('name',)
	form_columns = ('name',)


# Custom Video View
class VideoView(CModelView):
	column_list = ('video', 'quality', 'episode')


# Custom User View
class UserView(CModelView):

	@expose('/edit/', methods=('GET', 'POST'))
	def create_view(self):
		id = request.args.get('id')
		if current_user.id != id and not current_user.is_admin:
			return redirect(url_for('main.profile', id=id))
		return super(UserView, self).edit_view()

	form_excluded_columns = ('password_hash',)
	column_list = ('username', 'email', 'is_admin')
	edit_template = 'main/edit_profile.html'

	form_columns = (
		'username',
		'email',
		'password',
		'avatar',
		'banner',
		'is_admin',
	)

	form_extra_fields = {
		'avatar'  : S3ImageUploadField('Avatar', base_path=STATIC, namegen=media_prefix_uuid, max_size=(190, 190, True)),
		'banner'  : S3ImageUploadField('Banner', base_path=STATIC, namegen=media_prefix_uuid, max_size=(1700, 300, True)),
		'password': PasswordField('Password')
	}

	def on_model_change(self, form, User, is_created):
		if form.password.data != '':
			User.set_password(form.password.data)


# Custom Anime View
class AnimeView(CModelView):
	column_list = ('name', 'genres')
	column_select_related_list = ('genres',)
	column_filters = ('genres',)
	form_excluded_columns = ('episodes',)
	# Alternative way to contribute field is to override it completely.
	# In this case, Flask-Admin won't attempt to merge various parameters for the field.
	form_extra_fields = {
		'image': S3ImageUploadField('Image', base_path=STATIC, namegen=media_prefix_uuid, validators=[DataRequired()])
	}


# Custom Episode View
class EpisodeView(CModelView):
	column_list = ('number', 'anime')
	column_select_related_list = ('anime',)
	column_filters = ('anime', 'number')
	form_excluded_columns = ('episodes',)

	form_extra_fields = {
		'image': S3ImageUploadField('Image', base_path=STATIC, namegen=media_prefix_uuid, validators=[DataRequired()])
	}


admin.add_view(UserView(User, db.session))
admin.add_view(AnimeView(Anime, db.session, category="Anime"))
admin.add_view(EpisodeView(Episode, db.session, category="Anime"))
admin.add_view(VideoView(Video, db.session, category="Anime"))
admin.add_view(GenreView(Genre, db.session, category="Config"))
admin.add_view(QualityView(Quality, db.session, category="Config"))
admin.add_view(FileView(config.FLASKS3_BUCKET_NAME, config.FLASKS3_REGION, config.AWS_ACCESS_KEY_ID, config.AWS_SECRET_ACCESS_KEY))

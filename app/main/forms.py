from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email

from app.models import User


class LoginForm(FlaskForm):
	username = StringField('Username:', validators=[DataRequired()])
	password = PasswordField('Password:', validators=[DataRequired()])
	remember_me = BooleanField('Lembrar-me:')
	submit = SubmitField('Entrar')


class RegistrationForm(FlaskForm):
	username = StringField('Username:', validators=[DataRequired()])
	email = StringField('Email:', validators=[DataRequired(), Email()])
	password = PasswordField('Password:', validators=[DataRequired()])
	password2 = PasswordField('Confirmar Password:', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Registar')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Porfavor utilize um username diferente.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Porfavor utilize um email diferente.')


class EditForm(FlaskForm):
	username = StringField('Username:', validators=[DataRequired()])
	email = StringField('Email:', validators=[DataRequired(), Email()])
	password = PasswordField('Confirmar Password:', validators=[DataRequired()])
	avatar = FileField(validators=[FileAllowed('image', 'Image only!')])
	banner = FileField(validators=[FileAllowed('image', 'Image only!')])
	submit = SubmitField('Editar')

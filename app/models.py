import os

from sqlalchemy.event import listens_for
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from flask_login import UserMixin
from config import STATIC

# Many to Many Relationship Table ( Anime <-> Genre )
anime_genres = db.Table('anime_genres',
                        db.Column('anime_id', db.Integer, db.ForeignKey('anime.id'), primary_key=True),
                        db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True))


# Many to Many Relationship Table ( Episode <-> User )
class UserRatedEpisodes(db.Model):
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'), primary_key=True)

	liked = db.Column(db.Boolean, default=False)
	disliked = db.Column(db.Boolean, default=False)

	episode = db.relationship("Episode", backref=db.backref('users_rated', lazy='dynamic', cascade='all,delete-orphan'))
	user = db.relationship('User', backref=db.backref('rated_episodes', lazy='dynamic', cascade='all,delete-orphan'))


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	avatar = db.Column(db.Unicode(128), nullable=True)
	banner = db.Column(db.Unicode(128), nullable=True)
	password_hash = db.Column(db.String(128))
	is_admin = db.Column(db.Boolean(), default=False)

	# rated_episodes = db.relationship('Episode', secondary='user_rated_episodes', backref=db.backref('users'), lazy='dynamic')

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


class Genre(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))

	def __str__(self):
		return self.name


class Anime(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True, index=True, nullable=False)
	image = db.Column(db.Unicode(128), nullable=False)
	description = db.Column(db.UnicodeText())
	genres = db.relationship('Genre', secondary=anime_genres, backref=db.backref('animes', lazy='dynamic'))
	episodes = db.relationship('Episode', cascade="all,delete", backref=db.backref('anime'))

	def __str__(self):
		return self.name


class Episode(db.Model):
	id = db.Column(db.Integer, index=True, primary_key=True)
	image = db.Column(db.Unicode(128), nullable=False)
	number = db.Column(db.Float(), nullable=False)
	anime_id = db.Column(db.Integer(), db.ForeignKey('anime.id'), nullable=False)
	videos = db.relationship('Video', cascade="all,delete", backref=db.backref('episode'))

	@property
	def e_number(self):
		ep = str(self.number)
		return ep[:-2] if ep.endswith(".0") else ep

	def __str__(self):
		anime_name = Anime.query.get(self.anime_id)
		return f"{anime_name} - {self.e_number}"


class Quality(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True, index=True, nullable=False)
	videos = db.relationship('Video', cascade="all,delete", backref=db.backref('quality'))

	def __str__(self):
		return self.name


class Video(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	video = db.Column(db.Unicode(180), nullable=False)
	quality_id = db.Column(db.Integer(), db.ForeignKey('quality.id'), nullable=False)
	episode_id = db.Column(db.Integer(), db.ForeignKey('episode.id'), nullable=False)

	def __str__(self):
		return str(self.video)


@listens_for(Anime, 'after_delete')
@listens_for(Episode, 'after_delete')
def del_image(mapper, connection, target):
	if target.image:
		try:
			os.remove(os.path.join(STATIC, target.image))
		except OSError:
			pass


@listens_for(User, 'after_delete')
def del_avatar_banner(mapper, connection, target):
	if target.avatar:
		try:
			os.remove(os.path.join(STATIC, target.avatar))
		except OSError:
			pass
	if target.banner:
		try:
			os.remove(os.path.join(STATIC, target.banner))
		except OSError:
			pass


@login.user_loader
def load_user(id: int):
	return User.query.get(int(id))

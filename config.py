# Statement for enabling the development environment
import os

DEBUG = False

# BASE_DIR = abspath(dirname(__file__))

# Define the application STATIC and MEDIA path
STATIC = '/static'
MEDIA_PATH = '/static/media'

# Enable HTML Minification
MINIFY_PAGE = True

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:admin@127.0.0.1:5432/AnimeGalaxy')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "SUPERDUCKINGSECRETKEY"

# Secret key for signing cookies
SECRET_KEY = "SUPERDUCKINGSECRETKEY"

# AWS CONFIG
FLASKS3_BUCKET_NAME = 'anime-galaxy'
FLASKS3_REGION = 'eu-west-2'
AWS_ACCESS_KEY_ID = 'AKIAJSZT2QEAJX4WX6UQ'
AWS_SECRET_ACCESS_KEY = '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'
FLASKS3_ACTIVE = True
FLASKS3_DEBUG = DEBUG
FLASKS3_GZIP = True
FLASKS3_GZIP_ONLY_EXTS = ['.js', '.css']
FLASKS3_FORCE_MIMETYPE = True
FLASKS3_FILEPATH_HEADERS = {
	r'.css$': {
		'Content-Type': 'text/css',
	}
}

CSP = {
		'default-src': [
			'\'self\'',
			'anime-galaxy.s3.amazonaws.com'
		],

		'img-src'    : '*',
		'style-src'  : [
			'\'self\'',
			'stackpath.bootstrapcdn.com',
			'use.fontawesome.com',
			'anime-galaxy.s3.amazonaws.com',
			'\'unsafe-inline\''
		],
		'script-src': [
			'\'self\'',
			'code.jquery.com',
			'stackpath.bootstrapcdn.com',
			'use.fontawesome.com',
			'anime-galaxy.s3.amazonaws.com',
			'\'unsafe-inline\''
		],
		'font-src': '*'
	}

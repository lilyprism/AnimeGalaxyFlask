# Statement for enabling the development environment
DEBUG = True

# Define the application directory
from os.path import abspath, dirname, join

BASE_DIR = abspath(dirname(__file__))

# Define the application STATIC and MEDIA path
STATIC = join(dirname(__file__), 'app\static')
MEDIA_PATH = join(dirname(__file__), 'app\static\media')

# Enable HTML Minification
MINIFY_PAGE = True

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'postgres://uqmgfiflobiwcf:6dbf877b48810819ecabdea67cb7ba7ace818d31ccc7c01e317cf7cd548f95f8@ec2-23-21-147-71.compute-1.amazonaws.com:5432' \
                          '/d5e7c2n50ucg1l'  # 'postgresql+psycopg2://postgres:admin@127.0.0.1:5432/AnimeGalaxy'
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

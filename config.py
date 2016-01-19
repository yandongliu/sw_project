# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    THREADS_PER_PAGE = 2
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    # Flask-User settings
    USER_APP_NAME  = "Shuwen"  # Used by email templates
    USER_LOGIN_TEMPLATE = 'user/login.html'
    USER_REGISTER_TEMPLATE = 'user/register.html'
    USER_FORGOT_PASSWORD_TEMPLATE = 'user/forgot_password.html'

    # Flask-Mail settings
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'gmail address')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'gmail pwd')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', '"MyApp" <noreply@example.com>')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '465'))
    MAIL_USE_SSL = int(os.getenv('MAIL_USE_SSL', True))


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

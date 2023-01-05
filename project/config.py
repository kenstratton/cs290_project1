# config.py


import os


class BaseConfig(object):
    # Builds path named 'my_blog' that is through the same path with this module.
    SECRET_KEY = 'secret_key'
    SECURITY_PASSWORD_SALT = 'secret_key_two'
    DEBUG = False
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # mail settings
    MAIL_SERVER = 'smtp.mail.yahoo.co.jp'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # mail authentication
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

    # mail accounts
    MAIL_DEFAULT_SENDER = 'from@example.com'


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///logbase.db'
    DEBUG_TB_ENABLED = True


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'secret_key'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG_TB_ENABLED = False
    STRIPE_SECRET_KEY = 'stripe_secret_key'
    STRIPE_PUBLISHABLE_KEY = 'stripe_publishable_key'
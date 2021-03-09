import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """General configuration variables"""

    # flask specific application configurations
    DEBUG = False
    TESTING = False
    ENV = None

    SECRET_KEY = b"\x1c\x92\x07\xc8\xea\xbbA\xa1\x04\xac\xa4I\xc5\x11\x9b\xb1"
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = "postgres://paywuadmin:paywu123@localhost:5432/paywu"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TEMPLATES_AUTO_RELOAD = True

    AFRI_TALK_USER = None
    AFRI_TALK_KEY = None

    APP_NAME = "paywu"


class DevelopmentConfig(Config):
    """
    Configuration variables when in development mode
    """

    """Development Mode configuration"""
    DEBUG = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "db.sqlite3")}'
    ENV = "development"
    AFRI_TALK_USER = "sandbox"
    AFRI_TALK_KEY = "3f1bc65b1c29fa85a02c1f99ad4bcc52c1c1c2178aadfbb1d24e8510c94c52e6"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


class ProductionConfig(Config):
    """Production Mode configuration"""

    CSRF_ENABLED = True
    ENV = "production"

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
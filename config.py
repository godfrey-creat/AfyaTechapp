class Config:
    SECRET_KEY = '33969889'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'


    DEBUG = False

    WTF_CSRF_ENABLED = True

    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 487
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'your-email@example.com'
    MAIL_PASSWORD = 'your-email-password'

import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

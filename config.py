from dataclasses import dataclass
from distutils.command.config import config
from distutils.debug import DEBUG
import os



db_name = os.environ['RDS_DB_NAME']
db_user = os.environ['RDS_USERNAME']
db_pass = os.environ['RDS_PASSWORD']
db_host = os.environ['RDS_HOSTNAME']
db_port = os.environ['RDS_PORT']
proddb = f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
secret_key = os.getenv('SECRET_KEY')
email_host = "smtp.gmail.com"


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = secret_key
    DATABASE_URL = proddb
    EMAIL_HOST = email_host


class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

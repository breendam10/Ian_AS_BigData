import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Usa diretamente a URL do .env (mysql://maps to mysql+mysqldb via mysqlclient)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
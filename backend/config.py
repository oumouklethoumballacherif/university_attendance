

# config.py
import os

class Config:
    # Chaîne de connexion MySQL
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:MYSQL123@localhost/gestion_presence'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)

"""
settings.py

Configuration for Flask app

"""

class Config:
    SECRET_KEY = "this-is-a-secret-key"
    debug = False

class Production(Config):
    debug = True
    ADMIN = "podeveloperwer@gmail.com"
    SQLALCHEMY_DATABASE_URI = 'mysql+gaerdbms:///scholarship?instance=seokinseokinseokinseokin:seokinseokinseokinseokin-sql'
    migration_directory = 'migrations'
import os

class Config:

    DATABASE_USER = 'root'
    DATABASE_PASS = ''
    DATABASE_HOST = 'localhost'
    DATABASE_DB = 'bela_projekt'

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASS}"
        f"@{DATABASE_HOST}/{DATABASE_DB}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jako-tajni-kljuc-za-belu'
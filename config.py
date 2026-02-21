import os

class Config:

    DATABASE_USER = 'apelko'
    DATABASE_PASS = '1191250989'
    DATABASE_HOST = 'rwa.studenti.math.hr'
    DATABASE_DB = 'apelko_bela'

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASS}"
        f"@{DATABASE_HOST}/{DATABASE_DB}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jako-tajni-kljuc-za-belu'
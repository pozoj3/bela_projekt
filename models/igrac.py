from database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "igraci"

    id_igraca = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    jel_registriran = db.Column(db.Boolean, default=False)
    mail = db.Column(db.Text, nullable=False)
    br_odigranih = db.Column(db.Integer, default=0)
    br_pobjeda = db.Column(db.Integer, default=0)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def dodaj_odigranu(self):
        self.br_odigranih += 1

    def dodaj_pobjedu(self):
        self.br_pobjeda += 1

    def __repr__(self):
        return f"<Igrac {self.username}>"


from database import db

class Igra(db.Model):
    __tablename__ = 'igra'

    id_igre = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_sobe = db.Column(db.Integer, db.ForeignKey('soba.id_sobe'), nullable=False)
    
    br_bodova_vi = db.Column(db.Integer, default=0)
    br_bodova_mi = db.Column(db.Integer, default=0)
    
    zadnji_dijelio = db.Column(db.Integer, db.ForeignKey('igrac.id'))

    runde = db.relationship('Runda', backref='igra', lazy=True, cascade="all, delete-orphan")

class RundaModel(db.Model):
    __tablename__ = 'runda'

    id_runde = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_igre = db.Column(db.Integer, db.ForeignKey('igra.id_igre'), nullable=False)
    redni_broj = db.Column(db.Integer, nullable=False)
    adut = db.Column(db.String(1))
    # ADUT ĆE BIT H/K/T/P
    pobjednik_stiha = db.Column(db.Integer)

    karte = db.relationship('RundaKarte', backref='runda', lazy=True, cascade="all, delete-orphan")
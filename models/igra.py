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
    igrac_koji_zove = db.Column(db.Integer, nullable=False)
    faza_igre = db.Column(db.Enum('zvanje', 'igranje', 'kraj'), nullable=False)
    djelitelj = db.Column(db.Integer, nullable=False)
    na_redu = db.Column(db.Integer, nullable=False)
    red_igranja = db.Column(db.String(7), nullable=False)
    broj_stiha = db.Column(db.Integer, nullable=False)
    bodovi_mi = db.Column(db.Integer, nullable=False)
    bodovi_vi = db.Column(db.Integer, nullable=False)
    bodovi_zvanja_mi = db.Column(db.Integer, nullable=True)
    bodovi_zvanja_vi = db.Column(db.Integer, nullable=True)
    osvojeni_stihovi_mi = db.Column(db.Integer, nullable=True)
    osvojeni_stihovi_vi = db.Column(db.Integer, nullable=True)

    karte = db.relationship('RundaKarte', backref='runda', lazy=True, cascade="all, delete-orphan")

class RundaKarte(db.Model):
    __tablename__ = 'runda_karte'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_runde = db.Column(db.Integer, db.ForeignKey('runda.id_runde'), nullable=False)
    id_igraca = db.Column(db.Integer, db.ForeignKey('igrac.id'), nullable=False)

    oznaka_karte = db.Column(db.String(2), nullable=False) # NPR. T9, Pk I SLIČNO
    
    # RUKA, IGRAČU VIDLJIVA U RUCI, TALON, ZADNJE DVIJE KARTE DO ZVANJA ADUTA, ODIGRANA, KARTA ODIGRANA
    tip = db.Column(db.Enum('ruka', 'talon', 'odigrana', 'stol'), nullable=False)
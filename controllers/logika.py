from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from database import db
from utils.karta import Karta
from utils.runda import Runda
from models.igra import Igra, RundaModel
from models.soba import Soba
from models.igrac import Igrac

logika_bp = Blueprint('logika', __name__)


def dohvati_rundu_objekt(id_igre):
    igra_db = Igra.query.get(id_igre)

    runda_db = RundaModel.query.filter_by(id_igre = id_igre).order_by(RundaModel.id_runde.desc()).first()

    if not runda_db:
        return None, None
    
    logika_runde = Runda()

    logika_runde.adut = runda_db.adut
    logika_runde.na_redu = 1 #ovo treba dodati u bazu
                             #da more pisati logika_runde.na_redu = runda.db.na_redu

    return runda_db, logika_runde


@logika_bp.route('/pokreni_igru/<int:id_sobe>', methods=['POST'])
def pokreni_igru(id_sobe):
    soba = Soba.query.get_or_404(id_sobe)

    nova_igra = Igra(id_sobe = id_sobe, zadnji_dijelio = 1)
    db.session.add(nova_igra)
    db.session.commit()

    nova_logika = Runda()
    nova_logika.promjesaj_karte()

    nova_runda_db = RundaModel(id_igre=nova_igra.id_igre,
            redni_broj = 1, adut = None, pobjednik_stiha = None)
    
    db.session.add(nova_runda_db)
    db.session.commit()


    #tu treba za spremanje karti

    return jsonify({"status": "uspjeh", "id_igre" : nova_igra.id_igre})


@logika_bp.route("/odigraj_potez", methods=['POST'])
def odigraj_potez():
    data = request.json
    id_igre = data.get("id_igre")
    oznaka_karte = data.get("karta")
    id_igraca = session.get("id_igraca")

    runda_db, logika_runde = dohvati_rundu_objekt(id_igre)
    karta_objekt = Karta(oznaka_karte)
    uspjeh = logika_runde.baci_kartu(id_igraca, karta_objekt)

    if uspjeh:
        # A) Nađi tu kartu u bazi i promijeni joj status iz 'ruka' u 'stol'
        # karta_db = RundaKarte.query.filter_by(runda_id=runda_db.id, oznaka=oznaka_karte).first()
        # karta_db.lokacija = 'stol'

        # B) Provjeri je li gotov štih (4 karte na stolu)
        if len(logika_runde.karte_na_stolu) == 4: # Ovo provjeravaš nakon dodavanja
             # Tvoja logika: logika_runde.pokupi_stih()
             # Ažuriraj bodove u tablici Igra
             pass
        
        db.session.commit()

        return jsonify({"status": "ok", "stanje": "karta_bacena"})
    else:
        return jsonify({"status": "greska", "poruka": "Neispravan potez!"}), 400
    

@logika_bp.route("/stanje_igre/<int:id_igre>", metods=['GET'])
def stanje_igre(id_igre):
    #dodali bumo za crtanje
    pass
    


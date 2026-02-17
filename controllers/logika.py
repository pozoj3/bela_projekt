from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from database import db
from utils.karta import Karta
from utils.runda import Runda
from models.igra import Igra, RundaModel, RundaKarte
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

    mapa_igraca = {
        1: soba.igrac1_id,
        2: soba.igrac2_id,
        3: soba.igrac3_id,
        4: soba.igrac4_id
    }

    for logika_id, karte_lista in nova_logika.ruke.items():
        pravi_id = mapa_igraca[logika_id]

        for karta in karte_lista:
            nova_karta_db = RundaKarte(id_runde = nova_runda_db.id_runde,
                    id_igraca = pravi_id, oznaka_karte = karta.oznaka, tip = "ruka")
            
        db.session.add(nova_karta_db)
    
    for logika_id, karte_lista in nova_logika.taloni.items():
        pravi_id = mapa_igraca[logika_id]

        for karta in karte_lista:
            nova_karta_db = RundaKarte(id_runde = nova_runda_db.id_runde,
                id_igraca = pravi_id, oznaka_karte = karta.oznaka, tip = "talon")
            db.session.add(nova_karta_db)

    db.session.commit()
    
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
        karta_db = RundaKarte.query.filter_by(id_runde = runda_db.id_runde,
                id_igraca = id_igraca, oznaka_karte = oznaka_karte).first()

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
    


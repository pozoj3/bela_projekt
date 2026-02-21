from flask import Blueprint, render_template, redirect, url_for, session, flash, request
import random
from database import db
from utils.karta import Karta
from utils.runda import Runda
from models.igra import Igra, RundaModel, RundaKarte
from models.soba import Soba
from models.igrac import Igrac

logika_bp = Blueprint('logika', __name__)


#vraca rjecnik {logicki_id : stvarni_db_id} i obrnuti rjecnik
def dohvati_mapu_igraca(id_igre):
    igra = Igra.query.get(id_igre)
    if not igra:
        return None, None
    
    soba = Soba.query.get(igra.id_sobe)
    if not soba:
        return None, None

    mapaLS = {
        1 : soba.igrac1_id,
        2 : soba.igrac2_id,
        3 : soba.igrac3_id,
        4 : soba.igrac4_id
    }

    mapaSL = {}
    for logicki_id, stvarni_id in mapaLS.items():
        if stvarni_id is not None:
            mapaSL[stvarni_id] = logicki_id

    return mapaLS, mapaSL



#rekonstruira objekt Runda
def dohvati_rundu_objekt(id_igre):
    runda_db = RundaModel.query.filter_by(id_igre = id_igre).order_by(RundaModel.id_runde.desc()).first()

    if not runda_db:
        return None, None, None
    
    mapaLS, mapaSL = dohvati_mapu_igraca(id_igre)
    if not mapaLS or not mapaSL:
        return None, None, None
    
    logika_runde = Runda()

    red_lista = []
    if runda_db.red_igranja:
        red_lista = [int(x) for x in runda_db.red_igranja.split(',')]

    logika_runde.postavi_stanje_iz_baze(
        adut = runda_db.adut,
        igrac_koji_zove = runda_db.igrac_koji_zove,
        red_igranja = red_lista,
        broj_stiha = runda_db.broj_stiha,
        bodovi_mi = runda_db.bodovi_mi,
        bodovi_vi = runda_db.bodovi_vi,
        bodovi_zvanja_mi = runda_db.bodovi_zvanja_mi,
        bodovi_zvanja_vi= runda_db.bodovi_zvanja_vi,
        osvojeni_stihovi_mi= runda_db.osvojeni_stihovi_mi,
        osvojeni_stihovi_vi= runda_db.osvojeni_stihovi_vi
    )

    sve_karte_db = RundaKarte.query.filter_by(id_runde = runda_db.id_runde).all()

    for karta_db in sve_karte_db:
        logicki_id = mapaSL.get(karta_db.id_igraca)

        if logicki_id:
            karta_log = Karta(karta_db.oznaka_karte)

            if karta_db.tip == 'ruka':
                logika_runde.ruke[logicki_id].append(karta_log)
            elif karta_db.tip == 'talon':
                logika_runde.taloni[logicki_id].append(karta_log)
            elif karta_db.tip == 'stol':
                logika_runde.karte_na_stolu.append(karta_log)
            elif karta_db.tip == 'odigrana':
                logika_runde.bacene_karte[logicki_id].append(karta_log)
                

    return runda_db, logika_runde, mapaSL


@logika_bp.route('/pokreni_igru/<int:id_sobe>', methods=['POST'])
def pokreni_igru(id_sobe):
    soba = Soba.query.get_or_404(id_sobe)

    nova_igra = Igra(id_sobe = id_sobe, zadnji_dijelio = 1) 
    db.session.add(nova_igra)
    db.session.flush()

    prvi_na_redu = random.randint(1, 4)
    nova_logika = Runda()
    nova_logika.promjesaj_karte(prvi_na_redu=prvi_na_redu)

    red_igranja_str = ",".join(str(x) for x in nova_logika.red_igranja)

    nova_runda_db = RundaModel(
        id_igre=nova_igra.id_igre,
        redni_broj=1,
        djelitelj = djelitelj,
        na_redu=prvi_na_redu,
        red_igranja=red_igranja_str,
        broj_stiha=0,
        bodovi_mi=0,
        bodovi_vi=0
        # adut i igrac_koji_zove ostaju prazni (NULL) jer se adut još ne zna!
    )
    
    db.session.add(nova_runda_db)
    db.session.flush()

    mapa_igraca = {
        1: soba.igrac1_id,
        2: soba.igrac2_id,
        3: soba.igrac3_id,
        4: soba.igrac4_id
    }

    for logika_id, karte_lista in nova_logika.ruke.items():
        pravi_id = mapa_igraca[logika_id]
        if pravi_id:
            for karta in karte_lista:
                nova_karta_db = RundaKarte(
                    id_runde = nova_runda_db.id_runde,
                    id_igraca = pravi_id,
                    oznaka_karte = karta.oznaka,
                    tip = "ruka"
                )       
                db.session.add(nova_karta_db)
    
    for logika_id, karte_lista in nova_logika.taloni.items():
        pravi_id = mapa_igraca[logika_id]
        if pravi_id:
            for karta in karte_lista:
                nova_karta_db = RundaKarte(
                    id_runde = nova_runda_db.id_runde,
                    id_igraca = pravi_id,
                    oznaka_karte = karta.oznaka,
                    tip = "talon"
                )  
                db.session.add(nova_karta_db)

    db.session.commit()
    
    return jsonify({"status": "uspjeh", "id_igre" : nova_igra.id_igre})


@logika_bp.route("/zovi_aduta", methods = ['POST'])
def zovi_aduta():
    data = request.json
    id_igre = data.get("id_igre")
    odluka = data.get("odluka")
    id_igraca_session = session.get("id_igraca")

    if not id_igraca_session:
        return jsonify({"status": "greska", "poruka" : "Niste prijavljeni."}), 401
    
    runda_db, logika_runde, mapaSL = dohvati_rundu_objekt(id_igre)

    if not runda_db:
        return jsonify({"status": "greska", "poruka" : "Runda nije pronađena."}), 404
    
    logicki_id = mapaSL.get(id_igraca_session)
    if runda_db.faza_igre != "zvanje": #treba dodati fazu igre
        return jsonify({"status": "greska", "poruka": "Zvanje aduta je već završilo."}), 400
    
    if logicki_id != runda_db.na_redu:
        return jsonify({"status": "greska", "poruka": "Niste vi na redu za zvanje!"}), 403
    

    #igrac veli dalje
    if odluka == "dalje":
        if logicki_id == runda_db.djelitelj:
            return jsonify({"status": "greska", "poruka": "Na musu ste, morate zvati aduta!"}), 400
        
        iduci_na_redu = 1 if logicki_id == 4 else logicki_id + 1
        runda_db.na_redu = iduci_na_redu

        db.session.commit()
        return jsonify({"status": "ok", "poruka": "Rekli ste dalje.", "na_redu": iduci_na_redu})
    

    #igrac bira boju
    elif odluka in ["H", "K", "P", "T"]:
        runda_db.adut = odluka
        runda_db.igrac_koji_zove = logicki_id
        runda_db.faza_igre = "igranje"

        logika_runde.zovi_aduta(odluka, logicki_id)

        for i in range(1,5):
            logika_runde.otkrij_karte(i)
            logika_runde.sortiraj_ruku(i)
            logika_runde.zvanja_karte(i)

        logika_runde.validna_zvanja()
        runda_db.bodovi_zvanja_mi = logika_runde.bodovi_zvanja[1] + logika_runde.bodovi_zvanja[3]
        runda_db.bodovi_zvanja_vi = logika_runde.bodovi_zvanja[2] + logika_runde.bodovi_zvanja[4]

        karte_talon_db = RundaKarte.query.filter_by(id_runde=runda_db.id_runde, tip="talon").all()
        for karta_db in karte_talon_db:
            karta_db.tip = "ruka"

        prvi_baca = 1 if runda_db.djelitelj == 4 else runda_db.djelitelj + 1

        red_liste = [
            prvi_baca, 
            logika_runde.pomoca_za_red(prvi_baca + 1),
            logika_runde.pomoca_za_red(prvi_baca + 2),
            logika_runde.pomoca_za_red(prvi_baca + 3)
        ]
        runda_db.red_igranja = ",".join(str(x) for x in red_liste)
        logika_runde.red_igranja = red_liste

        db.session.commit()

        return jsonify({"status" : "ok", "poruka" : f"Adut je {odluka}.",
                        "na_redu": prvi_baca, "zvanja_mi" : runda_db.bodovi_zvanja_mi,
                        "zvanja_vi": runda_db.bodovi_zvanja_vi})
    
    else:
        return jsonify({"status": "greska", "poruka": "Nepoznata odluka."}), 400




@logika_bp.route("/odigraj_potez", methods=['POST'])
def odigraj_potez():
    data = request.json
    id_igre = data.get("id_igre")
    kliknuta_karta = data.get("kliknuta_karta")
    id_igraca_session = session.get("id_igraca")

    if not id_igre:
        return jsonify({"status" : "greska", "poruka" : "Igra nije pronadena."})
    
    if not id_igraca_session:
        return jsonify({"status" : "greska", "poruka" : "Niste prijavljeni."})
    
    runda_db, logika_runde, mapaSL = dohvati_rundu_objekt(id_igre)

    if not runda_db:
        return jsonify({"status" : "greska", "poruka" : "Runda nije pronadena."})
    
    if runda_db.faza_igre != "igranje":
        return jsonify({"status" : "greska", "poruka" : "Trenutno ne mozete baciti kartu."})
    
    logicki_id = mapaSL.get(id_igraca_session)

    if logicki_id != runda_db.na_redu:
        return jsonify({"status" : "greska", "poruka" : "Niste na redu."})
    
    pokusana_karta = Karta(kliknuta_karta)
    jelBacena = logika_runde.baci_kartu(pokusana_karta= pokusana_karta, br_igraca= logicki_id)
    
    if not jelBacena:
        return jsonify({"status" : "greska", "poruka" : "Ne mozete baciti tu kartu, morate postivati pravila."})   
    
    karta_db = RundaKarte.query.filter_by(id_runde = runda_db.id_runde,
                id_igraca = id_igraca_session, oznaka_karte = kliknuta_karta, tip = "ruka").first()
        
    if karta_db:
        karta_db.tip = "stol"
        
    runda_db.bodovi_zvanja_mi = logika_runde.bodovi_zvanja[1] + logika_runde.bodovi_zvanja[3]
    runda_db.bodovi_zvanja_vi = logika_runde.bodovi_zvanja[2] + logika_runde.bodovi_zvanja[4]

    stanje_odgovor = "karta_bacena"
    if len(logika_runde.karte_na_stolu) == 4:
        logika_runde.pokupi_stih()

        runda_db.bodovi_mi = logika_runde.bodovi_mi
        runda_db.bodovi_vi = logika_runde.bodovi_vi
        runda_db.broj_stiha = logika_runde.broj_stiha
        runda_db.osvojeni_stihovi_mi = logika_runde.osvojeni_stihovi_mi
        runda_db.osvojeni_stihovi_vi = logika_runde.osvojeni_stihovi_vi

        karta_na_stolu_db = RundaKarte.query.filter_by(id_runde = runda_db.id_runde, tip = "stol").all()
        for karta in karta_na_stolu_db:
            karta.tip = "odigrana"
        
        pobjednik = logika_runde.red_igranja[0]
        runda_db.na_redu = pobjednik

        runda_db.red_igranja = ",".join(str(x) for x in logika_runde.red_igranja)

        stanje_odgovor = "stih_gotov"

        if runda_db.broj_stiha == 8:
            logika_runde.konacni_bodovi()

            runda_db.bodovi_mi = logika_runde.bodovi_mi
            runda_db.bodovi_vi = logika_runde.bodovi_vi
            runda_db.faza_igre = "kraj"

            igra_db = Igra.query.get(runda_db.id_igre)
            igra_db.br_bodova_mi += runda_db.bodovi_mi
            igra_db.br_bodova_vi += runda_db.bodovi_vi

            if igra_db.br_bodova_mi >= 1001 or igra_db.br_bodova_vi >= 1001:
                stanje_odgovor = "kraj_igre"

            else:
                novi_djelitelj = 1 if runda_db.djelitelj == 4 else runda_db.djelitelj + 1
                prvi_igra = 1 if novi_djelitelj == 4 else novi_djelitelj + 1

                nova_logika = Runda()
                nova_logika.promjesaj_karte(prvi_na_redu= prvi_igra)

                red_igranja_str = ",".join(str(x) for x in nova_logika.red_igranja)

                nova_runda_db = RundaModel(
                    id_igre = igra_db.id_igre,
                    redni_broj = runda_db.redni_broj + 1,
                    faza_igre = "zvanje",
                    djelitelj = novi_djelitelj,
                    na_redu = prvi_igra,
                    red_igranja = red_igranja_str,
                    broj_stiha = 0, bodovi_mi = 0, bodovi_vi = 0
                )

                db.session.add(nova_runda_db)
                db.session.flush()

                mapaLS, _ = dohvati_mapu_igraca(igra_db.id_igre)

                for logicki_id, karte_lista in nova_logika.ruke.items():
                    for karta in karte_lista:
                        db.session.add(RundaKarte(id_runde = nova_runda_db.id_runde,
                                id_igraca = mapaLS[logicki_id], oznaka_karte = karta.oznaka, tip = "ruka"))
                        
                for logicki_id, karte_lista in nova_logika.taloni.items():
                    for karta in karte_lista:
                        db.session.add(RundaKarte(id_runde = nova_runda_db.id_runde,
                                id_igraca = mapaLS[logicki_id], oznaka_karte = karta.oznaka, tip = "talon"))
        
        else:
            broj_karti_stol = len(logika_runde.karte_na_stolu)
            iduci_igrac = logika_runde.red_igranja[broj_karti_stol]
            runda_db.na_redu = iduci_igrac

        db.session.commit()

        return jsonify({"status" : "ok", "stanje" : stanje_odgovor, "na_redu" : runda_db.na_redu})
        

    

@logika_bp.route("/stanje_igre/<int:id_igre>", methods=['GET'])
def stanje_igre(id_igre):
    id_igraca_session = session.get("id_igraca")

    if not id_igraca_session:
        return jsonify({"status": "greska", "poruka": "Niste prijavljeni."})
    
    runda_db, logika_runde, mapaSL = dohvati_rundu_objekt(id_igre)

    if not runda_db:
        return jsonify({"status": "greska", "poruka": "Runda nije pronađena."})
    
    igra_db = Igra.query.get(id_igre)
    logicki_id = mapaSL.get(id_igraca_session)

    stol_oznake = [k.oznaka for k in logika_runde.karte_na_stolu]

    karta_ruka_oznake = []
    if logicki_id and logicki_id in logika_runde.ruke:
        karta_ruka_oznake = [k.oznaka for k in logika_runde.ruke[logicki_id]]

    trenutni_bodovi_mi = runda_db.bodovi_mi + runda_db.bodovi_zvanja_mi
    trenutni_bodovi_vi = runda_db.bodovi_vi + runda_db.bodovi_zvanja_vi

    stanje = { "status" : "ok",
              "faza_igre" : runda_db.faza_igre,
              "na_redu" : runda_db.na_redu,
              "djelitelj" : runda_db.djelitelj,
              "adut" : runda_db.adut,
              "igrac_koji_zove" : runda_db.igrac_koji_zove,
              "id_ovog_igraca" : logicki_id,
              "karte_igraca" : karta_ruka_oznake,
              "stol" : stol_oznake,
              "rezultat_runde" : { "mi" : trenutni_bodovi_mi, "vi" : trenutni_bodovi_vi},
              "rezultat_ukupno" : {"mi" : igra_db.br_bodova_mi, "vi" : igra_db.br_bodova_vi}}
    
    return jsonify(stanje)
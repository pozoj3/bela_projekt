from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from database import db
from models.igrac import Igrac
from models.soba import Soba

# KREIRAMO BLUEPRINT ZA SVE ŠTO IMA VEZE S LOBBY-JEM
lobby_bp = Blueprint('lobby', __name__)

# RUTA ZA LOBBY
@lobby_bp.route('/lobby')
def prikaz_lobbyja():
    # PROVJERA JE LI KORISNIK ULOGIRAN, AKO NIJE POŠALJEMO GA NA LOGIN
    id_igraca = session.get('id_igraca')
    if not id_igraca:
        return redirect(url_for('auth.login'))

    # DOHVATI PODATKE O IGRACU
    korisnik = Igrac.query.get(id_igraca)
    
    # RENDER TEMPLATE-u ŠALJEMO KORISNIKA KAKO BISMO MOGLI PRIKAZATI LOBBY KAO HOME-SCREEN NEKOG PROFILA
    return render_template('lobby.html', igrac=korisnik)

# RUTA ZA KREIRANJE NOVE SOBE, IGRAČ 1 ZAPOČINJE IGRU
@lobby_bp.route('/kreiraj_sobu', methods=['POST'])
def kreiraj_sobu():

    # PROVJERA JE LI IGRAČ ULOGIRAN, AKO NE ŠALJEMO GA NA LOGIN
    current_id_igraca = session.get('id_igraca')
    if not current_id_igraca:
        return redirect(url_for('auth.login'))

    # IZRADA NOVOG RETKA ZA SOBU, SAMO PRVI IGRAČ
    nova_soba = Soba(
        igrac1_id=current_id_igraca,
        igrac2_id=None,
        igrac3_id=None,
        igrac4_id=None
    )
    
    # DODAVANJE RETKA U TABLICU
    db.session.add(nova_soba)
    db.session.commit()
    

    flash(f"Soba {nova_soba.id_sobe} uspješno kreirana!", "success")
    return redirect(url_for('lobby.ulazak_u_sobu', id_sobe=nova_soba.id_sobe))


# OSTALI IGRAČI SE MOGU NAKNADNO PRIDRUŽITI SOBI
@lobby_bp.route('/pridruzi_se', methods=['POST'])
def pridruzi_se():

    # DOHVATI UNESEN ID SOBE I id_igraca KOJI JE TRENTNO PRIJAVLJEN, AKO JE, AKO NIJE POŠALJI GA NA LOGIN
    id_sobe = request.form.get('id_sobe')
    current_id_igraca = session.get('id_igraca')
    
    if not current_id_igraca:
        return redirect(url_for('auth.login'))

    # SPREMI REDAK SOBE LOKALNO
    soba = Soba.query.get(id_sobe)
    
    # AKO GA NISI PRONAŠAO, BACI GREŠKU
    if not soba:
        flash("Soba ne postoji!", "danger")
        return redirect(url_for('lobby.prikaz_lobbyja'))

    # PROVJERI JE LI IGRAČ VEĆ U SOBI
    if current_id_igraca in [soba.igrac1_id, soba.igrac2_id, soba.igrac3_id, soba.igrac4_id]:
        return redirect(url_for('lobby.ulazak_u_sobu', id_sobe=soba.id_sobe))

    # NAĐI PRVO SLOBODNO MJESTO I DODAJ GA TAMO
    if soba.igrac2_id is None:
        soba.igrac2_id = current_id_igraca
    elif soba.igrac3_id is None:
        soba.igrac3_id = current_id_igraca
    elif soba.igrac4_id is None:
        soba.igrac4_id = current_id_igraca
        # OVDJE MOŽEMO UBACITI DA SE IGRA POKRENE KAD IMAMO 4 IGRAČA
    else:
        # AKO IGRAČ NIJE VEĆ U SOBI, A IMAMO 4 IGRAČA UNUTRA, BACI GREŠKU
        flash("Soba je puna!", "warning")
        return redirect(url_for('lobby.prikaz_lobbyja'))

    # AŽURIRAJ REDAK I POŠALJI IGRAČA U SOBU
    db.session.commit()
    return redirect(url_for('lobby.ulazak_u_sobu', id_sobe=soba.id_sobe))

# RUTA ZA PROMJENU NA SOBU
@lobby_bp.route('/soba/<int:id_sobe>')
def ulazak_u_sobu(id_sobe):
    # UZMI BROJ I PROSLIJEDI GA KAO id_sobe
    soba = Soba.query.get_or_404(id_sobe)
    
    # KADA ĆEMO IMATI KONKRETNIJI NAZIV PROMIJENIT ĆEMO OVO, ALI ŠALJEMO IGRAČA ZA STOL
    # return render_template('stol.html', soba=soba)
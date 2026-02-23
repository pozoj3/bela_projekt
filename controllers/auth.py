from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from database import db
from models.igrac import Igrac

auth_bp = Blueprint('auth', __name__)


# RUTA ZA PRIKAZ LOGIN STRANICE
@auth_bp.route('/', methods=['GET'])
def index():
    return render_template('login.html')


#LOGIN RUTA, PROVJERA KORISNIKA I POSTAVLJANJE SESSION-A
@auth_bp.route('/login', methods=['POST'])
def checklogin():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash("Neispravno korisničko ime ili lozinka.","auth_error")
        return redirect(url_for('auth.index'))

    korisnik = Igrac.query.filter_by(username=username).first()

    # PROVJERI JESMO LI NAŠLI USER-a S TIM IMENOM
    if korisnik:

        # AKO POSTOJI USER, ONDA PROVJERI ŠIFRU
        if not korisnik.check_password(password):
            flash("Neispravno korisničko ime ili lozinka.", "auth_error")
            return redirect(url_for('auth.index'))

        # AKO SMO OVO PREŽIVJELI LOGIN JE DOBAR, PROVJERI JEL REGISTRIRAN
        if not korisnik.jel_registriran:
            flash("Korisnik nije dovršio registraciju.", "auth_error")
            return redirect(url_for('auth.index'))

        # POSTAVI SESSION AKO JE SVE PRIJE PROSLO
        session['id_igraca'] = korisnik.id_igraca
        session['username'] = korisnik.username

        # SVE JE DOBRO, PREUSMJERI KORISNIKA NA LOBBY
        flash("Uspješno ste prijavljeni!", "auth_error")
        return redirect(url_for('lobby.prikaz_lobbyja'))


    # AKO USER NE POSTOJI
    flash("Korisnik ne postoji.", "auth_error")
    return redirect(url_for('auth.index'))


# RUTA ZA REGISTRACIJU, PROVJERA UNOSA I KREIRANJE NOVOG KORISNIKA U BAZI
@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    mail = request.form.get('mail')

    # PROVJERA DA LI SU SVA POLJA POPUNJENA
    if not username or not password or not mail:
        flash("Sva polja su obavezna.", "auth_error")
        return redirect(url_for('auth.index'))

    # PROVJERA POSTOJI LI USER
    postoji = Igrac.query.filter_by(username=username).first()
    if postoji:
        flash("Korisničko ime već postoji.", "auth_error")
        return redirect(url_for('auth.index'))

    # SVE JE DOBRO, KREIRAJ NOVOG KORISNIKA
    novi_igrac = Igrac(
        username=username,
        mail=mail,
        jel_registriran=True,
        br_odigranih=0,
        br_pobjeda=0
    )

    # HASHIRANJE LOZINKE
    novi_igrac.set_password(password)

    # SPREMI KORISNIKA U BAZU
    db.session.add(novi_igrac)
    db.session.commit()

    flash("Registracija uspješna!", "auth_error")
    return redirect(url_for('auth.index'))


@auth_bp.route('/registracija_str')
def registracija_str():
    return render_template('registracija.html')


# RUTA ZA ODJAVU, ČIŠĆENJE SESSION-A I PREUSMJERAVANJE NA LOGIN
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Odjavljeni ste.", "auth_error")
    return redirect(url_for('auth.index'))

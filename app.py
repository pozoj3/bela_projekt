from flask import Flask, render_template, request, redirect, session;
from flask_session import Session;
import pymysql.cursors;
from werkzeug.security import generate_password_hash, check_password_hash;
import secrets;


# KONFIGURACIJA --------

app = Flask(__name__);
app.secret_key = secrets.token_hex(16);

app.config['SESSION_TYPE'] = 'cachelib';
app.config['SESSION_PERMANENT'] = False;

Session(app);

def get_db_connection():
    return pymysql.connect(
        host='rwa.studenti.math.hr',
        user='apelko',
        password='1191250989',
        database='apelko_bela',
        cursorclass=pymysql.cursors.DictCursor
    );

# RUTE --------

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('login.html');

@app.route('/login', methods=['GET','POST'])
def checklogin():
    username = request.form.get('username');
    password = request.form.get('password');
    conn = get_db_connection();
    cursor = conn.cursor();
    cursor.execute("SELECT password_hash, has_registered FROM users WHERE username = %s",(username,));
    user=cursor.fetchone();
    cursor.close();
    conn.close();

    # PROVJERI JESMO LI NAŠLI USER-a S TIM NICKOM
    if(user):

        # AKO POSTOJI USER, ONDA PROVJERI ŠIFRU
        if(not(check_password_hash(user['password_hash'],password))):
            # AKO SMO UŠLI U OVAJ IF ZNAČI DA SU ILI USERNAME ILI LOZINKA NETOČNI
            return redirect('/');
    
        if user['has_registered'] != 1:
            # AKO SMO UŠLI U OVAJ IF ZNAČI DA KORISNIK NIJE DOVRŠIO REGISTRACIJU, KASNIJE ĆEMO TO DODATI
            return redirect('/');
    
        # AKO SMO OVO PREZIVJELI LOGIN JE DOBAR I POSTAVIMO SESSION VARIJABLE I SALJEMO KORISNIKA U LOBBY
        session['username'] = username;
        return redirect('/lobby');

    # AKO SMO DOŠLI NEKIM SLUČAJEM DO KRAJA, A NEMAMO USERA ILI NISMO PRONAŠLI USERA ONDA JAVI GREŠKU I VRATI
    # KORISNIKA NA LOGIN PONOVNO
    if 'username' not in session:
        return redirect('/');

@app.route('/lobby')
def lobby():
    #AKO NETKO DODE U LOBBY BEZ LOGINA VRACAMO GA NATRAG NA LOGIN STRANICU
    if 'username' not in session:
        return redirect('/');
    return render_template('lobby.html');
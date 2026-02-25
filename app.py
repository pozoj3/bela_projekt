from flask import Flask, render_template
from flask_socketio import SocketIO
from config import Config
from database import db

app = Flask(__name__)
app.config.from_object(Config)

# INICIJALIZACIJA ZA SOCKET-e
socketio = SocketIO(app, cors_allowed_origins="*")

from controllers.auth import auth_bp
from controllers.lobby import lobby_bp
from controllers.logika import logika_bp

# Inicijalizacija baze
db.init_app(app)

# Registracija blueprintova
app.register_blueprint(auth_bp)
app.register_blueprint(lobby_bp)
app.register_blueprint(logika_bp)

if __name__ == "__main__":
    socketio.run(app, host = "0.0.0.0", port= 5000, debug=True)

@app.route('/')
def index():
    return render_template("login.html")

from flask import Flask, render_template
from config import Config
from database import db

from controllers.auth import auth_bp
from controllers.lobby import lobby_bp

app = Flask(__name__)
app.config.from_object(Config)

# Inicijalizacija baze
db.init_app(app)

# Registracija blueprintova
app.register_blueprint(auth_bp)
app.register_blueprint(lobby_bp)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def index():
    return render_template("login.html")

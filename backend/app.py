from flask import Flask, render_template, session, redirect, url_for
from db import db
from auth import auth
from routes.admin_routes import admin_bp
from models import Enseignant, Etudiant
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret_key_universite"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MYSQL123@localhost/gestion_presence'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init SQLAlchemy
db.init_app(app)

# Register Blueprints
app.register_blueprint(auth)
app.register_blueprint(admin_bp)

@app.context_processor
def inject_user():
    return {
        'current_user': session.get('user'),  # récupère l'utilisateur connecté depuis la session
        'current_year': datetime.now().year   # année actuelle
    }


# ------------------------
# Dashboards enseignants / étudiants
# ------------------------
@app.route('/enseignant/dashboard')
def dashboard_enseignant():
    if session.get('user') and session['user']['type'] == 'enseignant':
        return render_template('enseignant/dashboard_enseignant.html',
                               current_user=session['user'],
                               current_year=datetime.now().year)
    return redirect(url_for('auth.login'))

@app.route('/etudiant/dashboard')
def dashboard_etudiant():
    if session.get('user') and session['user']['type'] == 'etudiant':
        return render_template('etudiant/dashboard_etudiant.html',
                               current_user=session['user'],
                               current_year=datetime.now().year)
    return redirect(url_for('auth.login'))


# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')


# ------------------------
# Lancement
# ------------------------
if __name__ == '__main__':
    app.run(debug=True)

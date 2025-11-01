from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Admin, Enseignant, Etudiant

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        matricule = request.form['username']
        password = request.form['password']

        # Vérification admin
        admin = Admin.query.filter_by(email=matricule).first()
        if admin and admin.mot_de_passe == password:
            session['user'] = {'type': 'admin', 'id': admin.id_admin, 'name': admin.nom}
            return redirect(url_for('admin.dashboard'))  # blueprint admin

        # Vérification enseignant
        ens = Enseignant.query.filter_by(matricule=matricule).first()
        if ens and ens.mot_de_passe == password:
            session['user'] = {'type': 'enseignant', 'id': ens.id_enseignant, 'name': f"{ens.nom} {ens.prenom}"}
            return redirect(url_for('dashboard_enseignant'))

        # Vérification étudiant
        etu = Etudiant.query.filter_by(matricule=matricule).first()
        if etu:
            session['user'] = {'type': 'etudiant', 'id': etu.id_etudiant, 'name': f"{etu.nom} {etu.prenom}"}
            return redirect(url_for('dashboard_etudiant'))

        flash("Identifiant ou mot de passe incorrect", "error")
        return redirect(url_for('auth.login'))

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

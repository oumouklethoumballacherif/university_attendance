# backend/routes/admin_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Admin, Enseignant, Etudiant, Filiere, Departement, Matiere
from db import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# ----------------------------
# 🔒 DÉCORATEUR : accès admin uniquement
# ----------------------------
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = session.get('user')
        if not user or user.get('type') != 'admin':
            flash("⛔ Accès réservé à l’administrateur.", "error")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper


# ----------------------------
# 🧭 DASHBOARD ADMIN
# ----------------------------
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    return render_template(
        'administrateur/dashboard_admin.html',
        current_user=session['user'],
        current_year=datetime.now().year
    )


# ----------------------------
# 👩‍🏫 CRUD ENSEIGNANTS
# ----------------------------
@admin_bp.route('/teachers')
@admin_required
def manage_teachers():
    teachers = Enseignant.query.all()
    return render_template('administrateur/manage_teachers.html', teachers=teachers)


@admin_bp.route('/teachers/add', methods=['GET', 'POST'])
@admin_required
def add_teacher():
    departements = Departement.query.all()

    if request.method == 'POST':
        matricule = request.form.get('matricule')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        mot_de_passe = request.form.get('mot_de_passe')
        id_departement = request.form.get('id_departement')

        # Vérification des champs obligatoires
        if not (matricule and nom and prenom and mot_de_passe and id_departement):
            flash("⚠️ Veuillez remplir tous les champs obligatoires.", "error")
            return redirect(url_for('admin.add_teacher'))

        try:
            new_teacher = Enseignant(
                matricule=matricule,
                nom=nom,
                prenom=prenom,
                email=email,
                mot_de_passe=mot_de_passe,
                id_departement=int(id_departement)  # Convertir en int pour la clé étrangère
            )
            db.session.add(new_teacher)
            db.session.commit()
            flash("✅ Enseignant ajouté avec succès !", "success")
            return redirect(url_for('admin.manage_teachers'))
        except IntegrityError:
            db.session.rollback()
            flash("❌ Ce matricule ou cet email existe déjà.", "error")
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur serveur : {str(e)}", "error")

    return render_template('teacher/CRUD/add_teacher.html', departements=departements)


@admin_bp.route('/teachers/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_teacher(id):
    teacher = Enseignant.query.get_or_404(id)
    departements = Departement.query.all()

    if request.method == 'POST':
        teacher.matricule = request.form.get('matricule')
        teacher.nom = request.form.get('nom')
        teacher.prenom = request.form.get('prenom')
        teacher.email = request.form.get('email')
        mot_de_passe = request.form.get('mot_de_passe')
        id_departement = request.form.get('id_departement')

        if id_departement:  # Assurer que le département est sélectionné
            teacher.id_departement = int(id_departement)
        if mot_de_passe:  # Mettre à jour le mot de passe seulement si fourni
            teacher.mot_de_passe = mot_de_passe

        try:
            db.session.commit()
            flash("✅ Enseignant modifié avec succès !", "success")
            return redirect(url_for('admin.manage_teachers'))
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur : {str(e)}", "error")

    return render_template('teacher/CRUD/edit_teacher.html', teacher=teacher, departements=departements)


@admin_bp.route('/teachers/delete/<int:id>', methods=['POST'])
@admin_required
def delete_teacher(id):
    teacher = Enseignant.query.get_or_404(id)
    try:
        db.session.delete(teacher)
        db.session.commit()
        flash("✅ Enseignant supprimé avec succès !", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur : {str(e)}", "error")
    return redirect(url_for('admin.manage_teachers'))

# ----------------------------
# 🎓 CRUD ÉTUDIANTS
# ----------------------------
@admin_bp.route('/students')
@admin_required
def manage_students():
    students = Etudiant.query.all()
    filieres = Filiere.query.all()
    return render_template('administrateur/manage_students.html',
                           students=students, filieres=filieres)
@admin_bp.route('/students/add', methods=['GET', 'POST'])
@admin_required
def add_student():
    filieres = Filiere.query.all()

    if request.method == 'POST':
        print(request.form)
        matricule = request.form.get('matricule')
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        mot_de_passe = request.form.get('mot_de_passe')
        filiere_id = request.form.get('filiere_id')
        annee = request.form.get('annee')

        # Vérification des champs
        if not all([matricule, nom, prenom, mot_de_passe, filiere_id, annee]):
            flash("⚠️ Tous les champs sont obligatoires.", "error")
            return redirect(url_for('admin.add_student'))

        try:
            new_student = Etudiant(
                matricule=matricule.strip(),
                nom=nom.strip(),
                prenom=prenom.strip(),
                mot_de_passe=mot_de_passe.strip(),
                filiere_id=int(filiere_id),
                annee=int(annee)
            )
            db.session.add(new_student)
            db.session.commit()
            flash("✅ Étudiant ajouté avec succès !", "success")
            return redirect(url_for('admin.manage_students'))
        except IntegrityError:
            db.session.rollback()
            flash("❌ Ce matricule existe déjà.", "error")
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur : {str(e)}", "error")

    return render_template('student/CRUD/add_student.html', filieres=filieres)


@admin_bp.route('/student/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_student(id):
    student = Etudiant.query.get_or_404(id)
    filieres = Filiere.query.all()

    if request.method == 'POST':
        student.matricule = request.form['matricule']
        student.nom = request.form['nom']
        student.prenom = request.form['prenom']
        mot_de_passe = request.form.get('mot_de_passe')
        student.filiere_id = int(request.form['filiere_id'])
        student.annee = int(request.form['annee'])

        if mot_de_passe:
            student.mot_de_passe = mot_de_passe

        try:
            db.session.commit()
            flash("✅ Étudiant modifié avec succès !", "success")
            return redirect(url_for('admin.manage_students'))
        except IntegrityError:
            db.session.rollback()
            flash("❌ Ce matricule existe déjà.", "error")
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur : {str(e)}", "error")

    return render_template('student/CRUD/edit_student.html', student=student, filieres=filieres)


@admin_bp.route('/students/delete/<int:id>', methods=['POST'])
@admin_required
def delete_student(id):
    student = Etudiant.query.get_or_404(id)
    try:
        db.session.delete(student)
        db.session.commit()
        flash("✅ Étudiant supprimé avec succès !", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur : {str(e)}", "error")
    return redirect(url_for('admin.manage_students'))

#
# ----------- Départements -----------

@admin_bp.route('/departements')
def manage_departements():
    departements = Departement.query.all()
    return render_template('administrateur/manage_departement.html', departements=departements)

@admin_bp.route('/departements/add', methods=['GET', 'POST'])
def add_departement():
    if request.method == 'POST':
        nom = request.form['nom']
        dep = Departement(nom_departement=nom)
        db.session.add(dep)
        db.session.commit()
        return redirect(url_for('admin.manage_departements'))
    return render_template('departements/CRUD/add_departement.html')

@admin_bp.route('/departements/<int:id>/edit', methods=['GET', 'POST'])
def edit_departement(id):
    departement = Departement.query.get_or_404(id)
    if request.method == 'POST':
        departement.nom_departement = request.form['nom']
        db.session.commit()
        return redirect(url_for('admin.manage_departements'))
    return render_template('departements/CRUD/edit_departement.html', departement=departement)

@admin_bp.route('/departements/delete/<int:id>', methods=['POST'])
@admin_required
def delete_departement(id):
    departement = Departement.query.get_or_404(id)
    try:
        # Vérifier si des filières existent dans ce département
        if departement.filieres and len(departement.filieres) > 0:
            flash("❌ Impossible de supprimer ce département car il contient des filières.", "error")
            return redirect(url_for('admin.manage_departements'))

        # Vérifier si des enseignants sont rattachés à ce département
        if departement.enseignants and len(departement.enseignants) > 0:
            flash("❌ Impossible de supprimer ce département car il contient des enseignants.", "error")
            return redirect(url_for('admin.manage_departements'))

        db.session.delete(departement)
        db.session.commit()
        flash("✅ Département supprimé avec succès !", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la suppression : {str(e)}", "error")

    return redirect(url_for('admin.manage_departements'))

# ----------- Filières -----------

@admin_bp.route('/departements/<int:id_departement>/filieres')
def manage_filieres_by_departement(id_departement):
    departement = Departement.query.get_or_404(id_departement)
    filieres = Filiere.query.filter_by(id_departement=id_departement).all()
    return render_template('administrateur/manage_filieres.html', filieres=filieres, departement=departement)

@admin_bp.route('/departements/<int:id_departement>/filieres/add', methods=['GET', 'POST'])
def add_filiere(id_departement):
    departement = Departement.query.get_or_404(id_departement)
    if request.method == 'POST':
        nom = request.form['nom_filiere']
        filiere = Filiere(nom_filiere=nom, id_departement=id_departement)
        db.session.add(filiere)
        db.session.commit()
        return redirect(url_for('admin.manage_filieres_by_departement', id_departement=id_departement))
    return render_template('filieres/CRUD/add_filiere.html', departement=departement)

@admin_bp.route('/filieres/<int:id_filiere>/edit', methods=['GET', 'POST'])
def edit_filiere(id_filiere):
    filiere = Filiere.query.get_or_404(id_filiere)
    if request.method == 'POST':
        filiere.nom_filiere = request.form['nom_filiere']
        db.session.commit()
        return redirect(url_for('admin.manage_filieres_by_departement', id_departement=filiere.id_departement))
    return render_template('filieres/CRUD/edit_filiere.html', filiere=filiere)

@admin_bp.route('/filieres/<int:id_filiere>/delete', methods=['POST'])
def delete_filiere(id_filiere):
    filiere = Filiere.query.get_or_404(id_filiere)
    # Optionnel : supprimer toutes les matières liées
    Matiere.query.filter_by(id_filiere=id_filiere).delete()
    db.session.delete(filiere)
    db.session.commit()
    return redirect(url_for('admin.manage_filieres_by_departement', id_departement=filiere.id_departement))

# ----------- Matières -----------

@admin_bp.route('/filieres/<int:id_filiere>/matieres')
def manage_matieres_by_filiere(id_filiere):
    filiere = Filiere.query.get_or_404(id_filiere)
    matieres = Matiere.query.filter_by(id_filiere=id_filiere).all()
    return render_template('administrateur/manage_matieres.html', matieres=matieres, filiere=filiere)

@admin_bp.route('/filieres/<int:id_filiere>/matieres/add', methods=['GET', 'POST'])
def add_matiere(id_filiere):
    filiere = Filiere.query.get_or_404(id_filiere)
    if request.method == 'POST':
        nom = request.form['nom_matiere']
        code = request.form.get('code')
        matiere = Matiere(nom_matiere=nom, code=code, id_filiere=id_filiere)
        db.session.add(matiere)
        db.session.commit()
        return redirect(url_for('admin.manage_matieres_by_filiere', id_filiere=id_filiere))
    return render_template('matieres/CRUD/add_matiere.html', filiere=filiere)

@admin_bp.route('/matieres/<int:id_matiere>/edit', methods=['GET', 'POST'])
def edit_matiere(id_matiere):
    matiere = Matiere.query.get_or_404(id_matiere)
    if request.method == 'POST':
        matiere.nom_matiere = request.form['nom_matiere']
        matiere.code = request.form.get('code')
        db.session.commit()
        return redirect(url_for('admin.manage_matieres_by_filiere', id_filiere=matiere.id_filiere))
    return render_template('matieres/CRUD/edit_matiere.html', matiere=matiere)

@admin_bp.route('/matieres/<int:id_matiere>/delete', methods=['POST'])
def delete_matiere(id_matiere):
    matiere = Matiere.query.get_or_404(id_matiere)
    db.session.delete(matiere)
    db.session.commit()
    return redirect(url_for('admin.manage_matieres_by_filiere', id_filiere=matiere.id_filiere))
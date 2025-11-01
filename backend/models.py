# models.py
from db import db

# -----------------------------
# Table Admin
# -----------------------------
class Admin(db.Model):
    __tablename__ = "admin"
    id_admin = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)


# -----------------------------
# Table Départements
# -----------------------------
class Departement(db.Model):
    __tablename__ = "departements"
    id_departement = db.Column(db.Integer, primary_key=True)
    nom_departement = db.Column(db.String(100), nullable=False)

    # Relation avec enseignants et filières
    enseignants = db.relationship("Enseignant", backref="departement", lazy=True)
    filieres = db.relationship("Filiere", backref="departement", lazy=True)


# -----------------------------
# Table Filières
# -----------------------------
class Filiere(db.Model):
    __tablename__ = "filieres"
    id_filiere = db.Column(db.Integer, primary_key=True)
    nom_filiere = db.Column(db.String(100), nullable=False)

    id_departement = db.Column(db.Integer, db.ForeignKey("departements.id_departement"), nullable=False)

    # Relations
    matieres = db.relationship("Matiere", backref="filiere", lazy=True)
    etudiants = db.relationship("Etudiant", backref="filiere", lazy=True)


# -----------------------------
# Table Enseignants
# -----------------------------
class Enseignant(db.Model):
    __tablename__ = "enseignants"
    id_enseignant = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(50), nullable=False, unique=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150))
    mot_de_passe = db.Column(db.String(150), nullable=False)

    id_departement = db.Column(db.Integer, db.ForeignKey("departements.id_departement"), nullable=False)


# -----------------------------
# Table Matières
# -----------------------------
class Matiere(db.Model):
    __tablename__ = "matiere"
    id_matiere = db.Column(db.Integer, primary_key=True)
    nom_matiere = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20))

    id_filiere = db.Column(db.Integer, db.ForeignKey("filieres.id_filiere"), nullable=False)


# -----------------------------
# Table Étudiants
# -----------------------------
class Etudiant(db.Model):
    __tablename__ = "etudiant"
    id_etudiant = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(50), unique=True, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    annee = db.Column(db.String(20), nullable=False)
    mot_de_passe = db.Column(db.String(100), nullable=False)
    filiere_id = db.Column(db.Integer, db.ForeignKey("filieres.id_filiere"), nullable=False)

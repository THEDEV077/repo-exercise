from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .database import Base

# Enum pour l'état des exemplaires
class Etat(PyEnum):
    NEUF = "Neuf"
    TRES_BON_ETAT = "Très bon état"
    BON_ETAT = "Bon état"
    USAGE = "Usagé"
    ENDOMMAGE = "Endommagé"

# Enum pour le statut des exemplaires
class Statut(PyEnum):
    EN_RAYON = "En rayon"
    EN_PRET = "En prêt"
    EN_RETARD = "En retard"
    EN_RESERVE = "En réserve"
    EN_TRAVAUX = "En travaux"

# Enum pour la catégorie d'utilisateur
class CategorieUtilisateur(PyEnum):
    OCCASIONNEL = "Occasionnel"
    ABONNE = "Abonné"
    ABONNE_PRIVILEGIE = "Abonné privilégié"

# Enum pour la position du bibliothécaire
class PositionBibliothecaire(PyEnum):
    STAGIAIRE = "Stagiaire"
    PRINCIPAL = "Principal"

# Modèle pour Document (Livre et Périodique)
class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, index=True)
    annee_publication = Column(Integer)
    editeur = Column(String)
    reference = Column(String, unique=True, index=True)

    # Relations
    livres = relationship("Livre", back_populates="document", uselist=False)
    periodiques = relationship("Periodique", back_populates="document", uselist=False)
    exemplaires = relationship("Exemplaire", back_populates="document")

# Modèle pour Livre (sous-type de Document)
class Livre(Base):
    __tablename__ = "livres"

    id_document = Column(Integer, ForeignKey("documents.id"), primary_key=True)
    isbn = Column(String, unique=True)
    auteurs = Column(String)

    # Relation
    document = relationship("Document", back_populates="livres")

# Modèle pour Périodique (sous-type de Document)
class Periodique(Base):
    __tablename__ = "periodiques"

    id_document = Column(Integer, ForeignKey("documents.id"), primary_key=True)
    volume = Column(Integer)
    numero = Column(Integer)
    issn = Column(String, unique=True)

    # Relation
    document = relationship("Document", back_populates="periodiques")

# Modèle pour Exemplaire
class Exemplaire(Base):
    __tablename__ = "exemplaires"

    id = Column(Integer, primary_key=True, index=True)
    id_document = Column(Integer, ForeignKey("documents.id"))
    date_achat = Column(Date)
    etat = Column(Enum(Etat))
    statut = Column(Enum(Statut))

    # Relation
    document = relationship("Document", back_populates="exemplaires")

# Modèle pour Utilisateur
class Utilisateur(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    prenom = Column(String)
    categorie = Column(Enum(CategorieUtilisateur))

    # Relation avec les emprunts
    emprunts = relationship("Emprunt", back_populates="utilisateur")

# Modèle pour Emprunt
class Emprunt(Base):
    __tablename__ = "emprunts"

    id = Column(Integer, primary_key=True, index=True)
    id_utilisateur = Column(Integer, ForeignKey("utilisateurs.id"))
    id_exemplaire = Column(Integer, ForeignKey("exemplaires.id"))
    id_bibliothecaire = Column(Integer, ForeignKey("bibliothecaires.id"))
    date_debut = Column(Date)
    date_fin = Column(Date)

    # Relations
    utilisateur = relationship("Utilisateur", back_populates="emprunts")
    exemplaire = relationship("Exemplaire")
    bibliothecaire = relationship("Bibliothecaire", back_populates="emprunts")

# Modèle pour Bibliothécaire
class Bibliothecaire(Base):
    __tablename__ = "bibliothecaires"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String)
    position = Column(Enum(PositionBibliothecaire))

    emprunts = relationship("Emprunt", back_populates="bibliothecaire")
from fastapi import FastAPI, HTTPException, Depends,Request
from pydantic import BaseModel
from typing import List, Annotated, Optional
from app import models
from app.database import engine, SessionLocal
from sqlalchemy.orm import Session
from app.models import Document , CategorieUtilisateur, Utilisateur, Exemplaire, Statut ,Etat, Emprunt, PositionBibliothecaire, Bibliothecaire
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


app = FastAPI()


# Allow CORS for your frontend
origins = [
    "http://127.0.0.1:5500",  # Your frontend's origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



# @app.get("/")
# async def read_root():
#     return FileResponse("frontend/index.html")

class DocumentCreate(BaseModel):
    titre: str
    annee_publication: int
    editeur: str
    reference: str

@app.post("/documents/")
def create_document(document: DocumentCreate, db: Session = Depends(get_db)):
    new_document = Document(**document.dict())
    db.add(new_document)
    db.commit()
    db.refresh(new_document)
    return new_document

@app.get("/documents/")
def read_documents( db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return documents

@app.get("/documents/{document_id}")
def read_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@app.delete("/documents/{document_id}")
def delete_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(document)
    db.commit()
    return {"message": "Document deleted successfully"}

@app.put("/documents/{document_id}")
def update_document(document_id: int, updated_data: DocumentCreate, db: Session = Depends(get_db)):
    # Récupérer le document existant dans la base de données
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Mise à jour des champs du document
    for key, value in updated_data.dict().items():
        setattr(document, key, value)
    
    # Sauvegarder les modifications dans la base de données
    db.commit()
    db.refresh(document)
    
    return document



class UtilisateurCreate(BaseModel):
    nom: str
    prenom: str
    categorie: CategorieUtilisateur

@app.post("/utilisateurs/")
def create_utilisateur(utilisateur: UtilisateurCreate, db: Session = Depends(get_db)):
    new_user = Utilisateur(**utilisateur.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/utilisateurs/")
def read_utilisateurs( db: Session = Depends(get_db)):
    utilisateurs = db.query(Utilisateur).all()
    return utilisateurs



class ExemplaireCreate(BaseModel):
    id_document: int
    date_achat: str
    etat: Etat
    statut: Statut 

@app.post("/exemplaires/")
def create_exemplaire(exemplaire: ExemplaireCreate, db: Session = Depends(get_db)):
    new_exemplaire = Exemplaire(**exemplaire.dict())
    db.add(new_exemplaire)
    db.commit()
    db.refresh(new_exemplaire)
    return new_exemplaire

@app.get("/exemplaires/document/{document_id}")
def get_exemplaires_by_document(document_id: int, db: Session = Depends(get_db)):
    exemplaires = db.query(Exemplaire).filter(Exemplaire.id_document == document_id).all()
    return exemplaires


class EmpruntCreate(BaseModel):
    id_utilisateur: int
    id_exemplaire: int
    id_bibliothecaire: int
    date_debut: Optional[str]
    date_fin: Optional[str]

@app.post("/emprunts/")
def create_emprunt(emprunt: EmpruntCreate, db: Session = Depends(get_db)):
    new_emprunt = Emprunt(**emprunt.dict())
    db.add(new_emprunt)
    db.commit()
    db.refresh(new_emprunt)
    return new_emprunt

@app.get("/emprunts/utilisateur/{utilisateur_id}")
def get_emprunts_by_user(utilisateur_id: int, db: Session = Depends(get_db)):
    emprunts = db.query(Emprunt).filter(Emprunt.id_utilisateur == utilisateur_id).all()
    return emprunts


class BibliothecaireCreate(BaseModel):
    nom: str
    position: PositionBibliothecaire

@app.post("/bibliothecaires/")
def create_bibliothecaire(bibliothecaire: BibliothecaireCreate, db: Session = Depends(get_db)):
    new_bibliothecaire = Bibliothecaire(**bibliothecaire.dict())
    db.add(new_bibliothecaire)
    db.commit()
    db.refresh(new_bibliothecaire)
    return new_bibliothecaire

@app.get("/bibliothecaires/")
def read_bibliothecaires( db: Session = Depends(get_db)):
    bibliothecaires = db.query(Bibliothecaire).all()
    return bibliothecaires
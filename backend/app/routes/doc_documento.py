from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud.doc_documento import (
    create_documento, get_documento, get_documentos,
    update_documento, delete_documento
)
from app.schemas.doc_documento import DocumentoCreate, DocumentoRead, DocumentoUpdate

router = APIRouter(prefix="/documentos", tags=["Documentos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DocumentoRead)
def create_documento_route(documento: DocumentoCreate, db: Session = Depends(get_db)):
    try:
        return create_documento(db, documento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[DocumentoRead])
def list_documentos_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_documentos(db, skip, limit)


@router.get("/{id_documento}", response_model=DocumentoRead)
def read_documento_route(id_documento: str, db: Session = Depends(get_db)):
    db_doc = get_documento(db, id_documento)
    if not db_doc:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return db_doc


@router.put("/{id_documento}", response_model=DocumentoRead)
def update_documento_route(id_documento: str, documento: DocumentoUpdate, db: Session = Depends(get_db)):
    try:
        updated = update_documento(db, id_documento, documento)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not updated:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return updated


@router.delete("/{id_documento}")
def delete_documento_route(id_documento: str, db: Session = Depends(get_db)):
    deleted = delete_documento(db, id_documento)
    if not deleted:
        raise HTTPException(status_code=404, detail="Documento não encontrado")
    return {"msg": "Documento excluído com sucesso"}

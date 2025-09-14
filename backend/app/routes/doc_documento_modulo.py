from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud.doc_documento_modulo import (
    create_doc_modulo, get_doc_modulos, delete_doc_modulo
)
from app.schemas.doc_documento_modulo import DocumentoModuloCreate, DocumentoModuloRead

router = APIRouter(prefix="/documentos-modulos", tags=["Documentos x Módulos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DocumentoModuloRead)
def create_assoc_route(assoc: DocumentoModuloCreate, db: Session = Depends(get_db)):
    return create_doc_modulo(db, assoc)


@router.get("/{id_documento}", response_model=list[DocumentoModuloRead])
def list_assocs_route(id_documento: str, db: Session = Depends(get_db)):
    return get_doc_modulos(db, id_documento)


@router.delete("/{id_documento}/{id_modulo}")
def delete_assoc_route(id_documento: str, id_modulo: int, db: Session = Depends(get_db)):
    deleted = delete_doc_modulo(db, id_documento, id_modulo)
    if not deleted:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return {"msg": "Associação removida com sucesso"}

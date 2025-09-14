from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud.doc_documento_chunk import (
    create_chunk, get_chunks_by_document, delete_chunks_by_document
)
from app.schemas.doc_documento_chunk import DocumentoChunkCreate, DocumentoChunkRead

router = APIRouter(prefix="/documentos-chunks", tags=["Documentos x Chunks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DocumentoChunkRead)
def create_chunk_route(chunk: DocumentoChunkCreate, db: Session = Depends(get_db)):
    return create_chunk(db, chunk)


@router.get("/{id_documento}", response_model=list[DocumentoChunkRead])
def list_chunks_route(id_documento: str, db: Session = Depends(get_db)):
    return get_chunks_by_document(db, id_documento)


@router.delete("/{id_documento}")
def delete_chunks_route(id_documento: str, db: Session = Depends(get_db)):
    delete_chunks_by_document(db, id_documento)
    return {"msg": "Chunks excluídos com sucesso"}

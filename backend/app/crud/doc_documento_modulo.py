from sqlalchemy.orm import Session
from app.models.doc_documento_modulo import DocumentoModulo
from app.schemas.doc_documento_modulo import DocumentoModuloCreate


def create_doc_modulo(db: Session, assoc: DocumentoModuloCreate):
    db_assoc = DocumentoModulo(**assoc.dict())
    db.add(db_assoc)
    db.commit()
    db.refresh(db_assoc)
    return db_assoc


def get_doc_modulos(db: Session, id_documento: str):
    return db.query(DocumentoModulo).filter(DocumentoModulo.id_documento == id_documento).all()


def delete_doc_modulo(db: Session, id_documento: str, id_modulo: int):
    assoc = db.query(DocumentoModulo).filter(
        DocumentoModulo.id_documento == id_documento,
        DocumentoModulo.id_modulo == id_modulo
    ).first()
    if not assoc:
        return None
    db.delete(assoc)
    db.commit()
    return assoc

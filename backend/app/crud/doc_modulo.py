from sqlalchemy.orm import Session
from app.models.doc_modulo import Modulo
from app.models.doc_sistema import Sistema
from app.schemas.doc_modulo import ModuloCreate, ModuloUpdate


def create_modulo(db: Session, modulo: ModuloCreate):
    # Valida se o sistema existe
    sistema = db.query(Sistema).filter(Sistema.id_sistema == modulo.id_sistema).first()
    if not sistema:
        raise ValueError("Sistema não encontrado")

    db_modulo = Modulo(**modulo.dict())
    db.add(db_modulo)
    db.commit()
    db.refresh(db_modulo)
    return db_modulo


def get_modulo(db: Session, id_modulo: int):
    return db.query(Modulo).filter(Modulo.id_modulo == id_modulo).first()


def get_modulos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Modulo).offset(skip).limit(limit).all()


def update_modulo(db: Session, id_modulo: int, modulo: ModuloUpdate):
    db_modulo = get_modulo(db, id_modulo)
    if not db_modulo:
        return None

    if modulo.id_sistema is not None:
        sistema = db.query(Sistema).filter(Sistema.id_sistema == modulo.id_sistema).first()
        if not sistema:
            raise ValueError("Sistema não encontrado")

    for key, value in modulo.dict(exclude_unset=True).items():
        setattr(db_modulo, key, value)

    db.commit()
    db.refresh(db_modulo)
    return db_modulo


def delete_modulo(db: Session, id_modulo: int):
    db_modulo = get_modulo(db, id_modulo)
    if not db_modulo:
        return None
    db.delete(db_modulo)
    db.commit()
    return db_modulo

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud.doc_modulo import (
    create_modulo, get_modulo, get_modulos,
    update_modulo, delete_modulo
)
from app.schemas.doc_modulo import ModuloCreate, ModuloRead, ModuloUpdate

router = APIRouter(prefix="/modulos", tags=["Módulos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ModuloRead)
def create_modulo_route(modulo: ModuloCreate, db: Session = Depends(get_db)):
    try:
        return create_modulo(db, modulo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ModuloRead])
def list_modulos_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_modulos(db, skip, limit)


@router.get("/{id_modulo}", response_model=ModuloRead)
def read_modulo_route(id_modulo: int, db: Session = Depends(get_db)):
    db_modulo = get_modulo(db, id_modulo)
    if not db_modulo:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")
    return db_modulo


@router.put("/{id_modulo}", response_model=ModuloRead)
def update_modulo_route(id_modulo: int, modulo: ModuloUpdate, db: Session = Depends(get_db)):
    try:
        updated = update_modulo(db, id_modulo, modulo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not updated:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")
    return updated


@router.delete("/{id_modulo}")
def delete_modulo_route(id_modulo: int, db: Session = Depends(get_db)):
    deleted = delete_modulo(db, id_modulo)
    if not deleted:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")
    return {"msg": "Módulo excluído com sucesso"}

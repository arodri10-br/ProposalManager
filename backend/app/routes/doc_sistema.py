from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud.doc_sistema import (
    create_sistema, get_sistema, get_sistemas,
    update_sistema, delete_sistema
)
from app.schemas.doc_sistema import SistemaCreate, SistemaRead, SistemaUpdate

router = APIRouter(prefix="/sistemas", tags=["Sistemas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=SistemaRead)
def create_sistema_route(sistema: SistemaCreate, db: Session = Depends(get_db)):
    try:
        return create_sistema(db, sistema)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[SistemaRead])
def list_sistemas_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_sistemas(db, skip, limit)


@router.get("/{id_sistema}", response_model=SistemaRead)
def read_sistema_route(id_sistema: int, db: Session = Depends(get_db)):
    db_sistema = get_sistema(db, id_sistema)
    if not db_sistema:
        raise HTTPException(status_code=404, detail="Sistema não encontrado")
    return db_sistema


@router.put("/{id_sistema}", response_model=SistemaRead)
def update_sistema_route(id_sistema: int, sistema: SistemaUpdate, db: Session = Depends(get_db)):
    try:
        updated = update_sistema(db, id_sistema, sistema)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not updated:
        raise HTTPException(status_code=404, detail="Sistema não encontrado")
    return updated


@router.delete("/{id_sistema}")
def delete_sistema_route(id_sistema: int, db: Session = Depends(get_db)):
    deleted = delete_sistema(db, id_sistema)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sistema não encontrado")
    return {"msg": "Sistema excluído com sucesso"}

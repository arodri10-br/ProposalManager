from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud.pm_cliente import (
    create_cliente, get_cliente, get_clientes,
    update_cliente, delete_cliente
)
from app.schemas.pm_cliente import ClienteCreate, ClienteRead, ClienteUpdate

router = APIRouter(prefix="/clientes", tags=["Clientes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ClienteRead)
def create_cliente_route(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return create_cliente(db, cliente)


@router.get("/", response_model=list[ClienteRead])
def list_clientes_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_clientes(db, skip, limit)


@router.get("/{id_cliente}", response_model=ClienteRead)
def read_cliente_route(id_cliente: int, db: Session = Depends(get_db)):
    db_cliente = get_cliente(db, id_cliente)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return db_cliente


@router.put("/{id_cliente}", response_model=ClienteRead)
def update_cliente_route(id_cliente: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    updated = update_cliente(db, id_cliente, cliente)
    if not updated:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return updated


@router.delete("/{id_cliente}")
def delete_cliente_route(id_cliente: int, db: Session = Depends(get_db)):
    deleted = delete_cliente(db, id_cliente)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"msg": "Cliente excluído com sucesso"}

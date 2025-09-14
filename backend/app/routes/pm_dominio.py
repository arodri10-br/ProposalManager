from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

# Importa as funções CRUD
from app.crud.pm_dominio import (
    create_dominio_hd, get_dominios_hd, get_dominio_hd,
    update_dominio_hd, delete_dominio_hd,
    create_dominio_data, get_dominios_data, get_dominio_data,
    update_dominio_data, delete_dominio_data
)

# Importa os schemas
from app.schemas.pm_dominio import (
    DominioHdCreate, DominioHdRead, DominioHdUpdate,
    DominioDataCreate, DominioDataRead, DominioDataUpdate   # <-- adicionar aqui
)


router = APIRouter(prefix="/dominios", tags=["Domínios"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------
# Rotas para pm_dominio_hd
# ------------------------
@router.post("/hd/", response_model=DominioHdRead)
def create_hd_route(hd: DominioHdCreate, db: Session = Depends(get_db)):
    return create_dominio_hd(db, hd)


@router.get("/hd/", response_model=list[DominioHdRead])
def list_hd_route(db: Session = Depends(get_db)):
    return get_dominios_hd(db)


@router.get("/hd/{tabela}", response_model=DominioHdRead)
def read_hd_route(tabela: str, db: Session = Depends(get_db)):
    db_hd = get_dominio_hd(db, tabela)
    if not db_hd:
        raise HTTPException(status_code=404, detail="Domínio não encontrado")
    return db_hd


@router.put("/hd/{tabela}", response_model=DominioHdRead)
def update_hd_route(tabela: str, hd: DominioHdUpdate, db: Session = Depends(get_db)):
    updated = update_dominio_hd(db, tabela, hd)
    if not updated:
        raise HTTPException(status_code=404, detail="Domínio não encontrado")
    return updated

@router.delete("/hd/{tabela}")
def delete_hd_route(tabela: str, db: Session = Depends(get_db)):
    deleted = delete_dominio_hd(db, tabela)
    if not deleted:
        raise HTTPException(status_code=404, detail="Domínio não encontrado")
    return {"msg": "Domínio excluído com sucesso"}


# ------------------------
# Rotas para pm_dominio_data
# ------------------------
@router.post("/data/", response_model=DominioDataRead)
def create_data_route(data: DominioDataCreate, db: Session = Depends(get_db)):
    return create_dominio_data(db, data)


@router.get("/data/{tabela}", response_model=list[DominioDataRead])
def list_data_route(tabela: str, db: Session = Depends(get_db)):
    return get_dominios_data(db, tabela)


@router.get("/data/{tabela}/{chave_valor}", response_model=DominioDataRead)
def read_data_route(tabela: str, chave_valor: str, db: Session = Depends(get_db)):
    db_data = get_dominio_data(db, tabela, chave_valor)
    if not db_data:
        raise HTTPException(status_code=404, detail="Valor de domínio não encontrado")
    return db_data


@router.put("/data/{tabela}/{chave_valor}", response_model=DominioDataRead)
def update_data_route(tabela: str, chave_valor: str, data: DominioDataUpdate, db: Session = Depends(get_db)):
    updated = update_dominio_data(db, tabela, chave_valor, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Valor de domínio não encontrado")
    return updated

@router.delete("/data/{tabela}/{chave_valor}")
def delete_data_route(tabela: str, chave_valor: str, db: Session = Depends(get_db)):
    deleted = delete_dominio_data(db, tabela, chave_valor)
    if not deleted:
        raise HTTPException(status_code=404, detail="Valor de domínio não encontrado")
    return {"msg": "Valor de domínio excluído com sucesso"}

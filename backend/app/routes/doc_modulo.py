# app/routes/doc_modulo.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

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


@router.post(
    "/",
    response_model=ModuloRead,
    summary="Criar módulo",
    description="Cria um novo módulo vinculado a um sistema existente."
)
def create_modulo_route(modulo: ModuloCreate, db: Session = Depends(get_db)):
    try:
        return create_modulo(db, modulo)
    except ValueError as e:
        # Ex.: "Sistema não encontrado" ou violação de regra de domínio
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=List[ModuloRead],
    summary="Listar módulos de um sistema",
    description="Retorna os módulos pertencentes ao sistema informado via parâmetro de query `id_sistema` (obrigatório)."
)
def list_modulos_route(
    id_sistema: int = Query(
        ...,
        title="ID do Sistema",
        description="Identificador do sistema ao qual os módulos pertencem.",
        example=1
    ),
    skip: int = Query(0, ge=0, example=0),
    limit: int = Query(100, ge=1, le=500, example=100),
    db: Session = Depends(get_db),
):
    return get_modulos(db, skip=skip, limit=limit, id_sistema=id_sistema)


@router.get(
    "/by-sistema/{id_sistema}",
    response_model=List[ModuloRead],
    summary="Listar módulos por sistema (atalho RESTful)",
    description="Mesmo resultado da rota `/modulos/`, porém usando `id_sistema` como parâmetro de caminho."
)
def list_modulos_by_sistema_route(
    id_sistema: int,
    skip: int = Query(0, ge=0, example=0),
    limit: int = Query(100, ge=1, le=500, example=100),
    db: Session = Depends(get_db),
):
    return get_modulos(db, skip=skip, limit=limit, id_sistema=id_sistema)


@router.get(
    "/{id_modulo}",
    response_model=ModuloRead,
    summary="Obter módulo por ID",
    description="Recupera os dados de um módulo pelo seu identificador."
)
def read_modulo_route(id_modulo: int, db: Session = Depends(get_db)):
    db_modulo = get_modulo(db, id_modulo)
    if not db_modulo:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")
    return db_modulo


@router.put(
    "/{id_modulo}",
    response_model=ModuloRead,
    summary="Atualizar módulo",
    description="Atualiza os dados de um módulo. Se permitir troca de sistema, valide o novo `id_sistema` no CRUD."
)
def update_modulo_route(id_modulo: int, modulo: ModuloUpdate, db: Session = Depends(get_db)):
    try:
        updated = update_modulo(db, id_modulo, modulo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not updated:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")
    return updated


@router.delete(
    "/{id_modulo}",
    summary="Excluir módulo",
    description="Exclui um módulo pelo identificador."
)
def delete_modulo_route(id_modulo: int, db: Session = Depends(get_db)):
    deleted = delete_modulo(db, id_modulo)
    if not deleted:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")
    return {"msg": "Módulo excluído com sucesso"}

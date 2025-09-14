from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal

# Importando funções CRUD
from app.crud.pm_usuario import (
    create_usuario,
    get_usuario,
    get_usuarios,
    update_usuario,
    delete_usuario
)

# Importando schemas Pydantic
from app.schemas.pm_usuario import UsuarioCreate, UsuarioUpdate, UsuarioRead


router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# Dependency de sessão com o banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UsuarioRead)
def create_usuario_route(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return create_usuario(db, usuario)


@router.get("/{user_id}", response_model=UsuarioRead)
def read_usuario(user_id: int, db: Session = Depends(get_db)):
    db_user = get_usuario(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return db_user


@router.get("/", response_model=list[UsuarioRead])
def list_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_usuarios(db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=UsuarioRead)
def update_usuario_route(user_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    updated = update_usuario(db, user_id, usuario)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return updated


@router.delete("/{user_id}")
def delete_usuario_route(user_id: int, db: Session = Depends(get_db)):
    deleted = delete_usuario(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"msg": "Usuário excluído com sucesso"}

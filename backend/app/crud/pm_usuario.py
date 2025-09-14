from sqlalchemy.orm import Session
from app.models.pm_usuario import Usuario
from app.schemas.pm_usuario import UsuarioCreate, UsuarioUpdate
from app.security.hashing import hash_password

def create_usuario(db: Session, usuario: UsuarioCreate):
    db_user = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=hash_password(usuario.senha),
        status=usuario.status
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_usuario(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.id_usuario == user_id).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Usuario).offset(skip).limit(limit).all()

def update_usuario(db: Session, user_id: int, usuario: UsuarioUpdate):
    db_user = get_usuario(db, user_id)
    if not db_user:
        return None
    for field, value in usuario.dict(exclude_unset=True).items():
        if field == "senha":
            setattr(db_user, "senha_hash", hash_password(value))
        else:
            setattr(db_user, field, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_usuario(db: Session, user_id: int):
    db_user = get_usuario(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

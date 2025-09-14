from sqlalchemy.orm import Session
from app.models.pm_cliente import Cliente
from app.schemas.pm_cliente import ClienteCreate, ClienteUpdate


def create_cliente(db: Session, cliente: ClienteCreate):
    db_cliente = Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def get_cliente(db: Session, id_cliente: int):
    return db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()


def get_clientes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Cliente).offset(skip).limit(limit).all()


def update_cliente(db: Session, id_cliente: int, cliente: ClienteUpdate):
    db_cliente = get_cliente(db, id_cliente)
    if not db_cliente:
        return None
    for key, value in cliente.dict(exclude_unset=True).items():
        setattr(db_cliente, key, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def delete_cliente(db: Session, id_cliente: int):
    db_cliente = get_cliente(db, id_cliente)
    if not db_cliente:
        return None
    db.delete(db_cliente)
    db.commit()
    return db_cliente

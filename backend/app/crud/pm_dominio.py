from sqlalchemy.orm import Session
from app.models.pm_dominio import DominioHd, DominioData
from app.schemas.pm_dominio import DominioHdCreate, DominioDataCreate, DominioDataUpdate


# ------------------------
# pm_dominio_hd
# ------------------------
def create_dominio_hd(db: Session, hd: DominioHdCreate):
    db_hd = DominioHd(**hd.dict())
    db.add(db_hd)
    db.commit()
    db.refresh(db_hd)
    return db_hd


def get_dominios_hd(db: Session):
    return db.query(DominioHd).all()


def get_dominio_hd(db: Session, tabela: str):
    return db.query(DominioHd).filter(DominioHd.tabela == tabela).first()


def update_dominio_hd(db: Session, tabela: str, hd_data):
    db_hd = get_dominio_hd(db, tabela)
    if not db_hd:
        return None
    for key, value in hd_data.dict(exclude_unset=True).items():
        setattr(db_hd, key, value)
    db.commit()
    db.refresh(db_hd)
    return db_hd


def delete_dominio_hd(db: Session, tabela: str):
    db_hd = get_dominio_hd(db, tabela)
    if not db_hd:
        return None
    db.delete(db_hd)
    db.commit()
    return db_hd


# ------------------------
# pm_dominio_data
# ------------------------
def create_dominio_data(db: Session, data: DominioDataCreate):
    db_data = DominioData(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_dominios_data(db: Session, tabela: str):
    return db.query(DominioData).filter(DominioData.tabela == tabela).all()


def get_dominio_data(db: Session, tabela: str, chave_valor: str):
    return (
        db.query(DominioData)
        .filter(DominioData.tabela == tabela, DominioData.chave_valor == chave_valor)
        .first()
    )


def update_dominio_data(db: Session, tabela: str, chave_valor: str, data: DominioDataUpdate):
    db_data = get_dominio_data(db, tabela, chave_valor)
    if not db_data:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(db_data, key, value)
    db.commit()
    db.refresh(db_data)
    return db_data


def delete_dominio_data(db: Session, tabela: str, chave_valor: str):
    db_data = get_dominio_data(db, tabela, chave_valor)
    if not db_data:
        return None
    db.delete(db_data)
    db.commit()
    return db_data

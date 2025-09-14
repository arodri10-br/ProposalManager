from sqlalchemy.orm import Session
from app.models.doc_sistema import Sistema
from app.models.pm_dominio import DominioData
from app.schemas.doc_sistema import SistemaCreate, SistemaUpdate


def create_sistema(db: Session, sistema: SistemaCreate):
    # Valida fornecedor
    fornecedor = db.query(DominioData).filter(
        DominioData.tabela == "FornecedorSistema",
        DominioData.chave_valor == sistema.fornecedor_chave
    ).first()

    if not fornecedor:
        raise ValueError("Fornecedor inválido: precisa estar no domínio FornecedorSistema")

    db_sistema = Sistema(**sistema.dict())
    db.add(db_sistema)
    db.commit()
    db.refresh(db_sistema)
    return db_sistema


def get_sistema(db: Session, id_sistema: int):
    return db.query(Sistema).filter(Sistema.id_sistema == id_sistema).first()


def get_sistemas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Sistema).offset(skip).limit(limit).all()


def update_sistema(db: Session, id_sistema: int, sistema: SistemaUpdate):
    db_sistema = get_sistema(db, id_sistema)
    if not db_sistema:
        return None

    # Se alterar fornecedor, validar
    if sistema.fornecedor_chave is not None:
        fornecedor = db.query(DominioData).filter(
            DominioData.tabela == "FornecedorSistema",
            DominioData.chave_valor == sistema.fornecedor_chave
        ).first()
        if not fornecedor:
            raise ValueError("Fornecedor inválido: precisa estar no domínio FornecedorSistema")

    for key, value in sistema.dict(exclude_unset=True).items():
        setattr(db_sistema, key, value)

    db.commit()
    db.refresh(db_sistema)
    return db_sistema


def delete_sistema(db: Session, id_sistema: int):
    db_sistema = get_sistema(db, id_sistema)
    if not db_sistema:
        return None
    db.delete(db_sistema)
    db.commit()
    return db_sistema

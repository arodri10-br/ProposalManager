from sqlalchemy.orm import Session
from app.models.doc_documento import Documento
from app.models.pm_dominio import DominioData
from app.schemas.doc_documento import DocumentoCreate, DocumentoUpdate


# Função auxiliar para validar domínio
def validar_dominio(db: Session, tabela: str, chave_valor: str):
    return db.query(DominioData).filter(
        DominioData.tabela == tabela,
        DominioData.chave_valor == chave_valor
    ).first()


def create_documento(db: Session, documento: DocumentoCreate):
    if not validar_dominio(db, "ClassificacaoDocumento", documento.classificacao_chave):
        raise ValueError("Classificação inválida: precisa estar no domínio ClassificacaoDocumento")

    if not validar_dominio(db, "RegraRetencao", documento.retencao_chave):
        raise ValueError("Regra de retenção inválida: precisa estar no domínio RegraRetencao")

    db_doc = Documento(**documento.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc


def get_documento(db: Session, id_documento: str):
    return db.query(Documento).filter(Documento.id_documento == id_documento).first()


def get_documentos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Documento).offset(skip).limit(limit).all()


def update_documento(db: Session, id_documento: str, documento: DocumentoUpdate):
    db_doc = get_documento(db, id_documento)
    if not db_doc:
        return None

    if documento.classificacao_chave is not None:
        if not validar_dominio(db, "ClassificacaoDocumento", documento.classificacao_chave):
            raise ValueError("Classificação inválida: precisa estar no domínio ClassificacaoDocumento")

    if documento.retencao_chave is not None:
        if not validar_dominio(db, "RegraRetencao", documento.retencao_chave):
            raise ValueError("Regra de retenção inválida: precisa estar no domínio RegraRetencao")

    for key, value in documento.dict(exclude_unset=True).items():
        setattr(db_doc, key, value)

    db.commit()
    db.refresh(db_doc)
    return db_doc


def delete_documento(db: Session, id_documento: str):
    db_doc = get_documento(db, id_documento)
    if not db_doc:
        return None
    db.delete(db_doc)
    db.commit()
    return db_doc

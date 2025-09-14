from sqlalchemy import Column, String, Integer, CHAR, TIMESTAMP, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.sql import func
from app.core.database import Base


class DominioHd(Base):
    """
    Cabeçalho de tabela de domínio genérica.
    Define os campos e regras para os valores que estarão em pm_dominio_data.
    """
    __tablename__ = "pm_dominio_hd"

    tabela = Column(String(20), primary_key=True)   # nome lógico do domínio
    descricao = Column(String(50), nullable=False)
    chave = Column(String(50), nullable=False)

    campo01 = Column(String(50))
    campo02 = Column(String(50))
    campo03 = Column(String(50))
    campo04 = Column(String(50))
    campo05 = Column(String(50))

    tipo01 = Column(CHAR(1))
    tipo02 = Column(CHAR(1))
    tipo03 = Column(CHAR(1))
    tipo04 = Column(CHAR(1))
    tipo05 = Column(CHAR(1))

    permitenull01 = Column(CHAR(1), default="N")
    permitenull02 = Column(CHAR(1), default="N")
    permitenull03 = Column(CHAR(1), default="N")
    permitenull04 = Column(CHAR(1), default="N")
    permitenull05 = Column(CHAR(1), default="N")

    tamanho01 = Column(Integer)
    tamanho02 = Column(Integer)
    tamanho03 = Column(Integer)
    tamanho04 = Column(Integer)
    tamanho05 = Column(Integer)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"))
    updated_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"))
    updated_ip = Column(String(40))


class DominioData(Base):
    """
    Dados de domínio genéricos.
    Cada linha representa um valor possível em uma tabela de domínio definida em pm_dominio_hd.
    """
    __tablename__ = "pm_dominio_data"

    tabela = Column(String(20), ForeignKey("pm_dominio_hd.tabela"), nullable=False)
    chave_valor = Column(String(50), nullable=False)

    valor01 = Column(String(50))
    valor02 = Column(String(50))
    valor03 = Column(String(50))
    valor04 = Column(String(50))
    valor05 = Column(String(50))

    ativo = Column(CHAR(1), default="S")

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"))
    updated_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"))
    updated_ip = Column(String(40))

    __table_args__ = (
        PrimaryKeyConstraint("tabela", "chave_valor", name="pk_pm_dominio_data"),
    )

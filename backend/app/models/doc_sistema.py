from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship

class Sistema(Base):
    __tablename__ = "doc_sistema"

    id_sistema = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nome_sistema = Column(String(100), nullable=False)

    # Referência semântica ao domínio "FornecedorSistema"
    fornecedor_chave = Column(String(50), nullable=False)

    versao = Column(String(50), nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"), nullable=True)
    updated_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"), nullable=True)
    updated_ip = Column(String(40), nullable=True)

    modulos = relationship("Modulo", back_populates="sistema", cascade="all, delete-orphan")
    created_by_user = relationship("Usuario", foreign_keys=[created_by])
    updated_by_user = relationship("Usuario", foreign_keys=[updated_by])

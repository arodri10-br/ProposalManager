from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Modulo(Base):
    __tablename__ = "doc_modulo"

    id_modulo = Column(Integer, primary_key=True, autoincrement=True)
    id_sistema = Column(Integer, ForeignKey("doc_sistema.id_sistema"), nullable=False)

    nome_modulo = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"), nullable=True)
    updated_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"), nullable=True)
    updated_ip = Column(String(40), nullable=True)

    # Relacionamento
    documentos = relationship("DocumentoModulo", back_populates="modulo")
    sistema = relationship("Sistema", back_populates="modulos")


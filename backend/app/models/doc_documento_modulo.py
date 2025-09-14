from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship


class DocumentoModulo(Base):
    __tablename__ = "doc_documento_modulo"

    id_documento = Column(String(36), ForeignKey("doc_documento.id_documento", ondelete="CASCADE"), primary_key=True)
    id_modulo = Column(Integer, ForeignKey("doc_modulo.id_modulo", ondelete="CASCADE"), primary_key=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"), nullable=True)
    updated_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"), nullable=True)
    updated_ip = Column(String(40), nullable=True)

    documento = relationship("Documento", back_populates="modulos")
    modulo = relationship("Modulo", back_populates="documentos")

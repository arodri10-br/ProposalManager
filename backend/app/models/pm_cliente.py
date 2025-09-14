from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Cliente(Base):
    __tablename__ = "pm_cliente"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome_cliente = Column(String(50), nullable=False)
    cnpj = Column(String(20), nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    updated_ip = Column(String(40), nullable=True)

    # Relacionamento
    documentos = relationship("Documento", back_populates="cliente", cascade="all, delete-orphan")


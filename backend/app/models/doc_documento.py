from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid


class Documento(Base):
    __tablename__ = "doc_documento"

    id_documento = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_cliente = Column(Integer, ForeignKey("pm_cliente.id_cliente"), nullable=False)

    nome_arquivo = Column(Text, nullable=False)
    tipo = Column(String(20), nullable=False)  # BRD, Proposta, Manual, Web
    caminho_rede = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    checksum = Column(String(64), nullable=True)  # SHA256
    texto_original = Column(Text, nullable=True)  # Apenas PUB

    data_upload = Column(TIMESTAMP, server_default=func.now())
    ultima_verificacao = Column(TIMESTAMP, nullable=True)

    classificacao_chave = Column(String(50), nullable=False)  # FK lógica
    retencao_chave = Column(String(50), nullable=False)       # FK lógica

    origem_tipo    = Column(String(10), nullable=True)     # 'UPLOAD' | 'URL'
    origem_nome    = Column(String(255), nullable=True)    # nome lógico
    origem_mime    = Column(String(100), nullable=True)
    origem_sha256  = Column(String(64), nullable=True)
    origem_tamanho = Column(Integer, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"), nullable=True)
    updated_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"), nullable=True)
    updated_ip = Column(String(40), nullable=True)

    # Relacionamentos
    cliente = relationship("Cliente", back_populates="documentos")

    modulos = relationship("DocumentoModulo",back_populates="documento",cascade="all, delete-orphan",passive_deletes=True )
    chunks = relationship("DocumentoChunk",back_populates="documento",cascade="all, delete-orphan",passive_deletes=True)
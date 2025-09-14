# models/doc_documento_chunk.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, LargeBinary, Index, UniqueConstraint
from sqlalchemy.sql import func
from app.core.database import Base
import uuid
from sqlalchemy.orm import relationship

class DocumentoChunk(Base):
    __tablename__ = "doc_documento_chunk"

    id_chunk = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_documento = Column(
        String(36),
        ForeignKey("doc_documento.id_documento", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # já existiam
    chunk_index = Column(Integer, nullable=False)
    texto = Column(Text, nullable=True)     # Apenas se PUB/INT
    embedding = Column(LargeBinary, nullable=False)
    fonte = Column(String(255), nullable=True)  # Ex: "page:3", "paragraph:8", "section:2.1"

    # ✅ novos campos (presentes no schema Pydantic)
    page_number = Column(Integer, nullable=True)
    char_start = Column(Integer, nullable=True)
    char_end = Column(Integer, nullable=True)

    data_insercao = Column(TIMESTAMP, server_default=func.now())
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    created_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"), nullable=True)
    updated_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"), nullable=True)
    updated_ip = Column(String(40), nullable=True)

    documento = relationship("Documento", back_populates="chunks")

    __table_args__ = (
        UniqueConstraint("id_documento", "chunk_index", name="uq_doc_chunk_idx"),
        Index("ix_doc_chunk_page", "id_documento", "page_number"),
    )

from pydantic import BaseModel, Field
from typing_extensions import Annotated
from typing import Optional, List
from datetime import datetime

# Import com forward refs (entre aspas evita dependência circular)
# Se der erro de import circular, pode usar TYPE_CHECKING
from app.schemas.doc_documento_chunk import DocumentoChunkRead
from app.schemas.doc_documento_modulo import DocumentoModuloRead


# ------------------------
# Base
# ------------------------
class DocumentoBase(BaseModel):
    nome_arquivo: str
    tipo: Annotated[str, Field(max_length=20)]   # BRD, Proposta, Manual, Web
    caminho_rede: Optional[str] = None
    url: Optional[str] = None
    checksum: Optional[str] = None
    texto_original: Optional[str] = None
    classificacao_chave: str
    retencao_chave: str


# ------------------------
# Create
# ------------------------
class DocumentoCreate(DocumentoBase):
    id_cliente: int


# ------------------------
# Update
# ------------------------
class DocumentoUpdate(BaseModel):
    nome_arquivo: Optional[str] = None
    tipo: Optional[str] = None
    caminho_rede: Optional[str] = None
    url: Optional[str] = None
    checksum: Optional[str] = None
    texto_original: Optional[str] = None
    classificacao_chave: Optional[str] = None
    retencao_chave: Optional[str] = None


# ------------------------
# Read
# ------------------------
class DocumentoRead(DocumentoBase):
    id_documento: str
    id_cliente: int

    data_upload: datetime
    ultima_verificacao: Optional[datetime] = None

    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    updated_ip: Optional[str] = None

    class Config:
        from_attributes = True


# ------------------------
# Read com relacionamentos
# ------------------------
class DocumentoWithRelations(DocumentoRead):
    chunks: List[DocumentoChunkRead] = []
    modulos: List[DocumentoModuloRead] = []

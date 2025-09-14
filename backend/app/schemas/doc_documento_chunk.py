from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ------------------------
# Base
# ------------------------
class DocumentoChunkBase(BaseModel):
    chunk_index: int
    texto: Optional[str] = None
    embedding: bytes
    fonte: Optional[str] = None
    page_number: Optional[int] = None
    char_start: Optional[int] = None
    char_end: Optional[int] = None
    fonte: Optional[str] = None  


# ------------------------
# Create
# ------------------------
class DocumentoChunkCreate(DocumentoChunkBase):
    id_documento: str


# ------------------------
# Update
# ------------------------
class DocumentoChunkUpdate(BaseModel):
    texto: Optional[str] = None
    embedding: Optional[bytes] = None
    fonte: Optional[str] = None
    page_number: Optional[int] = None
    char_start: Optional[int] = None
    char_end: Optional[int] = None


# ------------------------
# Read
# ------------------------
class DocumentoChunkRead(DocumentoChunkBase):
    id_chunk: str
    id_documento: str

    data_insercao: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    updated_ip: Optional[str] = None

    class Config:
        from_attributes = True

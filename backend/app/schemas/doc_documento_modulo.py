from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DocumentoModuloBase(BaseModel):
    id_documento: str
    id_modulo: int


class DocumentoModuloCreate(DocumentoModuloBase):
    pass


class DocumentoModuloRead(DocumentoModuloBase):
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    updated_ip: Optional[str] = None

    class Config:
        from_attributes = True

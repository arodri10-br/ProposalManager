from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ModuloBase(BaseModel):
    id_sistema: int
    nome_modulo: str = Field(..., max_length=100)
    descricao: Optional[str] = None


class ModuloCreate(ModuloBase):
    pass


class ModuloUpdate(BaseModel):
    id_sistema: Optional[int] = None
    nome_modulo: Optional[str] = Field(None, max_length=100)
    descricao: Optional[str] = None


class ModuloRead(ModuloBase):
    id_modulo: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    updated_ip: Optional[str] = None

    class Config:
        from_attributes = True

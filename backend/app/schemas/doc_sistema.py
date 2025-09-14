from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SistemaBase(BaseModel):
    nome_sistema: str = Field(..., max_length=100)
    fornecedor_chave: str = Field(..., max_length=50, description="Código do fornecedor (domínio FornecedorSistema)")
    versao: Optional[str] = Field(None, max_length=50)


class SistemaCreate(SistemaBase):
    pass


class SistemaUpdate(BaseModel):
    nome_sistema: Optional[str] = Field(None, max_length=100)
    fornecedor_chave: Optional[str] = Field(None, max_length=50)
    versao: Optional[str] = Field(None, max_length=50)


class SistemaRead(SistemaBase):
    id_sistema: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    updated_ip: Optional[str] = None

    class Config:
        from_attributes = True

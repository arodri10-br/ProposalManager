from pydantic import BaseModel, StringConstraints, Field
from typing import Optional, Annotated
from datetime import datetime


# Definições de tipos com restrições
NomeCliente = Annotated[str, StringConstraints(max_length=50)]
CNPJ = Annotated[str, StringConstraints(max_length=20)]


class ClienteBase(BaseModel):
    nome_cliente: NomeCliente
    cnpj: Optional[CNPJ] = None


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome_cliente: Optional[NomeCliente] = None
    cnpj: Optional[CNPJ] = None


class ClienteRead(ClienteBase):
    id_cliente: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    updated_ip: Optional[str] = None

    class Config:
        from_attributes = True

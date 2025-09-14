from pydantic import BaseModel, constr
from typing import Optional, Annotated
from datetime import datetime


class UsuarioBase(BaseModel):
    nome: Annotated[str, constr(max_length=50)]
    email: Annotated[str, constr(max_length=50)]
    status: Optional[str] = "A"


class UsuarioCreate(UsuarioBase):
    senha: str


class UsuarioUpdate(BaseModel):
    nome: Optional[Annotated[str, constr(max_length=50)]]
    email: Optional[Annotated[str, constr(max_length=50)]]
    status: Optional[str]
    senha: Optional[str]


class UsuarioRead(UsuarioBase):
    id_usuario: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True   # substitui orm_mode no Pydantic v2

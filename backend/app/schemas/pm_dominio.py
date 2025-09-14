from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ------------------------
# Cabeçalho de domínio (já existia)
# ------------------------
class DominioHdBase(BaseModel):
    tabela: str
    descricao: str
    chave: str
    campo01: Optional[str] = None
    campo02: Optional[str] = None
    campo03: Optional[str] = None
    campo04: Optional[str] = None
    campo05: Optional[str] = None
    tipo01: Optional[str] = None
    tipo02: Optional[str] = None
    tipo03: Optional[str] = None
    tipo04: Optional[str] = None
    tipo05: Optional[str] = None
    permitenull01: Optional[str] = "N"
    permitenull02: Optional[str] = "N"
    permitenull03: Optional[str] = "N"
    permitenull04: Optional[str] = "N"
    permitenull05: Optional[str] = "N"
    tamanho01: Optional[int] = None
    tamanho02: Optional[int] = None
    tamanho03: Optional[int] = None
    tamanho04: Optional[int] = None
    tamanho05: Optional[int] = None


class DominioHdCreate(DominioHdBase):
    pass


class DominioHdUpdate(BaseModel):
    descricao: Optional[str] = None
    chave: Optional[str] = None
    campo01: Optional[str] = None
    campo02: Optional[str] = None
    campo03: Optional[str] = None
    campo04: Optional[str] = None
    campo05: Optional[str] = None
    tipo01: Optional[str] = None
    tipo02: Optional[str] = None
    tipo03: Optional[str] = None
    tipo04: Optional[str] = None
    tipo05: Optional[str] = None
    permitenull01: Optional[str] = None
    permitenull02: Optional[str] = None
    permitenull03: Optional[str] = None
    permitenull04: Optional[str] = None
    permitenull05: Optional[str] = None
    tamanho01: Optional[int] = None
    tamanho02: Optional[int] = None
    tamanho03: Optional[int] = None
    tamanho04: Optional[int] = None
    tamanho05: Optional[int] = None


class DominioHdRead(DominioHdBase):
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    updated_ip: Optional[str] = None

    class Config:
        from_attributes = True


# ------------------------
# Dados de domínio (NOVO)
# ------------------------
class DominioDataBase(BaseModel):
    tabela: str
    chave_valor: str
    valor01: Optional[str] = None
    valor02: Optional[str] = None
    valor03: Optional[str] = None
    valor04: Optional[str] = None
    valor05: Optional[str] = None
    ativo: Optional[str] = "S"


class DominioDataCreate(DominioDataBase):
    """Para inserts (tabela e chave_valor são obrigatórios)."""
    pass


class DominioDataUpdate(BaseModel):
    """Para updates (todos opcionais)."""
    valor01: Optional[str] = None
    valor02: Optional[str] = None
    valor03: Optional[str] = None
    valor04: Optional[str] = None
    valor05: Optional[str] = None
    ativo: Optional[str] = None


class DominioDataRead(DominioDataBase):
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    updated_ip: Optional[str] = None

    class Config:
        from_attributes = True

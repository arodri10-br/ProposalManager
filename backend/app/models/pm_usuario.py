from sqlalchemy import Column, Integer, String, CHAR, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "pm_usuario"

    id_usuario = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    status = Column(CHAR(1), nullable=False, default="A")

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    created_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"), nullable=True)
    updated_by = Column(Integer, ForeignKey("pm_usuario.id_usuario"), nullable=True)
    updated_ip = Column(String(40), nullable=True)

    created_by_user = relationship("Usuario",remote_side=[id_usuario],foreign_keys=[created_by],backref="usuarios_criados")
    updated_by_user = relationship("Usuario",remote_side=[id_usuario],foreign_keys=[updated_by],backref="usuarios_atualizados"
                                   )

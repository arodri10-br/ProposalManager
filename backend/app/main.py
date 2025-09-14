from fastapi import FastAPI
from app.core.database import Base, engine

# Imports explícitos das rotas
import app.routes.pm_usuario as pm_usuario
import app.routes.pm_dominio as pm_dominio
import app.routes.pm_cliente as pm_cliente
import app.routes.doc_sistema as doc_sistema
import app.routes.doc_modulo as doc_modulo
import app.routes.doc_documento as doc_documento
import app.routes.doc_documento_modulo as doc_documento_modulo
import app.routes.doc_documento_chunk as doc_documento_chunk
import app.routes.doc_upload as doc_upload
# Garante que todas as tabelas serão criadas no banco (somente em dev/sqlite)
Base.metadata.create_all(bind=engine)

# Inicializa aplicação FastAPI
app = FastAPI(title="Proposal Manager")

# Inclui os routers
app.include_router(pm_usuario.router)
app.include_router(pm_dominio.router)
app.include_router(pm_cliente.router)
app.include_router(doc_sistema.router)
app.include_router(doc_modulo.router)
app.include_router(doc_documento.router)
app.include_router(doc_documento_modulo.router)
app.include_router(doc_documento_chunk.router)
app.include_router(doc_upload.router)
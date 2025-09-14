from fastapi import FastAPI, Request
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.datastructures import UploadFile as StarletteUploadFile  

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

app.add_middleware(CORSMiddleware,
  allow_origins=["*"], allow_credentials=False,
  allow_methods=["*"], allow_headers=["*"])

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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    content_type = request.headers.get("content-type")
    form_keys = None
    files_info = {}

    try:
        # Só tenta ler form se for multipart
        if content_type and content_type.startswith("multipart/form-data"):
            form = await request.form()
            form_keys = list(form.keys())
            # 🔒 Só trata como arquivo quando for UploadFile de verdade
            for k, v in form.multi_items():
                if isinstance(v, StarletteUploadFile):
                    files_info[k] = {
                        "filename": v.filename,
                        "content_type": getattr(v, "content_type", None),
                    }
        else:
            form_keys = []
    except Exception as e:
        form_keys = f"<não consegui parsear form: {e}>"

    # Log seguro (sem tocar em atributos de string)
    print(
        "[422] ",
        request.method, str(request.url),
        f"CT={content_type}",
        f"errors={exc.errors()}",
        f"form_keys={form_keys}",
        f"file_fields={list(files_info.keys())}",
        sep=" | "
    )

    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
            "content_type": content_type,
            "form_keys": form_keys,
            "files": files_info,
            "query": dict(request.query_params),
        },
    )
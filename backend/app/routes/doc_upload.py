# app/routes/doc_upload.py
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Union, TypedDict, cast, Any
from starlette.datastructures import UploadFile as StarletteUploadFile

import os
import uuid
import pickle
import io
import json
import hashlib
import mimetypes
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

# DOCX (opcional)
try:
    from docx import Document as DocxDocument
except Exception:
    DocxDocument = None

from app.core.database import SessionLocal
from app.crud.doc_documento import create_documento
from app.crud.doc_documento_modulo import create_doc_modulo
from app.crud.doc_documento_chunk import create_chunk
from app.schemas.doc_documento import DocumentoCreate
from app.schemas.doc_documento_modulo import DocumentoModuloCreate
from app.schemas.doc_documento_chunk import DocumentoChunkCreate
from app.utils.embeddings import gerar_embedding

router = APIRouter(prefix="/upload", tags=["Upload de Documentos"])

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# Helpers de chunking
# ---------------------------

def chunk_by_chars(text: str, max_chars: int = 1200, overlap: int = 200, base_start: int = 0) -> List[Dict[str, Any]]:
    """
    Divide 'text' em janelas de tamanho 'max_chars' com sobreposição 'overlap'.
    Retorna dicts: {'texto','char_start','char_end'}.
    Offsets são ABSOLUTOS (base_start = deslocamento inicial).
    """
    chunks: List[Dict[str, Any]] = []
    n = len(text)
    i = 0
    while i < n:
        end = min(i + max_chars, n)
        chunk_txt = text[i:end]
        chunks.append({
            "texto": chunk_txt,
            "char_start": base_start + i,
            "char_end": base_start + end
        })
        if end == n:
            break
        i = max(0, end - overlap)
    return chunks


def extract_pdf_chunks(file_bytes: bytes, max_chars: int = 1200, overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Extrai texto página a página e gera chunks com page_number e offsets absolutos.
    """
    reader = PdfReader(io.BytesIO(file_bytes))
    all_chunks: List[Dict[str, Any]] = []
    global_offset = 0

    for page_idx, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        page_chunks = chunk_by_chars(page_text, max_chars=max_chars, overlap=overlap, base_start=global_offset)
        for c in page_chunks:
            c["page_number"] = page_idx
        all_chunks.extend(page_chunks)
        # +1 por quebra entre páginas (mantém consistência com concatenação com "\n")
        global_offset += len(page_text) + 1

    return all_chunks


def extract_plaintext_chunks(text: str, max_chars: int = 1200, overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Chunking para texto “flat” (TXT/HTML/DOCX). Sem page_number. Offsets absolutos.
    """
    chunks = chunk_by_chars(text, max_chars=max_chars, overlap=overlap, base_start=0)
    for c in chunks:
        c["page_number"] = None
    return chunks


def extract_docx_plaintext_and_chunks(file_bytes: bytes, max_chars: int = 1200, overlap: int = 200):
    """
    Lê .docx e retorna (texto_completo, chunks) com offsets absolutos (sem página).
    """
    if DocxDocument is None:
        raise HTTPException(status_code=500, detail="Leitura DOCX indisponível. Instale 'python-docx'.")
    doc = DocxDocument(io.BytesIO(file_bytes))
    paragraphs = [p.text or "" for p in doc.paragraphs]
    full_text = "\n".join(paragraphs)
    chunks = extract_plaintext_chunks(full_text, max_chars=max_chars, overlap=overlap)
    return full_text, chunks

# ---------------------------
# Helpers de referência de origem (para CONF/INT)
# ---------------------------

class OriginRef(TypedDict):
    ref: str
    sha: str
    size: int
    mime: str


def build_origin_ref(filename: str, content_type: Optional[str], raw: bytes) -> OriginRef:
    ctype = content_type or (mimetypes.guess_type(filename or "")[0] or "application/octet-stream")
    sha = hashlib.sha256(raw).hexdigest()
    size = len(raw)
    ref = f"upload:{filename}|mime:{ctype}|sha256:{sha}|size:{size}"
    return {"ref": ref, "sha": sha, "size": size, "mime": ctype}


def build_origin_ref_from_url(nome_arquivo: str, html_bytes: bytes) -> OriginRef:
    sha = hashlib.sha256(html_bytes).hexdigest()
    size = len(html_bytes)
    ref = f"url:{nome_arquivo}|mime:text/html|sha256:{sha}|size:{size}"
    return {"ref": ref, "sha": sha, "size": size, "mime": "text/html"}


def normalize_modulos(modulos: Optional[Union[List[int], List[str], str]]) -> List[int]:
    if not modulos:
        return []
    if isinstance(modulos, list):
        out: List[int] = []
        for m in modulos:
            if m is None:
                continue
            s = str(m).strip()
            if not s:
                continue
            out.append(int(s))
        return out
    # string: tenta JSON, senão CSV
    s = str(modulos).strip()
    try:
        parsed = json.loads(s)
        if isinstance(parsed, list):
            return [int(x) for x in parsed]
        return [int(parsed)]
    except Exception:
        return [int(x) for x in s.split(",") if x.strip()]


# ---------------------------
# Endpoint
# ---------------------------

@router.post("/")
async def upload_documento(
    request: Request,
    id_cliente: int = Form(...),
    nome_arquivo: str = Form(...),
    tipo: str = Form(...),
    classificacao_chave: str = Form(...),  # CONF, INT, PUB
    retencao_chave: str = Form(...),       # RET5Y, RET10Y, ETERNAL
    modulos: Optional[Union[List[int], List[str], str]] = Form(None),
    url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    cls = classificacao_chave.upper()
    ret = retencao_chave.upper()

    # 1) Criar documento
    doc_create = DocumentoCreate(
        id_cliente=id_cliente,
        nome_arquivo=nome_arquivo,
        tipo=tipo,
        caminho_rede=None,
        url=url,
        checksum=None,
        texto_original=None,
        classificacao_chave=classificacao_chave,
        retencao_chave=retencao_chave
    )
    documento = create_documento(db, doc_create)

    # 2) Associar módulos (se houver)
    for id_modulo in normalize_modulos(modulos):
        assoc = DocumentoModuloCreate(
            id_documento=str(documento.id_documento),
            id_modulo=id_modulo
        )
        create_doc_modulo(db, assoc)

    # 3) Extrair conteúdo e gerar chunks enriquecidos
    texto = ""
    chunks_meta: List[Dict[str, Any]] = []
    origin: Optional[OriginRef] = None
    file_bytes: Optional[bytes] = None

    # Upload de arquivo
    file_is_upload = isinstance(file, StarletteUploadFile) and bool(getattr(file, "filename", ""))
    if file_is_upload:
        upload_file = cast(StarletteUploadFile, file)
        file_bytes = await upload_file.read()
        fname = (upload_file.filename or "").lower()
        ctype = getattr(upload_file, "content_type", "") or (mimetypes.guess_type(upload_file.filename or "")[0] or "")

        if fname.endswith(".pdf") or ctype == "application/pdf":
            # PDF: chunks com page_number
            chunks_meta = extract_pdf_chunks(file_bytes, max_chars=1200, overlap=200)
            try:
                # Texto completo via concatenação de chunks gigantes (mantém +1 por página)
                texto = "\n".join([c["texto"] for c in extract_pdf_chunks(file_bytes, max_chars=10**9, overlap=0)])
            except Exception:
                reader = PdfReader(io.BytesIO(file_bytes))
                texto = "\n".join([(p.extract_text() or "") for p in reader.pages])

        elif fname.endswith(".docx") or ctype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            if DocxDocument is None:
                raise HTTPException(status_code=500, detail="Instale 'python-docx' para suportar arquivos .docx.")
            texto, chunks_meta = extract_docx_plaintext_and_chunks(file_bytes, max_chars=1200, overlap=200)

        else:
            # Fallback texto plano (txt, md, csv etc.)
            try:
                texto = file_bytes.decode("utf-8", errors="ignore")
            except Exception:
                texto = ""
            chunks_meta = extract_plaintext_chunks(texto, max_chars=1200, overlap=200)

        # Referência de origem via hash (sempre calculamos)
        origin = build_origin_ref(upload_file.filename or "", ctype, file_bytes)

        # Políticas de armazenamento
        if cls in ("CONF", "INT"):
            # Não salvar arquivo; apenas guardar referência simbólica
            setattr(documento, "caminho_rede", origin["ref"])
        elif cls == "PUB":
            unique_name = f"{uuid.uuid4()}_{upload_file.filename or 'arquivo'}"
            save_path = os.path.join(UPLOAD_DIR, unique_name)
            with open(save_path, "wb") as f:
                f.write(file_bytes)
            setattr(documento, "caminho_rede", save_path)
        elif ret == "ETERNAL":
            setattr(documento, "caminho_rede", origin["ref"])

        db.commit()
        db.refresh(documento)

    # Scraping de URL
    elif url:
        try:
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                )
            }
            resp = requests.get(url, headers=headers, timeout=(10, 60), allow_redirects=True)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            texto = soup.get_text(separator="\n", strip=True)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao acessar URL: {e}")

        chunks_meta = extract_plaintext_chunks(texto, max_chars=1200, overlap=200)

        html_bytes = resp.content or resp.text.encode("utf-8", errors="ignore")
        origin = build_origin_ref_from_url(nome_arquivo, html_bytes)

        if cls in ("CONF", "INT"):
            setattr(documento, "caminho_rede", origin["ref"])
        elif cls == "PUB":
            unique_name = f"{uuid.uuid4()}_{nome_arquivo}"
            save_path = os.path.join(UPLOAD_DIR, unique_name)
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(resp.text)
            setattr(documento, "caminho_rede", save_path)
        elif ret == "ETERNAL":
            setattr(documento, "caminho_rede", origin["ref"])

        db.commit()
        db.refresh(documento)

    else:
        # Nem file nem url enviados
        raise HTTPException(status_code=400, detail="Envie 'file' (multipart) ou 'url' (texto).")

    # 4) Se for público, reter texto original
    if cls == "PUB" and texto:
        setattr(documento, "texto_original", texto)
        db.commit()
        db.refresh(documento)

    # 5) Persistir chunks + embeddings com metadados (page/offset)
    if chunks_meta:
        for i, meta in enumerate(chunks_meta):
            plain_chunk_text: str = meta["texto"]
            # Embedding sempre usa o texto; persistimos 'texto' apenas se PUB
            emb_vec = gerar_embedding(plain_chunk_text)
            embedding_bytes = pickle.dumps(emb_vec)

            # base_ref com hash curto (âncora estável)
            if origin is not None and "sha" in origin:
                if url:
                    base_ref = f"{url}@{origin['sha'][:8]}"
                elif file_is_upload:
                    # upload_file só existe neste branch; protege com nome_arquivo quando vazio
                    base_ref = f"{(upload_file.filename or nome_arquivo)}@{origin['sha'][:8]}"
                else:
                    base_ref = f"doc:{documento.id_documento}"
            else:
                base_ref = f"doc:{documento.id_documento}"

            if meta.get("page_number") is not None:
                fonte_valor = f"{base_ref}#p{meta['page_number']}-c{i}"
            else:
                fonte_valor = f"{base_ref}#c{i}"

            chunk_create = DocumentoChunkCreate(
                id_documento=str(documento.id_documento),
                chunk_index=i,
                texto=plain_chunk_text if cls == "PUB" else None,
                embedding=embedding_bytes,
                fonte=fonte_valor,
                page_number=meta.get("page_number"),
                char_start=meta["char_start"],
                char_end=meta["char_end"],
            )
            create_chunk(db, chunk_create)

    return {
        "msg": "Documento processado com sucesso",
        "id_documento": str(documento.id_documento),
        "caminho_rede": (
            str(documento.caminho_rede)
            if isinstance(documento.caminho_rede, str)
            else None
        ),
        "url": documento.url
    }

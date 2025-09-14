from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
import os
import uuid
import pickle
import io
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

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

def chunk_by_chars(text: str, max_chars: int = 1200, overlap: int = 200, base_start: int = 0) -> List[Dict]:
    """
    Divide 'text' em janelas de tamanho 'max_chars' com sobreposição 'overlap'.
    Retorna uma lista de dicts com 'texto', 'char_start', 'char_end'.
    Os offsets são ABSOLUTOS no documento, usando 'base_start' como deslocamento inicial.
    """
    chunks = []
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

def extract_pdf_chunks(file_bytes: bytes, max_chars: int = 1200, overlap: int = 200) -> List[Dict]:
    """
    Extrai texto página a página de um PDF e gera chunks com:
    - page_number (1-based)
    - char_start/char_end absolutos no documento
    """
    reader = PdfReader(io.BytesIO(file_bytes))
    all_chunks: List[Dict] = []
    global_offset = 0  # deslocamento cumulativo no documento (para offsets absolutos)

    for page_idx, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        # chunks dentro da página, com offsets absolutos
        page_chunks = chunk_by_chars(page_text, max_chars=max_chars, overlap=overlap, base_start=global_offset)
        for c in page_chunks:
            c["page_number"] = page_idx
        all_chunks.extend(page_chunks)

        # +1 para simular a quebra entre páginas (se você concatena com "\n" em outro lugar)
        global_offset += len(page_text) + 1

    return all_chunks

def extract_plaintext_chunks(text: str, max_chars: int = 1200, overlap: int = 200) -> List[Dict]:
    """
    Chunking para texto “flat” (TXT/HTML scraping). Sem page_number.
    Offsets são absolutos no documento.
    """
    chunks = chunk_by_chars(text, max_chars=max_chars, overlap=overlap, base_start=0)
    for c in chunks:
        c["page_number"] = None
    return chunks

# ---------------------------
# Endpoint
# ---------------------------

@router.post("/")
async def upload_documento(
    id_cliente: int = Form(...),
    nome_arquivo: str = Form(...),
    tipo: str = Form(...),
    classificacao_chave: str = Form(...),  # CONF, INT, PUB
    retencao_chave: str = Form(...),       # RET5Y, RET10Y, ETERNAL
    modulos: Optional[List[int]] = Form(None),
    url: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
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
    if modulos:
        for id_modulo in modulos:
            assoc = DocumentoModuloCreate(
                id_documento=str(documento.id_documento),
                id_modulo=id_modulo
            )
            create_doc_modulo(db, assoc)

    # 3) Extrair conteúdo e gerar chunks enriquecidos
    texto = ""
    chunks_meta: List[Dict] = []
    is_pdf = False
    file_bytes: Optional[bytes] = None

    # Upload de arquivo
    if file is not None and file.filename:
        file_bytes = await file.read()

        if file.filename.lower().endswith(".pdf"):
            is_pdf = True
            chunks_meta = extract_pdf_chunks(file_bytes, max_chars=1200, overlap=200)
            # texto completo (opcional – só será salvo se PUB)
            try:
                # Concatena páginas com quebra; mantém coerência com offsets (+1 a cada página)
                texto = "\n".join([c["texto"] for c in extract_pdf_chunks(file_bytes, max_chars=10**9, overlap=0)])
            except Exception:
                # fallback simples: extrai páginas e concatena sem recomputar offsets gigantes
                reader = PdfReader(io.BytesIO(file_bytes))
                texto = "\n".join([(p.extract_text() or "") for p in reader.pages])
        else:
            try:
                texto = file_bytes.decode("utf-8", errors="ignore")
            except Exception:
                texto = ""

            chunks_meta = extract_plaintext_chunks(texto, max_chars=1200, overlap=200)

        # Regras de retenção/armazenamento
        if classificacao_chave.upper() == "PUB":
            unique_name = f"{uuid.uuid4()}_{file.filename}"
            save_path = os.path.join(UPLOAD_DIR, unique_name)
            with open(save_path, "wb") as f:
                f.write(file_bytes)
            setattr(documento, "caminho_rede", save_path)
        elif retencao_chave.upper() == "ETERNAL":
            setattr(documento, "caminho_rede", nome_arquivo)

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

        if classificacao_chave.upper() == "PUB":
            unique_name = f"{uuid.uuid4()}_{nome_arquivo}"
            save_path = os.path.join(UPLOAD_DIR, unique_name)
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(resp.text)
            setattr(documento, "caminho_rede", save_path)
        elif retencao_chave.upper() == "ETERNAL":
            setattr(documento, "caminho_rede", nome_arquivo)

        db.commit()
        db.refresh(documento)

    # 4) Se for público, reter texto original
    if classificacao_chave.upper() == "PUB" and texto:
        setattr(documento, "texto_original", texto)
        db.commit()
        db.refresh(documento)

    # 5) Persistir chunks + embeddings com metadados (page/offset)
    if chunks_meta:
        for i, meta in enumerate(chunks_meta):
            plain_chunk_text = meta["texto"]
            # Embedding sempre usa o texto; persistimos 'texto' apenas se PUB
            emb_vec = gerar_embedding(plain_chunk_text)
            embedding_bytes = pickle.dumps(emb_vec)

            # fonte mais informativa
            if url:
                base_ref = url
            elif file:
                base_ref = nome_arquivo
            else:
                base_ref = f"doc:{documento.id_documento}"

            if meta.get("page_number") is not None:
                fonte_valor = f"{base_ref}#p{meta['page_number']}-c{i}"
            else:
                fonte_valor = f"{base_ref}#c{i}"

            chunk_create = DocumentoChunkCreate(
                id_documento=str(documento.id_documento),
                chunk_index=i,
                texto=plain_chunk_text if classificacao_chave.upper() == "PUB" else None,
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

from sqlalchemy.orm import Session
from app.models.doc_documento_chunk import DocumentoChunk
from app.schemas.doc_documento_chunk import DocumentoChunkCreate, DocumentoChunkUpdate

# Criar chunk
def create_chunk(db: Session, chunk: DocumentoChunkCreate):
    # Compatível com Pydantic v1 e v2:
    dump = getattr(chunk, "model_dump", chunk.dict)
    data = dump(exclude_none=True)
    db_chunk = DocumentoChunk(**data)
    db.add(db_chunk)
    db.commit()
    db.refresh(db_chunk)
    return db_chunk

# Listar chunks de um documento
def get_chunks_by_document(db: Session, id_documento: str):
    return db.query(DocumentoChunk).filter(
        DocumentoChunk.id_documento == id_documento
    ).order_by(DocumentoChunk.chunk_index).all()

# Obter chunk único
def get_chunk(db: Session, id_chunk: str):
    return db.query(DocumentoChunk).filter(
        DocumentoChunk.id_chunk == id_chunk
    ).first()

# Atualizar chunk
def update_chunk(db: Session, id_chunk: str, chunk_update: DocumentoChunkUpdate):
    db_chunk = get_chunk(db, id_chunk)
    if not db_chunk:
        return None

    for key, value in chunk_update.dict(exclude_unset=True).items():
        setattr(db_chunk, key, value)

    db.commit()
    db.refresh(db_chunk)
    return db_chunk

# Deletar chunk
def delete_chunk(db: Session, id_chunk: str):
    db_chunk = get_chunk(db, id_chunk)
    if not db_chunk:
        return None
    db.delete(db_chunk)
    db.commit()
    return db_chunk

def delete_chunks_by_document(db: Session, id_documento: str):
    db.query(DocumentoChunk).filter(
        DocumentoChunk.id_documento == id_documento
    ).delete(synchronize_session=False)
    db.commit()
import os

EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "LOCAL").upper()

# --------------------------
# OPENAI Backend
# --------------------------
if EMBEDDING_BACKEND == "OPENAI":
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    OPENAI_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# --------------------------
# LOCAL Backend (default)
# --------------------------
else:
    from sentence_transformers import SentenceTransformer
    LOCAL_MODEL_NAME = os.getenv("LOCAL_EMBEDDING_MODEL", "BAAI/bge-base-en-v1.5")
    model = SentenceTransformer(LOCAL_MODEL_NAME)


def gerar_embedding(texto: str):
    """
    Gera embedding de um texto usando o backend configurado (OPENAI ou LOCAL).
    """
    if EMBEDDING_BACKEND == "OPENAI":
        response = client.embeddings.create(
            model=OPENAI_MODEL,
            input=texto
        )
        return response.data[0].embedding
    else:
        return model.encode(texto).tolist()

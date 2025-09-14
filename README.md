# Sistema de Padronização e Automatização de Propostas — **Módulo de Upload & RAG**

Este README documenta **como o upload de documentos funciona**, **como os dados são armazenados** (modelo de dados e regras de confidencialidade / retenção) e descreve a **lógica de RAG para o chat** que consumirá esses dados.

> Stack: **FastAPI**, **SQLAlchemy**, **PostgreSQL** (recomendado), **PyPDF2**, **BeautifulSoup**.  
> Segurança: classificação (**CONF**, **INT**, **PUB**) e retenção (**RET5Y**, **RET10Y**, **ETERNAL**). Multi-tenant por `id_cliente`.

---

## 1) Fluxo de Upload (`POST /upload/`)

### 1.1 Parâmetros (FormData)
- `id_cliente: int` — tenant do documento (obrigatório)
- `nome_arquivo: str` — nome lógico do documento
- `tipo: str` — ex.: `pdf`, `txt`, `url`
- `classificacao_chave: str` — `CONF`, `INT`, `PUB`
- `retencao_chave: str` — `RET5Y`, `RET10Y`, `ETERNAL`
- `modulos: List[int]` (opcional) — IDs de módulos para vincular
- `url: str` (opcional) — quando o tipo for URL/scraping
- `file: UploadFile` (opcional) — quando for upload de arquivo

### 1.2 Pipeline resumido
1. **Cria o registro do documento** (`doc_documento`) com estado inicial (sem chunks).
2. **Associa módulos** (N:N via `doc_documento_modulo`).
3. **Extrai conteúdo**:
   - **PDF**: leitura por **página**, cálculo de `page_number`, offsets de caracteres **absolutos** (`char_start`, `char_end`).
   - **TXT/HTML (URL)**: extração de texto; offsets por janela de caracteres.
4. **Armazenamento do arquivo bruto** (condicional):
   - Se `classificacao_chave == "PUB"`: salva o arquivo/HTML em `data/uploads/` e guarda `caminho_rede`.
   - Se `retencao_chave == "ETERNAL"`: guarda apenas um caminho lógico (`caminho_rede = nome_arquivo`).
   - **CONF/INT**: **não** salva arquivo bruto por padrão (ajustável por política).
5. **Texto original**:
   - Persistido em `doc_documento.texto_original` **apenas** se `PUB`.
6. **Chunking + Embeddings**:
   - Janela por **caracteres** (default: `max_chars=1200`, `overlap=200`), preservando offsets e `page_number` (para PDF).
   - Para cada chunk: gera `embedding` (vetor), persiste em `doc_documento_chunk` com metadados:
     - `chunk_index`, `page_number`, `char_start`, `char_end`, `fonte` (`arquivo.pdf#p3-c12` ou `url#c8`).
     - `texto` do chunk **apenas** se `PUB`; caso contrário `NULL` (privacidade).

### 1.3 Regras de confidencialidade e retenção
- **CONF/INT**: não persistir `texto` nem arquivo bruto (somente embeddings + ponteiros).  
- **PUB**: persistir `texto_original`, `texto` dos chunks e arquivo/HTML em disco.
- **RET5Y/RET10Y/ETERNAL**: regem política de descarte/arquivamento. `ETERNAL` mantém referência lógica (`caminho_rede`) mesmo sem salvar arquivo.

---

## 2) Modelo de Dados (resumo)

### 2.1 `doc_documento` (Documento)
| Campo | Tipo | Notas |
|---|---|---|
| `id_documento` | UUID (String(36)) | PK |
| `id_cliente` | Integer (FK) | **Tenant**; `ondelete=CASCADE` |
| `nome_arquivo` | String | |
| `tipo` | String | `pdf`, `txt`, `url`… |
| `caminho_rede` | String \| NULL | usado p/ PUB/ETERNAL |
| `url` | String \| NULL | quando veio de web |
| `checksum` | String \| NULL | opcional |
| `texto_original` | Text \| NULL | **somente PUB** |
| `classificacao_chave` | String | `CONF`, `INT`, `PUB` |
| `retencao_chave` | String | `RET5Y`, `RET10Y`, `ETERNAL` |
| `created_at`/`updated_at` | TIMESTAMP | auditoria |

**Relacionamentos**  
- `documento.modulos` ↔ `doc_documento_modulo.documento` (1:N objeto de associação)  
- `documento.chunks` ↔ `doc_documento_chunk.documento` (1:N)  
- Recomenda-se `passive_deletes=True` + FK com `ondelete="CASCADE"`

### 2.2 `doc_documento_chunk` (Chunk)
| Campo | Tipo | Notas |
|---|---|---|
| `id_chunk` | UUID (String(36)) | PK |
| `id_documento` | FK → `doc_documento` | `ondelete=CASCADE` |
| `chunk_index` | Integer | `Unique(id_documento, chunk_index)` |
| `texto` | Text \| NULL | **apenas PUB** |
| `embedding` | **LargeBinary** | vetor (pickle/bytes) |
| `fonte` | String | ex.: `arquivo.pdf#p2-c7` |
| `page_number` | Integer \| NULL | PDF |
| `char_start` / `char_end` | Integer | offsets absolutos |
| `created_at`/`updated_at` | TIMESTAMP | auditoria |

> **Recomendação de evolução**: migrar `embedding` para **pgvector** (`VECTOR(1536)` ou dimensão do modelo) e indexar (HNSW/IVFFlat).

### 2.3 `doc_documento_modulo` (Associação N:N)
| Campo | Tipo | Notas |
|---|---|---|
| `id_documento` | FK | PK composto |
| `id_modulo` | FK | PK composto |
| Auditoria | TIMESTAMP/usuarios |  |

> **Importante**: evitar `back_populates` conflitantes (já corrigido).

---

## 3) Chunking & Embeddings (detalhes)

- **PDF**: extração por página → chunking por caracteres com sobreposição; cada chunk grava `page_number` e offsets **globais** (somando o tamanho das páginas anteriores + 1 por quebra).  
- **TXT/HTML**: chunking por caracteres com sobreposição; `page_number = NULL`.
- **Fonte**: cria referência humana e estável:  
  - De URL: `https://site.com/doc#c12` ou `#p3-c2`  
  - De arquivo: `Contrato.pdf#p5-c1`  
- **Privacidade**: embeddings são persistidos para todos os níveis; **texto do chunk** só para `PUB`.

Parâmetros padrão:
```py
max_chars = 1200
overlap   = 200
```

---

## 4) Lógica de **RAG** para o Chat

A seguir um blueprint para implementar o chat com **retrieval-augmented generation** sobre os dados indexados.

### 4.1 Requisitos de segurança/multi-tenant
- **Filtro obrigatório por `id_cliente`** em todas as consultas de chunks/documentos.
- **Gating por classificação**:  
  - Usuário só pode **ver** textos `PUB`.  
  - Para `CONF/INT`: usar embeddings **sem** exibir texto/citações literais (ver “Política de resposta” abaixo).  
- **ABAC/RBAC**: role do usuário pode afrouxar/rigidificar acesso (ex.: *Analista do Cliente* pode ver `INT` do próprio cliente).
- **Auditoria**: logar consultas (usuário, cliente, docs atingidos, tempo, hashes de consultas).

### 4.2 Arquitetura (consulta)
1. **Receber pergunta** do usuário (`query`) + contexto (histórico do chat) + escopo (cliente, módulos, data-range).
2. **Gerar embedding da query**.
3. **Buscar candidatos** (top-k=8..15):  
   - **Com pgvector** (recomendado): `ORDER BY embedding <-> :query LIMIT k`.  
   - Filtros: `id_cliente = :cliente`, `classificacao_chave IN (:permitidas)`, `modulos` (opcional), etc.
4. **Re-rank opcional**: por `BM25`/semântica (se usar vetor + texto PUB).  
5. **Construir contexto**: concatenar trechos (ou **resumos** de trechos CONF/INT) até um limite de tokens.
6. **Gerar resposta** com **prompt estruturado**, incorporando **regras de privacidade**.
7. **Citações**: apresentar `fonte` (arquivo e página) quando **PUB**; para `CONF/INT`, apenas **referências não verbatim** (“Fonte: Documento confidencial #123, p.5”).

### 4.3 Exemplo — consulta com **pgvector** (SQLAlchemy)
```py
# Modelo (exemplo) — requer extensão pgvector instalada:
# CREATE EXTENSION IF NOT EXISTS vector;
from sqlalchemy.dialects.postgresql import VECTOR
from sqlalchemy import Column, Integer, String, ForeignKey

class DocumentoChunkVector(Base):
    __tablename__ = "doc_documento_chunk"
    id_chunk = Column(String(36), primary_key=True)
    id_documento = Column(String(36), ForeignKey("doc_documento.id_documento", ondelete="CASCADE"))
    chunk_index = Column(Integer, nullable=False)
    texto = Column(Text)              # NULL em CONF/INT
    embedding = Column(VECTOR(1536))  # <— troque LargeBinary por VECTOR
    fonte = Column(String(255))
    page_number = Column(Integer)
    char_start = Column(Integer)
    char_end = Column(Integer)

# Consulta vetorial (k = 8)
qvec = embed(query)  # vetor Python (lista/ndarray) a partir do seu gerador de embedding
stmt = (
    db.query(DocumentoChunkVector)
      .join(Documento, Documento.id_documento == DocumentoChunkVector.id_documento)
      .filter(Documento.id_cliente == id_cliente_req)
      .filter(Documento.classificacao_chave.in_(classificacoes_permitidas))
      .order_by(DocumentoChunkVector.embedding.l2_distance(qvec))  # ou .cosine_distance()
      .limit(8)
)
candidatos = stmt.all()
```

> **Sem pgvector** (estado atual com `LargeBinary/pickle`): o retrieval exige carregar embeddings e calcular similaridade na aplicação (FAISS/NumPy). Para produção, **migre para pgvector** ou mantenha um índice FAISS **por cliente** em memória/disco.

### 4.4 Template de **prompt** (seguro)
```text
Você é um assistente que responde com base em evidências.

Regras de confidencialidade:
- Nunca revele texto literal proveniente de documentos marcados como CONF ou INT.
- Para CONF/INT, use os embeddings como sinal semântico e responda de forma geral,
  sem copiar trechos. Pode referenciar a origem sem detalhes sensíveis.
- Para PUB, você pode citar pequenos trechos (<= 2 linhas) e deve incluir a fonte.

Contexto recuperado:
{contexto}

Pergunta do usuário:
{pergunta}

Responda em português, concisa e tecnicamente.
Inclua "Fontes:" com lista de fontes quando PUB; para CONF/INT, cite apenas identificadores.
```

### 4.5 Montagem do **contexto** (pseudo-código)
```py
tokens = 0
blocos = []
for c in candidatos:
    if documento.classificacao_chave in ("CONF", "INT"):
        resumo = resumir_sem_texto(c.embedding, meta=c.fonte)  # ex.: "Contrato de Suporte (p.5): requisitos de SLA"
        add = resumo
    else:  # PUB
        add = c.texto  # pode truncar/limpar
    if tokens + len(tok(add)) > LIMITE: break
    blocos.append(f"[{c.fonte}] {add}")
    tokens += len(tok(add))

contexto = "\n\n".join(blocos)
```

### 4.6 Política de resposta
- **PUB**: resposta pode conter citações curtas com `fonte` (arquivo + página).  
- **CONF/INT**: **sem** citações literais; apenas resposta agregada + referência genérica.  
- **Sem resultados**: explique limitação e sugira ampliar escopo/módulos/termos.  

---

## 5) Boas práticas e Operação

- **Índices**: `UNIQUE (id_documento, chunk_index)`, `INDEX (id_documento, page_number)`.  
- **FKs** com `ondelete="CASCADE"` e `passive_deletes=True` nas relações ORM.  
- **Naming convention** no `MetaData` para facilitar Alembic.  
- **Validações**: tamanho de arquivo, tipos MIME, timeout de scraping, sanitização de HTML.  
- **Logs/Auditoria**: capture usuário, cliente, origem do documento e IDs de chunks consultados.  
- **Segurança**: isole por `id_cliente`; nunca misture contextos de clientes diferentes em uma mesma resposta.  
- **Migração para vetorial nativa**: `pgvector` + índice HNSW/IVFFlat para escala; ou FAISS por cliente.

---

## 6) Exemplo de chamada (cURL)
```bash
curl -X POST http://127.0.0.1:8000/upload/ ^
  -F "id_cliente=10" ^
  -F "nome_arquivo=Contrato_Suporte.pdf" ^
  -F "tipo=pdf" ^
  -F "classificacao_chave=CONF" ^
  -F "retencao_chave=RET5Y" ^
  -F "modulos=3" -F "modulos=7" ^
  -F "file=@C:\tmp\Contrato_Suporte.pdf"
```

---

## 7) Roadmap curto (RAG)
- [ ] Migrar `embedding` para **pgvector** ou adotar **FAISS por cliente**.
- [ ] Implementar **filtros de módulo** no retrieval (JOIN em `doc_documento_modulo`).
- [ ] Re-rank híbrido (BM25 + vetor) quando `texto` PUB existir.
- [ ] Citador de página (`fonte`) com link direto para visualizador.
- [ ] Guardrails de confidencialidade no prompt e no pós-processamento.
- [ ] Cache de resultados vetoriais por janela de chat (reduz latência/custo).
- [ ] Job assíncrono para (re)indexação pesada e OCR quando necessário.

---

**Anexos úteis**  
- Politicas de armazenamento e segurança devem alinhar-se a ISO 27001.  
- Documentos confidenciais: **evitar** persistência de texto/arquivo; trabalhar via embeddings e metadados.

> Em caso de dúvidas, abra uma issue descrevendo: `id_cliente`, `classificacao`, exemplo de pergunta e `fonte` dos chunks retornados.

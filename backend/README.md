# Proposal Manager Backend

Backend em **FastAPI + SQLAlchemy**, preparado para rodar em **SQLite (desenvolvimento)** e **PostgreSQL (produção)**.

---

## 🚀 Passos para rodar o projeto

### 1. Clonar o repositório
```bash
git clone <seu-repo>
cd backend
```

### 2. Criar e ativar ambiente virtual
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependências
```bash
cd .\backend\
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
O arquivo `.env` já está configurado para usar **SQLite**:
```
DATABASE_URL=sqlite:///./app.db
```

Se quiser usar PostgreSQL:
```
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nomedb
```

### 5. Rodar a aplicação
```bash
uvicorn app.main:app --reload
```

### 6. Acessar Swagger UI
Abra no navegador:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

Ou em Redoc:
👉 [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📂 Estrutura principal
```
app/
├── core/        # Configurações
├── models/      # Modelos ORM (SQLAlchemy)
├── schemas/     # Schemas Pydantic
├── crud/        # Operações no banco
├── routes/      # Rotas FastAPI
├── security/    # Segurança (hash, auth)
└── tests/       # Testes
```


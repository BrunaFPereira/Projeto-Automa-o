from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String

# Importa a Base, engine e SessionLocal do seu arquivo database.py
from src.database import Base, engine, SessionLocal

# 1. Modelo de Dados (Tabela 'itens' no PostgreSQL)
class ItemModel(Base):
    __tablename__ = "itens"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)

# Cria as tabelas no banco automaticamente ao iniciar a API
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Gerenciador de Sessão do Banco de Dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ROTAS DA API ---

@app.get("/")
def home():
    return {"message": "API rodando com sucesso!"}

@app.get("/status")
def status():
    return {"status": "ok", "versao": "1.0.0"}

# Rota para cadastrar item no PostgreSQL
@app.post("/itens/")
def criar_item(nome: str, descricao: str = None, db: Session = Depends(get_db)):
    novo_item = ItemModel(nome=nome, descricao=descricao)
    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)
    return novo_item

# Rota para listar todos os itens salvos no PostgreSQL
@app.get("/itens/")
def listar_itens(db: Session = Depends(get_db)):
    return db.query(ItemModel).all()
"""
Configuração e inicialização do banco de dados.
Inclua aqui a engine, sessão e utilitários de criação de tabelas.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL
import os

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_tables():
    """Cria todas as tabelas do banco de dados."""
    import app.models.database 
    Base.metadata.create_all(bind=engine)

"""
Função utilitária para obter uma sessão de banco de dados para uso com FastAPI (sync/async).
"""
from app.db.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

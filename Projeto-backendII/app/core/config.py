"""
Configurações globais do projeto (exemplo).
Coloque aqui variáveis de ambiente, configurações de banco, chaves, etc.
"""
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

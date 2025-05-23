"""
Este módulo demonstra como criar um endpoint FastAPI que aceita entrada do usuário,
a sanitiza e retorna uma resposta segura.
"""

from fastapi import FastAPI, Query, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import re
import html
import logging
import uuid

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='fastapi_security.log'
)
logger = logging.getLogger('security')


app = FastAPI(
    title="Secure API Example",
    description="A FastAPI application with security best practices",
    version="1.0.0"
)


SECRET_KEY = "aeb165ace8b94a3c9c1a2bc6fc41dc5a2eff3de2e90e443df9c70f69cd9c67cf"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username must be alphanumeric, with underscores or hyphens only')
        return v

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[^A-Za-z0-9]', v):
            raise ValueError('Password must contain at least one special character')
        return v

class User(UserBase):
    id: str
    disabled: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class Message(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    
    @validator('content')
    def sanitize_content(cls, v):
        sanitized = html.escape(v)
        return sanitized

class SearchQuery(BaseModel):
    query: str = Field(..., min_length=1, max_length=100)
    category: Optional[str] = None
    
    @validator('query')
    def sanitize_query(cls, v):
        sanitized = html.escape(v)
        sanitized = re.sub(r'[;\'"]', '', sanitized)
        return sanitized
    
    @validator('category')
    def validate_category(cls, v):
        if v is not None:
            allowed_categories = ['products', 'services', 'blog', 'news']
            if v not in allowed_categories:
                raise ValueError(f"Category must be one of: {', '.join(allowed_categories)}")
        return v

fake_users_db = {
    "johndoe": {
        "id": "user-1",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "full_name": "John Doe",
        "hashed_password": pwd_context.hash("Pass@word1"),
        "disabled": False,
    }
}


def verify_password(plain_password, hashed_password):
    """Verifica se uma senha em texto simples corresponde ao hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Gera um hash seguro de uma senha."""
    return pwd_context.hash(password)

def get_user(username: str):
    """Recupera um usuário do banco de dados pela username."""
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return User(**user_dict)
    return None

def authenticate_user(username: str, password: str):
    """Autentica um usuário verificando username e senha."""
    user = get_user(username)
    if not user:
        return False
    user_dict = fake_users_db[username]
    if not verify_password(password, user_dict["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um token JWT com os dados fornecidos e expiração."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Obtém o usuário atual com base no token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    """Verifica se o usuário atual está ativo."""
    user_dict = fake_users_db.get(current_user.username)
    if user_dict and user_dict.get("disabled"):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint para autenticação e obtenção de token JWT."""
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    logger.info(f"Successful login: {user.username}")
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Endpoint seguro que retorna informações do usuário atual."""
    return current_user

@app.post("/messages/send")
async def send_message(
    message: Message,
    current_user: User = Depends(get_current_active_user)
):
    """
    Endpoint que aceita uma mensagem, sanitiza o conteúdo e retorna uma resposta segura.
    A mensagem já é sanitizada pelo modelo Pydantic.
    """
    message_id = str(uuid.uuid4())
    
    logger.info(f"Message sent by user: {current_user.username}, ID: {message_id}")
    
    return {
        "id": message_id,
        "status": "sent",
        "sender": current_user.username,
        "content_length": len(message.content),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/search")
async def search(
    query: str = Query(..., min_length=1, max_length=100),
    category: Optional[str] = Query(None, max_length=20),
    current_user: User = Depends(get_current_active_user)
):
    """
    Endpoint de pesquisa que aceita e sanitiza parâmetros de consulta.
    
    Este endpoint demonstra:
    1. Validação de parâmetros de consulta
    2. Sanitização de entrada
    3. Autenticação do usuário
    4. Logging seguro
    """
    search_data = SearchQuery(query=query, category=category)
    
    query_preview = search_data.query[:10] + "..." if len(search_data.query) > 10 else search_data.query
    logger.info(f"Search by {current_user.username}: {query_preview}")
    
    results = [
        {"id": "1", "title": "Result 1", "description": f"Sample result for {search_data.query}"},
        {"id": "2", "title": "Result 2", "description": "Another sample result"}
    ]
    
    if search_data.category:
        results = [r for r in results if r["id"] == "1"]   
    
    return {
        "query": search_data.query,
        "category": search_data.category,
        "count": len(results),
        "results": results
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


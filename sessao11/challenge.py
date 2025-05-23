"""
Este desafio implementa uma API GraphQL avançada com suporte
a consultas aninhadas e mutações autenticadas usando Strawberry.

Execução:
1. Instale as dependências: pip install strawberry-graphql fastapi uvicorn python-jose[cryptography] pydantic
2. Execute: uvicorn challenge:app --reload
3. Acesse: http://localhost:8000/graphql

Recursos:
- Autenticação via JWT
- Consultas aninhadas (usuários têm postagens)
- Proteção de mutações
"""

import strawberry
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from strawberry.asgi import GraphQL
from strawberry.types import Info
from typing import List, Optional, Dict, Any, Annotated, Union, Union
from datetime import datetime, timedelta
import uuid
from jose import JWTError, jwt
from pydantic import BaseModel


SECRET_KEY = "super_secret_key_change_in_production_environment"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserInDB(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    disabled: bool = False
    hashed_password: str

users_db = {
    "user1": {
        "id": 1,
        "username": "user1",
        "email": "user1@example.com",
        "full_name": "User One",
        "disabled": False,
        "hashed_password": "fakehashedsecret1"
    },
    "user2": {
        "id": 2,
        "username": "user2",
        "email": "user2@example.com",
        "full_name": "User Two",
        "disabled": True,
        "hashed_password": "fakehashedsecret2"
    }
}

posts_db = {
    1: {
        "id": 1,
        "title": "First Post",
        "content": "This is the first post content",
        "author_id": 1,
        "created_at": "2023-05-20T12:00:00"
    },
    2: {
        "id": 2,
        "title": "Second Post",
        "content": "This is the second post content",
        "author_id": 1,
        "created_at": "2023-05-21T14:30:00"
    },
    3: {
        "id": 3,
        "title": "User Two's Post",
        "content": "This is a post by User Two",
        "author_id": 2,
        "created_at": "2023-05-22T10:15:00"
    }
}

def verify_password(plain_password, hashed_password):
    """Demo: senha é igual ao hash (NÃO FAÇA ISSO EM PRODUÇÃO)"""
    return plain_password == hashed_password.replace("fakehashed", "")

def get_user(username: str):
    if username in users_db:
        user_dict = users_db[username]
        return UserInDB(**user_dict)
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
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
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


@strawberry.type
class AuthenticationError:
    message: str


@strawberry.type
class Post:
    id: int
    title: str
    content: str
    author_id: int
    created_at: str
    
    @strawberry.field
    def author(self) -> "User":
        """Resolver para buscar o autor do post - demonstra consultas aninhadas"""
        for user_data in users_db.values():
            if user_data["id"] == self.author_id:
                return User(
                    id=user_data["id"],
                    username=user_data["username"],
                    email=user_data["email"],
                    full_name=user_data["full_name"]
                )
        return None

@strawberry.type
class User:
    id: int
    username: str
    email: str
    full_name: str
    
    @strawberry.field
    def posts(self) -> List[Post]:
        """Resolver para buscar os posts do usuário - demonstra consultas aninhadas"""
        return [
            Post(
                id=post["id"],
                title=post["title"],
                content=post["content"],
                author_id=post["author_id"],
                created_at=post["created_at"]
            )
            for post in posts_db.values()
            if post["author_id"] == self.id
        ]

class GraphQLContext:
    def __init__(self, request=None):
        self.request = request
        self.user = None

def requires_auth(resolver):
    async def wrapper(root, info: Info, **kwargs):
        context = info.context
        if not context.user:
            return AuthenticationError(message="Authentication required")
        return await resolver(root, info, **kwargs)
    return wrapper

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        """Consulta um usuário pelo ID"""
        for user_data in users_db.values():
            if user_data["id"] == id:
                return User(
                    id=user_data["id"],
                    username=user_data["username"],
                    email=user_data["email"],
                    full_name=user_data["full_name"]
                )
        return None
    
    @strawberry.field
    def users(self) -> List[User]:
        """Lista todos os usuários"""
        return [
            User(
                id=user_data["id"],
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"]
            )
            for user_data in users_db.values()
        ]
    
    @strawberry.field
    def posts(self) -> List[Post]:
        """Lista todos os posts"""
        return [
            Post(
                id=post["id"],
                title=post["title"],
                content=post["content"],
                author_id=post["author_id"],
                created_at=post["created_at"]
            )
            for post in posts_db.values()
        ]
    
    @strawberry.field
    def post(self, id: int) -> Optional[Post]:
        """Consulta um post pelo ID"""
        post_data = posts_db.get(id)
        if post_data:
            return Post(
                id=post_data["id"],
                title=post_data["title"],
                content=post_data["content"],
                author_id=post_data["author_id"],
                created_at=post_data["created_at"]
            )
        return None
    
    @strawberry.field
    async def me(self, info: Info) -> Union[User, AuthenticationError]:
        """Consulta o usuário autenticado atual"""
        context = info.context
        if not context.user:
            return AuthenticationError(message="Not authenticated")
            
        user_data = users_db.get(context.user.username)
        return User(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data["email"],
            full_name=user_data["full_name"]
        )

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_post(
        self, info: Info, title: str, content: str
    ) -> Union[Post, AuthenticationError]:
        """Cria um novo post (requer autenticação)"""
        context = info.context
        if not context.user:
            return AuthenticationError(message="Authentication required to create posts")
        
        new_id = max(posts_db.keys()) + 1 if posts_db else 1
        
        new_post = {
            "id": new_id,
            "title": title,
            "content": content,
            "author_id": context.user.id,
            "created_at": datetime.utcnow().isoformat()
        }
        
        posts_db[new_id] = new_post
        
        return Post(
            id=new_post["id"],
            title=new_post["title"],
            content=new_post["content"],
            author_id=new_post["author_id"],
            created_at=new_post["created_at"]
        )
    
    @strawberry.mutation
    async def update_post(
        self, info: Info, id: int, title: Optional[str] = None, content: Optional[str] = None
    ) -> Union[Post, AuthenticationError]:
        """Atualiza um post existente (requer autenticação e ser autor)"""
        context = info.context
        if not context.user:
            return AuthenticationError(message="Authentication required to update posts")
        
        if id not in posts_db:
            return AuthenticationError(message="Post not found")
        
        if posts_db[id]["author_id"] != context.user.id:
            return AuthenticationError(message="You can only update your own posts")
        
        if title is not None:
            posts_db[id]["title"] = title
        if content is not None:
            posts_db[id]["content"] = content
        
        return Post(
            id=posts_db[id]["id"],
            title=posts_db[id]["title"],
            content=posts_db[id]["content"],
            author_id=posts_db[id]["author_id"],
            created_at=posts_db[id]["created_at"]
        )
    
    @strawberry.mutation
    async def delete_post(
        self, info: Info, id: int
    ) -> Union[bool, AuthenticationError]:
        """Deleta um post (requer autenticação e ser autor)"""
        context = info.context
        if not context.user:
            return AuthenticationError(message="Authentication required to delete posts")

        if id not in posts_db:
            return AuthenticationError(message="Post not found")
        

        if posts_db[id]["author_id"] != context.user.id:
            return AuthenticationError(message="You can only delete your own posts")
        

        del posts_db[id]
        return True


schema = strawberry.Schema(query=Query, mutation=Mutation)


app = FastAPI(title="Advanced GraphQL API with Authentication")


@app.post("/token", response_model=Token)
async def login_for_access_token(username: str, password: str):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

async def get_context(request=None):
    context = GraphQLContext(request=request)
    
    if request:
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            token = authorization.replace("Bearer ", "")
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username = payload.get("sub")
                context.user = get_user(username)
            except JWTError:
                pass
    
    return context

graphql_app = GraphQL(
    schema,
    context_getter=get_context,
    debug=True
)

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

@app.get("/")
def read_root():
    return {
        "message": "GraphQL API Challenge - Session 11", 
        "docs": "Acesse /graphql para usar a interface GraphQL",
        "login": "Use o endpoint /token para obter um token JWT"
    }


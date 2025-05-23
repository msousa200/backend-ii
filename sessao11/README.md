# Session 11: Building GraphQL APIs with Python

Este diretório contém implementações de APIs GraphQL usando Strawberry e FastAPI.

## Pré-requisitos

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Exercício: GraphQL API Simples

Uma API GraphQL simples que permite consultar e atualizar usuários.

### Executar

```bash
uvicorn exercise:app --reload
```

Acesse: http://localhost:8000/graphql

### Funcionalidades
- Consultar usuário por ID
- Listar todos os usuários
- Atualizar nome de um usuário

### Exemplo de consultas

```graphql
# Consultar um usuário:
query {
  user(id: 1) {
    id
    name
  }
}

# Listar todos os usuários:
query {
  users {
    id
    name
  }
}

# Atualizar um usuário:
mutation {
  updateUserName(id: 1, name: "John Updated") {
    id
    name
  }
}
```

## Desafio: GraphQL API Avançada com Autenticação

Uma API GraphQL avançada com consultas aninhadas e autenticação.

### Executar

```bash
uvicorn challenge:app --reload
```

Acesse: http://localhost:8000/graphql

### Funcionalidades
- Autenticação via JWT (JSON Web Tokens)
- Consultas aninhadas (usuários têm posts, posts têm autores)
- Mutações protegidas por autenticação
- Validação de propriedade (apenas autores podem editar seus posts)

### Exemplo de uso

1. Obter token de autenticação:

```bash
curl -X POST "http://localhost:8000/token" -d "username=user1&password=secret1"
```

2. Usar o token nas consultas GraphQL (no cabeçalho):

```
Authorization: Bearer seu_token_aqui
```

3. Exemplo de consultas:

```graphql
# Consultar usuários e seus posts:
query {
  users {
    id
    username
    fullName
    posts {
      id
      title
      content
    }
  }
}

# Criar um post (requer autenticação):
mutation {
  createPost(title: "Novo Post", content: "Conteúdo do novo post") {
    ... on Post {
      id
      title
      content
    }
    ... on AuthenticationError {
      message
    }
  }
}
```

## Recursos Adicionais

- [Documentação do GraphQL](https://graphql.org/learn/)
- [Documentação do Strawberry](https://strawberry.rocks/docs/)
- [Documentação do FastAPI](https://fastapi.tiangolo.com/)

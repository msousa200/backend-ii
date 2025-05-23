# Exercício de Segurança com FastAPI

Este exercício demonstra como implementar segurança em uma API REST usando FastAPI, incluindo:
- Validação e sanitização de entrada
- Autenticação com JWT
- Proteção de endpoints
- Logging seguro

## Requisitos

Instale as dependências necessárias:

```bash
pip install -r requirements-fastapi.txt
```

## Executando a aplicação

Para iniciar o servidor:

```bash
python exercise.py
```

Ou diretamente com uvicorn:

```bash
uvicorn exercise:app --reload
```

## Testando os endpoints

Acesse a documentação interativa da API em: http://127.0.0.1:8000/docs

### Autenticação

1. Clique no botão "Authorize" e use as credenciais:
   - Username: johndoe
   - Password: Pass@word1

2. Teste os endpoints protegidos:
   - GET `/users/me` - Retorna informações do usuário atual
   - POST `/messages/send` - Envia uma mensagem sanitizada
   - GET `/search` - Executa uma pesquisa sanitizada

## Conceitos de segurança demonstrados

1. **Validação de entrada**: Validação rigorosa de todos os dados de entrada usando Pydantic
2. **Sanitização de dados**: Limpeza de HTML e outras entradas potencialmente perigosas
3. **Autenticação segura**: JWT com expiração, senhas com hash bcrypt
4. **Registro seguro**: Logging sem expor dados sensíveis
5. **Tratamento de erros seguro**: Mensagens de erro que não expõem detalhes internos

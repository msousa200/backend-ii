# Text Processing AI Agents API

Uma solução robusta de backend em FastAPI que integra capacidades avançadas de agentes de IA através do framework CrewAI. A aplicação permite processar textos de maneira eficiente, delegando responsabilidades aos agentes de IA para tarefas como tradução, sumarização e detecção de idioma.


## Características Principais

- **Integração com Agentes IA**: Utiliza o framework CrewAI para gerenciar agentes de IA para tarefas de processamento de texto
- **Múltiplos Tipos de Processamento**: 
  - **Sumarização**: Cria resumos concisos e precisos de textos longos
  - **Tradução**: Traduz textos entre Inglês e Português com detecção automática de idioma
  - **Detecção de Idioma**: Identifica se o texto está em Inglês ou Português
- **Processamento Assíncrono**: Tarefas executadas em background para melhor performance e experiência do usuário
- **Integração com Banco de Dados**: ORM SQLAlchemy com suporte para SQLite e PostgreSQL
- **Documentação da API**: Documentação OpenAPI gerada automaticamente via FastAPI
- **Suporte a Docker**: Implantação em contêineres com Docker e Docker Compose
- **Métricas e Monitoramento**: Métricas Prometheus para monitoramento de performance
- **Logging Abrangente**: Registro detalhado para depuração e auditoria
- **Testes Automatizados**: Testes unitários e de integração para validar o funcionamento dos componentes
- **CI/CD com GitHub Actions**: Pipeline automatizado para testes e deployment


## Arquitetura

A aplicação segue uma arquitetura modular com clara separação de responsabilidades:

- **Camada de API**: Rotas e endpoints FastAPI para lidar com requisições HTTP
- **Camada de Serviço**: Integração com CrewAI para gerenciamento de agentes de IA e processamento de texto
- **Camada de Dados**: Modelos SQLAlchemy e conexões com o banco de dados
- **Camada de Modelo**: Modelos Pydantic para validação de requisições/respostas

## Instalação

### Pré-requisitos

- Python 3.10+
- Docker e Docker Compose (para deployment em contêiner)
- (Opcional) PostgreSQL instalado localmente, caso queira usar fora do Docker

### Dependências de Banco de Dados

O backend suporta tanto SQLite (padrão para desenvolvimento/local) quanto PostgreSQL (recomendado para produção). O driver `psycopg2-binary` já está incluído nas dependências.

- Para SQLite, basta definir a variável de ambiente:
  ```env
  DATABASE_URL=sqlite:///./app.db
  ```
- Para PostgreSQL, defina:
  ```env
  DATABASE_URL=postgresql+psycopg2://usuario:senha@host:porta/nome_do_banco
  ```
  Exemplo para Docker Compose:
  ```env
  DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/postgres
  ```

A engine SQLAlchemy detecta automaticamente o tipo de banco e ajusta a configuração.

### Desenvolvimento Local

1. Clone o repositório:
```bash
git clone https://github.com/yourusername/Projeto-backendII.git
cd Projeto-backendII
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

5. Configure o banco de dados para usar SQLite:
```bash
export DATABASE_URL="sqlite:///./app.db"
```

6. Execute a aplicação:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

> **Nota**: Se a porta 8000 já estiver em uso, escolha outra porta disponível.

### Implantação com Docker

1. Construa e inicie os contêineres:
```bash
docker-compose up -d
```

2. A API estará disponível em http://localhost:8000

## Documentação da API

Quando a aplicação estiver em execução, acesse a documentação OpenAPI gerada automaticamente:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints da API

| Endpoint | Método | Descrição |
|----------|--------|-------------|
| `/` | GET | Endpoint raiz para verificar se a API está em execução |
| `/api/process-text` | POST | Processa texto usando agentes de IA (sumarização ou tradução) |
| `/api/detect-language` | POST | Detecta o idioma do texto fornecido |
| `/api/tasks/{task_id}` | GET | Obtém o status e o resultado de uma tarefa de processamento de texto |
| `/api/tasks` | GET | Lista todas as tarefas de processamento de texto |
| `/health` | GET | Endpoint de verificação de saúde para monitoramento |
| `/metrics` | GET | Endpoint de métricas do Prometheus |

### Exemplos de Requisições

> **IMPORTANTE**: O processamento de texto é realizado de forma assíncrona. Todas as requisições para `/api/process-text` retornam imediatamente com um ID de tarefa, mas o resultado só estará disponível após o processamento ser concluído. Você precisa fazer uma segunda requisição para `/api/tasks/{task_id}` para obter o resultado final.

#### Sumarizar Texto

1. Inicie o processamento:
```bash
curl -X POST "http://localhost:8000/api/process-text" \
     -H "Content-Type: application/json" \
     -d '{
        "text": "Este é um texto de exemplo que será processado pelo agente de IA para ser resumido em algumas sentenças concisas que capturam a essência do conteúdo original. O texto pode ser longo, mas o resumo será breve e informativo, destacando apenas os pontos mais importantes.",
        "processing_type": "summarization"
     }'
```

2. A resposta incluirá um ID de tarefa:
```json
{
  "id": 15,
  "status": "pending",
  "processing_type": "summarization",
  "created_at": "2025-05-22T20:06:05.283625Z",
  "updated_at": "2025-05-22T20:06:05.283625Z"
}
```

3. Use o ID da tarefa para verificar o resultado (substitua 15 pelo ID recebido):
```bash
curl -X GET "http://localhost:8000/api/tasks/15" -H "accept: application/json"
```

4. Quando o processamento estiver concluído, você receberá o texto resumido:
```json
{
  "id": 15,
  "original_text": "Este é um texto de exemplo...",
  "processed_text": "Este texto será resumido em sentenças concisas que capturam a essência do conteúdo original...",
  "processing_type": "summarization",
  "status": "completed",
  "created_at": "2025-05-22T20:06:05.283625Z",
  "updated_at": "2025-05-22T20:06:15.123456Z"
}
```

#### Traduzir Texto

1. Inicie a tradução:
```bash
curl -X POST "http://localhost:8000/api/process-text" \
     -H "Content-Type: application/json" \
     -d '{
        "text": "Este é um texto de exemplo que será traduzido para o inglês.",
        "processing_type": "translation",
        "target_language": "English"
     }'
```

2. Obtenha o resultado usando o ID retornado:
```bash
curl -X GET "http://localhost:8000/api/tasks/16" -H "accept: application/json"
```

#### Detectar Idioma

A detecção de idioma é processada de forma síncrona e retorna o resultado imediatamente:
```bash
curl -X POST "http://localhost:8000/api/detect-language" \
     -H "Content-Type: application/json" \
     -d '{
        "text": "Este é um texto de exemplo para detecção de idioma."
     }'
```

## Testes

Execute os testes usando pytest:

```bash
# Executar todos os testes
pytest

# Executar testes específicos
pytest app/tests/test_language_detection.py
pytest app/tests/test_direct_translation.py

# Ou usar o make
make test
```

## Testes Diretos dos Agentes

Além dos testes via API, você pode testar diretamente os agentes de IA usando o script `test_agents_terminal.py`. Isso é útil para verificar o funcionamento dos modelos sem depender da API completa:

```bash
# Executar com o texto padrão 
python test_agents_terminal.py

# Executar com um texto personalizado
python test_agents_terminal.py "Seu texto personalizado aqui"
```

Este script testará:
- Tradução PT→EN
- Sumarização
- Detecção de idioma

Útil para depurar problemas com os modelos de IA ou quando a API completa não está a funcionar.


## CI/CD

O projeto utiliza GitHub Actions para integração contínua e entrega contínua. O pipeline está configurado em `.github/workflows/ci.yml` e inclui:

- Testes automatizados com PostgreSQL
- Verificação de qualidade de código com Flake8
- Build e deploy automático (para branches principais)


## Estrutura do Projeto

```
├── app/                          # Diretório principal da aplicação
│   ├── api/                      # Endpoints da API REST
│   │   └── routes.py             # Definição de rotas FastAPI
│   ├── core/                     # Configurações essenciais
│   │   ├── config.py             # Configurações da aplicação
│   │   └── security.py           # Funções de segurança
│   ├── db/                       # Interação com banco de dados
│   │   ├── database.py           # Configuração do SQLAlchemy
│   │   └── deps.py               # Dependências de banco de dados
│   ├── models/                   # Modelos de dados
│   │   ├── database.py           # Modelos SQLAlchemy
│   │   ├── language_models.py    # Modelos de idioma
│   │   └── pydantic_models.py    # Esquemas Pydantic para validação
│   ├── services/                 # Lógica de negócios
│   │   ├── crew_service.py       # Serviço principal com CrewAI
│   │   ├── direct_summarization_service.py  # Serviço de resumo
│   │   ├── direct_translation_service.py    # Serviço de tradução
│   │   └── language_service.py   # Serviço de detecção de idioma
│   ├── tests/                    # Testes automatizados
│   │   ├── test_basic.py         # Testes básicos
│   │   ├── test_crew_service.py  # Testes do serviço CrewAI
│   │   └── ... (outros testes)
│   └── utils/                    # Utilitários diversos
│       ├── errors.py             # Tratamento de erros
│       ├── logging_util.py       # Configuração de logs
│       └── metrics.py            # Métricas de desempenho
├── docker-compose.yml            # Configuração do Docker Compose
├── Dockerfile                    # Configuração do Docker
├── main.py                       # Ponto de entrada da aplicação
├── Makefile                      # Comandos de automação
├── requirements.txt              # Dependências do projeto
└── test_agents_terminal.py       # Script para testar agentes via terminal
```

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.
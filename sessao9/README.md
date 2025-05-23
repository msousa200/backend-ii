# Django Testing with pytest - Session 9

Este projeto demonstra técnicas avançadas de teste em aplicações Django usando pytest.

## Estrutura do Projeto

```
blog_project/
├── blog_app/               # Aplicação Django
│   ├── admin.py            # Configuração do admin
│   ├── apps.py             # Configuração da app
│   ├── models.py           # Modelos de dados
│   ├── serializers.py      # Serializadores para a API REST
│   ├── tests/              # Testes com pytest
│   │   ├── test_api.py     # Testes de API (challenge)
│   │   └── test_models.py  # Testes de modelos (exercise)
│   └── views.py            # Views da API REST
├── blog_project/           # Configuração do projeto
│   ├── settings.py         # Configurações Django
│   ├── urls.py             # URLs do projeto
│   ├── wsgi.py             # Configuração WSGI
│   └── asgi.py             # Configuração ASGI
├── conftest.py             # Configuração global do pytest
├── manage.py               # Script de gerenciamento Django
├── pytest.ini              # Configuração do pytest
└── requirements.txt        # Dependências do projeto
```

## Requisitos

Para executar o projeto, você precisa ter o Python 3.8+ instalado. Instale as dependências com:

```bash
pip install -r requirements.txt
```

## Executando os Testes

Para executar todos os testes:

```bash
pytest
```

Para executar apenas os testes de modelos (exercício):

```bash
pytest blog_app/tests/test_models.py -v
```

Para executar apenas os testes de API (desafio):

```bash
pytest blog_app/tests/test_api.py -v
```

Para gerar um relatório de cobertura de testes:

```bash
pytest --cov=blog_app
```

## Recursos Demonstrados

### Testes de Modelos (Exercício)
- Testes básicos de modelos Django
- Uso de `pytest.mark.django_db` para habilitar transações de banco de dados
- Uso de `freezegun` para mockar data/hora
- Testes parametrizados com `pytest.mark.parametrize`

### Testes de API (Desafio)
- Testes de endpoints da API REST
- Uso de fixtures para criação de dados de teste
- Testes de ações personalizadas
- Testes de filtros e parâmetros de consulta
- Testes de CRUD completo

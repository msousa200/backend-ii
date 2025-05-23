# Desafio de Segurança com Django

Este desafio demonstra como implementar medidas de segurança abrangentes em uma aplicação Django, incluindo:
- Proteção CSRF
- Gerenciamento seguro de sessões
- Validação e sanitização de entrada
- Proteção contra SQL Injection e XSS
- Limitação de tentativas de login
- Logging seguro

## Estrutura do Projeto

Os seguintes arquivos fazem parte deste desafio:

- `challenge.py` - Implementação principal das funcionalidades de segurança
- `django_settings.py` - Configurações de segurança do Django
- `django_urls.py` - Configuração de URLs do projeto
- `login_template.html` - Template de exemplo para o formulário de login
- `requirements-django.txt` - Dependências necessárias

## Em um projeto Django real

Em um projeto Django real, os componentes estariam organizados da seguinte forma:

```
secure_project/
├── manage.py
├── secure_project/
│   ├── __init__.py
│   ├── settings.py  # Equivalente ao django_settings.py
│   ├── urls.py      # Equivalente ao django_urls.py
│   └── wsgi.py
├── secure_app/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py     # Formulários do challenge.py
│   ├── middleware.py
│   ├── models.py    # Modelos do challenge.py
│   ├── tests.py
│   └── views.py     # Views do challenge.py
└── templates/
    └── login.html   # Equivalente ao login_template.html
```

## Conceitos de segurança demonstrados

1. **Proteção CSRF**:
   - Uso do decorador `@csrf_protect`
   - Middleware CSRF ativado
   - Tags de template `{% csrf_token %}`

2. **Gerenciamento Seguro de Sessões**:
   - Regeneração de ID da sessão (`cycle_key()`)
   - Timeout de sessão
   - Cookies seguros (HttpOnly, Secure, SameSite)

3. **Validação e Sanitização de Entrada**:
   - Formulários Django com validação
   - Sanitização com bleach
   - Validadores personalizados

4. **Proteção Contra SQL Injection e XSS**:
   - ORM Django
   - Sanitização de HTML
   - Sistema de templates seguro

5. **Limitação de Tentativas de Login**:
   - Implementação básica
   - Integração com django-axes

6. **Logging Seguro**:
   - Sem dados sensíveis
   - Configuração apropriada

## Executando em um projeto real

Para implementar estas medidas em um projeto Django real:

1. Instale as dependências:
   ```bash
   pip install -r requirements-django.txt
   ```

2. Incorpore as configurações de segurança de `django_settings.py` no seu arquivo `settings.py`

3. Adapte os modelos, formulários e views do `challenge.py` para sua aplicação

4. Implemente os templates conforme necessário, seguindo as práticas de segurança

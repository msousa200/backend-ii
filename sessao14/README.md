# Sessão 14: Introdução aos Agentes de IA em Python com CrewAI

Esta sessão introduz o conceito de agentes de IA usando o framework CrewAI para criar componentes autônomos capazes de realizar tarefas e responder de forma inteligente.

## Definição

Agentes de IA são componentes de software autônomos que realizam tarefas com base em entrada do usuário ou dados ambientais. O CrewAI simplifica a criação desses agentes, fornecendo módulos pré-construídos para conversação, tomada de decisões e integração com serviços externos. Os casos de uso incluem chatbots, suporte automatizado ao cliente e assistentes de análise de dados.

## Pré-requisitos

- Python 3.10+
- Pip (Gerenciador de pacotes Python)

## Configuração Rápida

Use o script de configuração incluído para preparar o ambiente:

```bash
./setup.sh
```

Ou configure manualmente:

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Copie o arquivo de exemplo de variáveis de ambiente:
```bash
cp .env.example .env
```

3. (Opcional) Edite .env para adicionar sua chave API do OpenAI

## Estrutura do Projeto

- `exercise.py`: Implementação de um agente de IA básico
- `challenge.py`: Implementação de um agente de IA avançado com processamento de múltiplas consultas
- `requirements.txt`: Dependências do projeto
- `setup.sh`: Script de configuração automatizada
- `TUTORIAL.md`: Guia detalhado sobre criação de agentes com CrewAI
- `EXEMPLOS.md`: Exemplos de interações com os agentes implementados
- `.env.example`: Modelo para configuração de variáveis de ambiente

## Executando o Projeto

### Exercício Básico
```bash
python exercise.py
```

### Desafio Avançado
```bash
python challenge.py
```

## Descrição das Implementações

### Exercício

O exercício implementa um agente de IA simples que:
- Responde a consultas específicas com mensagens predefinidas
- Utiliza um dicionário para mapear consultas a respostas
- Oferece uma interface de linha de comando para interação
- Inclui tratamento básico de erros e fallbacks

### Desafio

O desafio implementa um agente de IA avançado que:
- Utiliza múltiplos agentes especializados para diferentes tipos de consultas
- Identifica o tipo de consulta com base em palavras-chave e padrões
- Processa consultas usando expressões regulares
- Mantém um histórico de conversação para contexto
- Oferece respostas dinâmicas baseadas em dados atuais (hora/data)
- Implementa uma estrutura modular e extensível

## Recursos e Documentação

- [Tutorial Detalhado](./TUTORIAL.md) - Guia passo a passo para criar agentes com CrewAI
- [Exemplos de Interação](./EXEMPLOS.md) - Exemplos práticos de como usar os agentes implementados
- [Documentação do CrewAI](https://crew.ai/docs)
- [Repositório GitHub do CrewAI](https://github.com/crew-ai/crewai-python)
- [Wikipedia: Agentes Inteligentes](https://en.wikipedia.org/wiki/Intelligent_agent)

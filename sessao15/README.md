# Sessão 15: Desenvolvimento Avançado de Agentes IA com CrewAI

Esta sessão aprofunda o conhecimento em desenvolvimento de agentes de IA, integrando gerenciamento de estado e dados de APIs externas em agentes CrewAI.

## Definição

Agentes de IA avançados não apenas respondem a consultas, mas também mantêm contexto e aprendem com interações. A integração do gerenciamento de estado e chamadas para APIs externas permite que os agentes forneçam respostas dinâmicas e personalizadas. Casos de uso incluem chatbots que acompanham o histórico do usuário e motores de recomendação que ajustam respostas com base em dados em tempo real.

## Pré-requisitos

- Python 3.10+
- Conhecimento prévio de CrewAI (Sessão 14)
- Acesso a APIs externas (OpenWeatherMap, NewsAPI)

## Estrutura do Projeto

- `exercise.py`: Implementação de um agente de IA que busca dados meteorológicos
- `challenge.py`: Implementação de um agente avançado com múltiplas integrações de API e gerenciamento de estado
- `requirements.txt`: Dependências do projeto
- `README.md`: Documentação do projeto

## Recursos

### Exercício

O exercício implementa um agente de IA que busca dados em tempo real de uma API externa de clima e responde com a temperatura atual para uma cidade específica. Características principais:

- Integração com a API OpenWeatherMap
- Histórico de consultas
- Extração de nomes de cidades de consultas em linguagem natural
- Tratamento de erros de API
- Formatação de respostas com dados de clima

### Desafio

O desafio implementa um agente de IA avançado com capacidade de:

- **Gerenciamento de Estado Complexo**:
  - Histórico de conversas
  - Preferências do usuário
  - Cache de dados
  - Consultas recentes

- **Integração com Múltiplas APIs**:
  - API de clima (OpenWeatherMap)
  - API de notícias (NewsAPI)

- **Processamento de Linguagem Natural**:
  - Identificação de tipos de consulta
  - Extração de preferências implícitas
  - Roteamento de consultas para agentes especializados

- **Personalização de Respostas**:
  - Adaptação com base no histórico do usuário
  - Formatação avançada de respostas
  - Enriquecimento de dados de múltiplas fontes

## Configuração

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Configure as chaves de API no arquivo `.env`:

```
OPENWEATHER_API_KEY=sua-chave-aqui
NEWS_API_KEY=sua-chave-aqui
OPENAI_API_KEY=sua-chave-aqui
```

**Nota**: Você pode obter chaves de API gratuitamente em:
- [OpenWeatherMap](https://openweathermap.org/api)
- [NewsAPI](https://newsapi.org/)
- [OpenAI](https://platform.openai.com/)

## Executando os Agentes

### Agente de Clima (Exercício)

```bash
python exercise.py
```

### Agente Inteligente Avançado (Desafio)

```bash
python challenge.py
```

## Exemplos de Uso

### Agente de Clima

```
Você: Como está o clima em Lisboa?
ClimaTempo: 
Informações do clima para Lisboa, PT:

🌡️ Temperatura: 18.5°C
🌡️ Sensação térmica: 17.8°C
🔽 Mínima: 16.2°C
🔼 Máxima: 19.7°C
💧 Umidade: 68%
🌤️ Condição: céu limpo
💨 Velocidade do vento: 3.6 m/s
```

### Agente Avançado

```
Você: Quais são as últimas notícias sobre tecnologia?
EticSmart: 📰 **Notícias recentes sobre tecnologia**

1. **Apple anuncia novo iPhone com tecnologia de IA integrada**
   Fonte: TechCrunch | 2025-05-21
   A Apple revelou seu mais recente smartphone com processadores dedicados para IA.

2. **Microsoft investe bilhões em segurança cibernética**
   Fonte: The Verge | 2025-05-22
   A gigante da tecnologia anunciou investimentos massivos para aprimorar soluções de segurança.

3. **Novo avanço em computação quântica promete revolucionar o setor**
   Fonte: Wired | 2025-05-20
   Cientistas conseguiram estabilizar qubits por períodos recordes.

Você: Como está o clima em Paris?
EticSmart: 🌤️ **Clima em Paris**

Temperatura atual: 22.4°C
Sensação térmica: 21.9°C
Umidade: 54%
Condição: parcialmente nublado
Vento: 2.8 m/s

Você: Histórico
EticSmart: Aqui está o histórico recente das nossas conversas:

[14:30:15] Você: Quais são as últimas notícias sobre tecnologia?
[14:30:18] EticSmart: 📰 **Notícias recentes sobre tecnologia**...
[14:31:05] Você: Como está o clima em Paris?
[14:31:08] EticSmart: 🌤️ **Clima em Paris**...
[14:31:30] Você: Histórico
```

## Conceitos Avançados Demonstrados

1. **Gerenciamento de Estado**
   - Persistência de dados entre interações
   - Rastreamento de preferências do usuário
   - Histórico de conversas

2. **Integração de APIs**
   - Chamadas assíncronas para serviços externos
   - Tratamento de erros de API
   - Cache de dados para redução de chamadas

3. **Personalização**
   - Aprendizado a partir de interações anteriores
   - Adaptação baseada em preferências do usuário
   - Contextualização de respostas

4. **Arquitetura Multi-Agente**
   - Agentes especializados para diferentes tipos de consulta
   - Coordenação entre agentes
   - Seleção dinâmica de agente com base no contexto

## Recursos Adicionais

- [Documentação Avançada do CrewAI](https://crew.ai/docs/advanced)
- [Guia de Integração de APIs](https://github.com/crew-ai/crewai-python)
- [Melhores Práticas para Agentes de IA](https://en.wikipedia.org/wiki/Artificial_intelligence)

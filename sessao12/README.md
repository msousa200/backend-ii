# Sessão 12: Desenvolvendo Serviços gRPC em Python

Este diretório contém implementações de serviços gRPC usando Python, demonstrando comunicação eficiente entre cliente e servidor utilizando o framework gRPC e Protocol Buffers.

## Pré-requisitos

Para executar os exemplos, você precisa instalar as seguintes dependências:

```bash
pip install grpcio grpcio-tools
```

## Estrutura do Projeto

```
sessao12/
├── exercise/                 # Exemplo básico - Calculadora de Cubo
│   ├── proto/                # Definições Protocol Buffer
│   │   └── calculator.proto  # Arquivo de definição de serviço
│   ├── server.py             # Implementação do servidor
│   └── client.py             # Implementação do cliente
│
└── challenge/                # Exemplo avançado - Servidor de Streaming
    ├── proto/                # Definições Protocol Buffer
    │   └── streaming.proto   # Arquivo de definição de serviço com streaming
    ├── server.py             # Implementação do servidor com streaming
    └── client.py             # Cliente que consome stream de dados
```

## Exercício: Calculadora de Cubo

Este exemplo implementa um serviço gRPC que calcula o cubo de um número.

### Compilando o arquivo .proto

Antes de executar os scripts, você precisa gerar os stubs Python a partir do arquivo .proto:

```bash
cd exercise/
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/calculator.proto
```

### Executando o Servidor

```bash
# Em um terminal
cd exercise/
python server.py
```

### Executando o Cliente

```bash
# Em outro terminal
cd exercise/
python client.py 5  # Calcula o cubo de 5
```

## Desafio: Servidor de Streaming

Este exemplo implementa um serviço gRPC que utiliza server-side streaming para enviar múltiplos números para o cliente.

### Compilando o arquivo .proto

```bash
cd challenge/
python -m grpc_tools.protoc -I./proto --python_out=. --grpc_python_out=. ./proto/streaming.proto
```

### Executando o Servidor

```bash
# Em um terminal
cd challenge/
python server.py
```

### Executando o Cliente

```bash
# Em outro terminal
cd challenge/
python client.py 1 10  # Solicita números de 1 a 10
```

## Conceitos Demonstrados

1. **Exercício Básico**:
   - Definição de serviço gRPC simples usando Protocol Buffers
   - Implementação de chamada RPC unária (request-response)
   - Serialização/deserialização eficiente com Protocol Buffers

2. **Desafio de Streaming**:
   - Implementação de server-side streaming
   - Envio de múltiplas mensagens em resposta a uma única solicitação
   - Tratamento de erros em gRPC
   - Processamento de stream de dados no cliente

## Recursos Adicionais

- [Documentação oficial do gRPC](https://grpc.io/docs/languages/python/quickstart/)
- [Protocol Buffers](https://developers.google.com/protocol-buffers)
- [Tipos de comunicação em gRPC](https://grpc.io/docs/what-is-grpc/core-concepts/#rpc-life-cycle)

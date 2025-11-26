# 💬 Chat Distribuído com Pyro4

Sistema de chat corporativo para comunicação interna segura usando RPC (Remote Procedure Call).

## 📋 Requisitos

- Python 3.7+
- Pyro4

## 🚀 Instalação

```bash
pip install -r requirements.txt
```

## ▶️ Como Executar

### Passo 1: Iniciar o Name Server
Abra um terminal e execute:
```bash
python -m Pyro4.naming
```

### Passo 2: Iniciar o Servidor do Chat
Abra outro terminal e execute:
```bash
python -m server.start_server
```

### Passo 3: Iniciar Clientes
Abra quantos terminais quiser (um para cada cliente) e execute:
```bash
python -m client.start_client
```

## 📁 Estrutura do Projeto

```
chat-distribuido/
├── client/
│   ├── __init__.py
│   ├── chat_client.py      # Implementação do cliente
│   └── start_client.py     # Script para iniciar cliente
├── server/
│   ├── __init__.py
│   ├── chat_server.py      # Implementação do servidor
│   └── start_server.py     # Script para iniciar servidor
├── common/
│   ├── __init__.py
│   ├── models.py           # Modelos compartilhados (Mensagem)
│   └── utils.py            # Utilitários compartilhados
├── config/
│   ├── __init__.py
│   └── settings.py         # Configurações globais
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo
```

## 🎯 Funcionalidades Implementadas

✅ **Registro de usuários** com validação de nome  
✅ **Envio e recebimento de mensagens** em tempo real  
✅ **Broadcast automático** para todos os clientes conectados  
✅ **Histórico de mensagens** (últimas 100)  
✅ **Lista de usuários online** atualizada  
✅ **Comandos especiais** do sistema  
✅ **Detecção de inatividade** e desconexão automática  
✅ **Rate limiting** para prevenir spam  
✅ **Validações de segurança** em mensagens e nomes  

## 🔧 Comandos Disponíveis no Chat

- `/help` - Mostra mensagem de ajuda
- `/users` - Lista todos os usuários online
- `/history` - Mostra histórico de mensagens
- `/clear` - Limpa a tela do terminal
- `/quit` - Sair do chat

## 🏗️ Arquitetura

O sistema utiliza **arquitetura Cliente/Servidor** com **RPC via Pyro4**:

1. **Name Server (Pyro4)**: Serviço de registro e descoberta
2. **Servidor Central**: Gerencia usuários, mensagens e broadcast
3. **Clientes**: Interface de usuário para enviar/receber mensagens

## 🔐 Recursos de Segurança

- Validação de nomes de usuário (3-20 caracteres)
- Limite de tamanho de mensagens (500 caracteres)
- Rate limiting (30 mensagens por minuto)
- Timeout de inatividade (5 minutos)
- Sanitização de inputs

## 👥 Conceitos de Sistemas Distribuídos Aplicados

- **RPC (Remote Procedure Call)** via Pyro4
- **Name Server** para descoberta de serviços
- **Comunicação Cliente/Servidor**
- **Broadcast de mensagens**
- **Sincronização com locks**
- **Threading** para recepção assíncrona

## 📝 Autor

Projeto desenvolvido para disciplina de Sistemas Distribuídos

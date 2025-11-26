# 💬 Chat Distribuído com Pyro4

Sistema de chat corporativo usando RPC (Remote Procedure Call) para comunicação interna segura.

---

## 📋 Requisitos

- Python 3.7+
- Pyro4
- VS Code (recomendado)

---

## 🚀 Instalação

```bash
pip install -r requirements.txt
```

---

## ▶️ Como Executar

### 🎯 Método 1: Launcher Automático (Recomendado)

```bash
python launcher.py
```

O launcher irá:
1. Verificar dependências
2. Iniciar Name Server
3. Iniciar Servidor
4. Permitir iniciar clientes

### 📝 Método 2: Manual

**Terminal 1 - Name Server:**
```bash
python -m Pyro4.naming
```

**Terminal 2 - Servidor:**
```bash
python -m server.start_server
```

**Terminal 3+ - Clientes:**
```bash
python -m client.start_client
```

---

## 📁 Estrutura

```
chat-distribuido/
├── client/
│   ├── __init__.py
│   ├── chat_client.py       # Cliente
│   └── start_client.py      # Inicializador
│
├── server/
│   ├── __init__.py
│   ├── chat_server.py       # Servidor
│   └── start_server.py      # Inicializador
│
├── common/
│   ├── __init__.py
│   ├── models.py            # Modelo Mensagem
│   └── utils.py             # Utilitários
│
├── config/
│   ├── __init__.py
│   └── settings.py          # Configurações
│
├── launcher.py              # Launcher
├── requirements.txt         # Dependências
└── README.md               # Documentação
```

---

## 🎯 Funcionalidades

### ✅ Básicas
- Registro de usuários
- Envio/recebimento de mensagens
- Broadcast automático
- Histórico (100 mensagens)
- Lista de usuários online
- Comandos do sistema

### 🆕 Avançadas
- Rate limiting (30 msg/min)
- Detecção de inatividade (5 min)
- Reconexão automática
- Estatísticas em tempo real
- Validações de segurança
- Interface colorida

---

## 🔧 Comandos do Chat

| Comando | Descrição |
|---------|-----------|
| `/help` | Ajuda |
| `/users` | Usuários online |
| `/history` | Histórico |
| `/stats` | Estatísticas |
| `/clear` | Limpa tela |
| `/quit` ou `/exit` | Sair |

---

## 🏗️ Arquitetura

```
┌─────────────┐
│ Name Server │  ← Descoberta de serviços
└──────┬──────┘
       │
  ┌────┴────┬────────┐
  │         │        │
Cliente  Cliente  Cliente
  │         │        │
  └─────────┼────────┘
            │
      ┌─────▼─────┐
      │  Servidor │  ← Gerencia tudo
      └───────────┘
```

**Componentes:**
1. **Name Server**: Registro e descoberta
2. **Servidor Central**: Gerencia usuários e mensagens
3. **Clientes**: Interface de chat

---

## 🔐 Segurança

- Validação de username (3-20 chars)
- Limite de mensagem (500 chars)
- Rate limiting (30 msg/min)
- Timeout de inatividade (5 min)
- Sanitização de inputs
- Nomes proibidos

---

## 👥 Conceitos Distribuídos

- ✅ RPC via Pyro4
- ✅ Name Server
- ✅ Cliente/Servidor
- ✅ Broadcast
- ✅ Sincronização (locks)
- ✅ Threading
- ✅ Polling
- ✅ Tratamento de falhas

---

## 🐛 Troubleshooting

**"Name Server not found"**
```bash
python -m Pyro4.naming
```

**"Connection refused"**
- Verifique firewall
- Servidor rodando?

**"Nome já em uso"**
- Escolha outro nome

---

## 📊 Estatísticas

Use `/stats` para ver:
- Usuários online
- Total de mensagens
- Pico de usuários
- Tempo ativo

---

## 🎓 Requisitos Acadêmicos

### ✅ Atendidos

**Cliente/Servidor:**
- Servidor gerencia tudo
- Clientes via RPC

**Funcionalidades:**
- Registro ✔️
- Envio ✔️
- Recebimento ✔️
- Broadcast ✔️

**Pyro4:**
- Name Server ✔️
- Objetos remotos ✔️
- Proxy ✔️

**Conceitos:**
- RPC ✔️
- Sincronização ✔️
- Threading ✔️
- Falhas ✔️

---

## 💻 Tecnologias

- Python 3.x
- Pyro4 (RPC)
- Threading
- ANSI Colors

---

## 📝 Notas

- **Compatível:** Windows, Linux, macOS
- **IDE:** VS Code
- **Testado:** Python 3.8+
- **Capacidade:** 50+ clientes

---

## 🎯 Roadmap

- [ ] Mensagens privadas
- [ ] Salas/canais
- [ ] Banco de dados
- [ ] GUI
- [ ] Criptografia
- [ ] Autenticação

---

## 📄 Licença

Projeto acadêmico - Sistemas Distribuídos

---

## 👨‍💻 Autor

Desenvolvido para disciplina de Sistemas Distribuídos

---

**⭐ Dê uma estrela se foi útil!**

"""
Configurações Globais do Sistema de Chat
Centralizadas para facilitar manutenção
"""

import re

# ============================================================
# CONFIGURAÇÕES DO SERVIDOR
# ============================================================

NAMESERVER_HOST = "localhost"
NAMESERVER_PORT = 9090

CHAT_SERVER_NAME = "chat.server"
CHAT_SERVER_HOST = "0.0.0.0"

# ============================================================
# LIMITES E SEGURANÇA
# ============================================================

MAX_MESSAGE_LENGTH = 500
MAX_USERNAME_LENGTH = 20
MIN_USERNAME_LENGTH = 3
MAX_MESSAGES_PER_MINUTE = 30
MAX_HISTORY_SIZE = 100
CLIENT_TIMEOUT = 300  # 5 minutos

# ============================================================
# POLLING
# ============================================================

POLLING_INTERVAL = 0.5
MAX_RECONNECT_ATTEMPTS = 3
RECONNECT_DELAY = 2

# ============================================================
# MENSAGENS
# ============================================================

WELCOME_MESSAGE = """
╔══════════════════════════════════════════════════════════╗
║          BEM-VINDO AO CHAT DISTRIBUÍDO PYRO4            ║
║                                                          ║
║  🏢 Sistema de comunicação segura corporativa           ║
║  🔒 Protocolo RPC com Pyro4                             ║
║  💬 Chat em tempo real                                  ║
╚══════════════════════════════════════════════════════════╝
"""

HELP_MESSAGE = """
╔══════════════════════════════════════════════════════════╗
║                  📋 COMANDOS DISPONÍVEIS                ║
╚══════════════════════════════════════════════════════════╝

  🔹 /help      - Mostra esta mensagem de ajuda
  🔹 /users     - Lista todos os usuários online
  🔹 /history   - Mostra histórico de mensagens
  🔹 /stats     - Estatísticas do servidor
  🔹 /clear     - Limpa a tela
  🔹 /quit      - Sair do chat (/exit também funciona)

╔══════════════════════════════════════════════════════════╗
║                      💡 DICAS DE USO                     ║
╚══════════════════════════════════════════════════════════╝

  ✓ Mensagens começam automaticamente (sem comando)
  ✓ Use Ctrl+C para sair rapidamente
  ✓ Máximo de 500 caracteres por mensagem
  ✓ Limite de 30 mensagens por minuto
  ✓ Inatividade de 5 minutos = desconexão automática

"""

# ============================================================
# CORES ANSI
# ============================================================

class Colors:
    """Códigos de cores ANSI para terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# ============================================================
# VALIDAÇÕES
# ============================================================

def validar_username(username):
    """
    Valida nome de usuário
    
    Regras:
    - Entre 3 e 20 caracteres
    - Apenas letras, números e underscore
    - Deve começar com letra
    
    Args:
        username: Nome a validar
        
    Returns:
        tuple: (bool, str) - (valido, mensagem)
    """
    if not username:
        return False, "Nome não pode ser vazio"
    
    if len(username) < MIN_USERNAME_LENGTH:
        return False, f"Nome deve ter no mínimo {MIN_USERNAME_LENGTH} caracteres"
    
    if len(username) > MAX_USERNAME_LENGTH:
        return False, f"Nome deve ter no máximo {MAX_USERNAME_LENGTH} caracteres"
    
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        return False, "Nome deve começar com letra e conter apenas letras, números e _"
    
    palavras_proibidas = ['admin', 'root', 'sistema', 'server']
    if username.lower() in palavras_proibidas:
        return False, "Este nome não está disponível"
    
    return True, "OK"


def validar_mensagem(mensagem):
    """
    Valida mensagem antes de enviar
    
    Args:
        mensagem: Texto da mensagem
        
    Returns:
        tuple: (bool, str) - (valido, mensagem)
    """
    if not mensagem or not mensagem.strip():
        return False, "Mensagem não pode ser vazia"
    
    if len(mensagem) > MAX_MESSAGE_LENGTH:
        return False, f"Mensagem muito longa (máx: {MAX_MESSAGE_LENGTH} caracteres)"
    
    caracteres_proibidos = ['\0', '\r']
    for char in caracteres_proibidos:
        if char in mensagem:
            return False, "Mensagem contém caracteres inválidos"
    
    return True, "OK"

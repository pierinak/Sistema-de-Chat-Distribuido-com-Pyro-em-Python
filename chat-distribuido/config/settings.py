"""
Configurações Globais do Sistema de Chat
Centralizadas para facilitar manutenção
"""

# ============================================================
# CONFIGURAÇÕES DO SERVIDOR
# ============================================================

# Name Server
NAMESERVER_HOST = "localhost"
NAMESERVER_PORT = 9090

# Servidor do Chat
CHAT_SERVER_NAME = "chat.server"
CHAT_SERVER_HOST = "0.0.0.0"  # Aceita conexões de qualquer IP

# ============================================================
# LIMITES E SEGURANÇA
# ============================================================

# Limites de mensagens
MAX_MESSAGE_LENGTH = 500
MAX_USERNAME_LENGTH = 20
MIN_USERNAME_LENGTH = 3

# Taxa de mensagens (rate limiting)
MAX_MESSAGES_PER_MINUTE = 30

# Histórico
MAX_HISTORY_SIZE = 100

# Timeout
CLIENT_TIMEOUT = 300  # 5 minutos de inatividade

# ============================================================
# CONFIGURAÇÕES DE LOGGING
# ============================================================

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = "logs/chat.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================
# MENSAGENS DO SISTEMA
# ============================================================

WELCOME_MESSAGE = """
╔══════════════════════════════════════════════════════════╗
║          BEM-VINDO AO CHAT DISTRIBUÍDO PYRO4            ║
║                                                          ║
║  Sistema de comunicação segura para sua empresa         ║
╚══════════════════════════════════════════════════════════╝
"""

HELP_MESSAGE = """
📋 COMANDOS DISPONÍVEIS:

/help     - Mostra esta mensagem de ajuda
/users    - Lista todos os usuários online
/history  - Mostra histórico de mensagens
/clear    - Limpa a tela
/quit     - Sair do chat

💡 DICAS:
- Mensagens começam automaticamente (sem comando)
- Use Ctrl+C para sair rapidamente
- Máximo de {max_len} caracteres por mensagem
""".format(max_len=MAX_MESSAGE_LENGTH)

# ============================================================
# CORES PARA TERMINAL (ANSI)
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
    - Não pode começar com número
    """
    import re
    
    if not username:
        return False, "Nome de usuário não pode ser vazio"
    
    if len(username) < MIN_USERNAME_LENGTH:
        return False, f"Nome deve ter no mínimo {MIN_USERNAME_LENGTH} caracteres"
    
    if len(username) > MAX_USERNAME_LENGTH:
        return False, f"Nome deve ter no máximo {MAX_USERNAME_LENGTH} caracteres"
    
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        return False, "Nome deve começar com letra e conter apenas letras, números e _"
    
    return True, "OK"


def validar_mensagem(mensagem):
    """Valida mensagem antes de enviar"""
    if not mensagem or not mensagem.strip():
        return False, "Mensagem não pode ser vazia"
    
    if len(mensagem) > MAX_MESSAGE_LENGTH:
        return False, f"Mensagem muito longa (máx: {MAX_MESSAGE_LENGTH} caracteres)"
    
    return True, "OK"
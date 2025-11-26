# ==================== server/start_server.py ====================
"""
Script de inicialização do servidor de chat
Ponto de entrada principal para o servidor
"""

import sys
import os

# Adiciona pasta raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.chat_server import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Servidor encerrado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro fatal no servidor: {e}")
        sys.exit(1)

# ==================== client/start_client.py ====================
"""
Script de inicialização do cliente de chat
Ponto de entrada principal para o cliente
"""

import sys
import os

# Adiciona pasta raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.chat_client import main

if __name__ == "__main__":
    main()

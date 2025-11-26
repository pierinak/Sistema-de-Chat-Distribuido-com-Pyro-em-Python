"""
Script de inicialização do cliente
"""

import sys
import os

# Adiciona pasta raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client.chat_client import main

if __name__ == "__main__":
    main()

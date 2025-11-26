# ==================== common/utils.py ====================
"""
Utilitários compartilhados entre cliente e servidor
"""

def formatar_timestamp(dt):
    """Formata datetime para exibição"""
    return dt.strftime("%d/%m/%Y %H:%M:%S")


def truncar_texto(texto, max_len=50):
    """Trunca texto longo"""
    if len(texto) <= max_len:
        return texto
    return texto[:max_len-3] + "..."


def limpar_terminal():
    """Limpa o terminal de forma cross-platform"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

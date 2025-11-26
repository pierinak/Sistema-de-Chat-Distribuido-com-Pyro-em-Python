"""
Utilitários compartilhados
"""

import os


def formatar_timestamp(dt):
    """
    Formata datetime para exibição
    
    Args:
        dt: objeto datetime
        
    Returns:
        str: Data/hora formatada
    """
    return dt.strftime("%d/%m/%Y %H:%M:%S")


def truncar_texto(texto, max_len=50):
    """
    Trunca texto longo
    
    Args:
        texto: Texto a truncar
        max_len: Comprimento máximo
        
    Returns:
        str: Texto truncado
    """
    if len(texto) <= max_len:
        return texto
    return texto[:max_len-3] + "..."


def limpar_terminal():
    """Limpa terminal (multiplataforma)"""
    os.system('cls' if os.name == 'nt' else 'clear')


def formatar_duracao(segundos):
    """
    Formata duração em segundos
    
    Args:
        segundos: Número de segundos
        
    Returns:
        str: Duração formatada (ex: "2h 30m")
    """
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segs = int(segundos % 60)
    
    partes = []
    if horas > 0:
        partes.append(f"{horas}h")
    if minutos > 0:
        partes.append(f"{minutos}m")
    if segs > 0 or not partes:
        partes.append(f"{segs}s")
    
    return " ".join(partes)

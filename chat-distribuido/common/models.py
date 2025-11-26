"""
Modelos de dados compartilhados entre cliente e servidor
"""

from datetime import datetime


class Mensagem:
    """
    Representa uma mensagem no sistema de chat
    
    Attributes:
        remetente (str): Nome do usuário que enviou
        conteudo (str): Texto da mensagem
        timestamp (datetime): Data/hora do envio
        tipo (str): Tipo da mensagem (normal, sistema, erro)
    """
    
    def __init__(self, remetente, conteudo, timestamp=None, tipo="normal"):
        """
        Cria nova mensagem
        
        Args:
            remetente: Nome do remetente
            conteudo: Conteúdo da mensagem
            timestamp: Data/hora (usa datetime.now() se None)
            tipo: Tipo da mensagem
        """
        self.remetente = remetente
        self.conteudo = conteudo
        self.timestamp = timestamp or datetime.now()
        self.tipo = tipo

    def to_dict(self):
        """
        Converte mensagem para dicionário
        
        Returns:
            dict: Dados da mensagem
        """
        return {
            "remetente": self.remetente,
            "conteudo": self.conteudo,
            "timestamp": self.timestamp.isoformat(),
            "tipo": self.tipo,
        }

    @staticmethod
    def from_dict(d):
        """
        Cria mensagem a partir de dicionário
        
        Args:
            d: Dicionário com dados
            
        Returns:
            Mensagem: Nova instância
        """
        return Mensagem(
            remetente=d["remetente"],
            conteudo=d["conteudo"],
            timestamp=datetime.fromisoformat(d["timestamp"]),
            tipo=d.get("tipo", "normal")
        )
    
    def __str__(self):
        """Representação em string"""
        hora = self.timestamp.strftime("%H:%M:%S")
        return f"[{hora}] {self.remetente}: {self.conteudo}"
    
    def __repr__(self):
        """Representação técnica"""
        return f"Mensagem(remetente={self.remetente}, tipo={self.tipo})"

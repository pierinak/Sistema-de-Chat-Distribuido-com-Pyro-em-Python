"""
Modelos de dados compartilhados entre cliente e servidor
"""

from datetime import datetime


class Mensagem:
    def __init__(self, remetente, conteudo, timestamp=None, tipo="normal"):
        self.remetente = remetente
        self.conteudo = conteudo
        self.timestamp = timestamp or datetime.now()
        self.tipo = tipo  # normal, sistema, erro

    def to_dict(self):
        return {
            "remetente": self.remetente,
            "conteudo": self.conteudo,
            "timestamp": self.timestamp.isoformat(),
            "tipo": self.tipo,
        }

    @staticmethod
    def from_dict(d):
        return Mensagem(
            remetente=d["remetente"],
            conteudo=d["conteudo"],
            timestamp=datetime.fromisoformat(d["timestamp"]),
            tipo=d.get("tipo", "normal")
        )

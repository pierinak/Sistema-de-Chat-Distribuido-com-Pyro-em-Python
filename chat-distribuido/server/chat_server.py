"""
Servidor de Chat Distribuído usando Pyro4
Gerencia usuários, mensagens, histórico e broadcast
"""

import Pyro4
import threading
import time
from datetime import datetime

from config.settings import (
    CHAT_SERVER_NAME,
    MAX_HISTORY_SIZE,
    CLIENT_TIMEOUT,
    validar_mensagem,
    validar_username,
)

from common.models import Mensagem


@Pyro4.expose
class ChatServer:
    """Servidor principal do chat"""

    def __init__(self):
        self.usuarios = {}   # nome → timestamp da última atividade
        self.mensagens = []  # lista de Mensagem
        self.lock = threading.Lock()

        # Thread de limpeza
        self.limpeza_thread = threading.Thread(target=self._limpar_inativos, daemon=True)
        self.limpeza_thread.start()

    # -------------------------------
    # Funções básicas
    # -------------------------------

    def ping(self):
        """Usado pelo cliente para verificar disponibilidade"""
        return True

    def registrar_usuario(self, nome):
        """Registra novo usuário"""
        valido, msg = validar_username(nome)
        if not valido:
            return False, msg

        with self.lock:
            if nome in self.usuarios:
                return False, "Nome já está em uso"

            self.usuarios[nome] = time.time()

            # Mensagem de sistema
            self._registrar_sistema(f"🔵 {nome} entrou no chat")

        return True, "Usuário registrado com sucesso"

    def desconectar_usuario(self, nome):
        """Remove usuário do servidor"""
        with self.lock:
            if nome in self.usuarios:
                del self.usuarios[nome]
                self._registrar_sistema(f"🔴 {nome} saiu do chat")

    # -------------------------------
    # Mensagens
    # -------------------------------

    def enviar_mensagem(self, remetente, conteudo):
        """Recebe e armazena mensagens dos clientes"""
        valido, msg = validar_mensagem(conteudo)
        if not valido:
            return False, msg

        msg = Mensagem(remetente, conteudo, datetime.now())

        with self.lock:
            self.usuarios[remetente] = time.time()  # Atualiza atividade
            self.mensagens.append(msg)

            # mantém o histórico limitado
            if len(self.mensagens) > MAX_HISTORY_SIZE:
                self.mensagens = self.mensagens[-MAX_HISTORY_SIZE:]

        return True, "Mensagem enviada"

    def obter_mensagens(self, usuario, ultimo_id):
        """Retorna mensagens novas a partir de um índice"""
        with self.lock:
            self.usuarios[usuario] = time.time()
            novas = self.mensagens[ultimo_id:]
            return [msg.to_dict() for msg in novas]

    def obter_historico(self, limite=20):
        """Retorna as últimas 'limite' mensagens"""
        with self.lock:
            return [m.to_dict() for m in self.mensagens[-limite:]]

    def obter_usuarios_online(self):
        """Retorna lista de usuários ativos"""
        with self.lock:
            return list(self.usuarios.keys())

    # -------------------------------
    # Suporte
    # -------------------------------

    def _registrar_sistema(self, texto):
        """Insere mensagem de sistema"""
        m = Mensagem("Sistema", texto, datetime.now(), tipo="sistema")
        self.mensagens.append(m)

    def _limpar_inativos(self):
        """Remove usuários que ficaram tempo demais sem enviar nada"""
        while True:
            time.sleep(5)
            agora = time.time()

            with self.lock:
                remover = [
                    u for u, ts in self.usuarios.items()
                    if agora - ts > CLIENT_TIMEOUT
                ]
                for u in remover:
                    del self.usuarios[u]
                    self._registrar_sistema(f"⚠️ {u} desconectado por inatividade")


def main():
    """Inicia servidor e registra no NameServer"""
    print("🚀 Iniciando servidor do Chat...")

    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()

    server = ChatServer()

    uri = daemon.register(server)
    ns.register(CHAT_SERVER_NAME, uri)

    print(f"Servidor registrado como: {CHAT_SERVER_NAME}")
    print("Aguardando conexões...\n")

    daemon.requestLoop()


if __name__ == "__main__":
    main()

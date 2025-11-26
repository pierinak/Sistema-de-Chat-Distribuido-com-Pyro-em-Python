"""
Servidor de Chat Distribuído usando Pyro4
Gerencia usuários, mensagens e broadcast
"""

import Pyro4
import threading
import time
from datetime import datetime
from collections import defaultdict

from config.settings import (
    CHAT_SERVER_NAME,
    MAX_HISTORY_SIZE,
    CLIENT_TIMEOUT,
    MAX_MESSAGES_PER_MINUTE,
    validar_mensagem,
    validar_username,
)

from common.models import Mensagem


@Pyro4.expose
class ChatServer:
    """Servidor principal do chat"""

    def __init__(self):
        """Inicializa o servidor"""
        self.usuarios = {}  # nome -> timestamp última atividade
        self.mensagens = []  # lista de objetos Mensagem
        self.lock = threading.Lock()
        
        # Rate limiting por usuário
        self.message_timestamps = defaultdict(list)
        
        # Estatísticas
        self.stats = {
            'total_messages': 0,
            'total_users': 0,
            'peak_users': 0,
            'start_time': datetime.now()
        }

        # Inicia thread de limpeza
        self.limpeza_thread = threading.Thread(
            target=self._limpar_inativos, 
            daemon=True
        )
        self.limpeza_thread.start()
        
        print("✅ Servidor inicializado")

    def ping(self):
        """Verifica se servidor está ativo"""
        return True

    def registrar_usuario(self, nome):
        """
        Registra novo usuário
        
        Args:
            nome: Nome do usuário
            
        Returns:
            tuple: (sucesso, mensagem)
        """
        valido, msg = validar_username(nome)
        if not valido:
            return False, msg

        with self.lock:
            if nome in self.usuarios:
                return False, "❌ Nome já em uso"

            self.usuarios[nome] = time.time()
            self.stats['total_users'] += 1
            self.stats['peak_users'] = max(
                self.stats['peak_users'], 
                len(self.usuarios)
            )

            self._registrar_sistema(f"🔵 {nome} entrou no chat")
            
            print(f"[REGISTRO] '{nome}' conectado. Online: {len(self.usuarios)}")

        return True, f"✅ Bem-vindo, {nome}!"

    def desconectar_usuario(self, nome):
        """
        Remove usuário
        
        Args:
            nome: Nome do usuário
        """
        with self.lock:
            if nome in self.usuarios:
                del self.usuarios[nome]
                self._registrar_sistema(f"🔴 {nome} saiu do chat")
                
                if nome in self.message_timestamps:
                    del self.message_timestamps[nome]
                
                print(f"[SAÍDA] '{nome}' desconectado. Online: {len(self.usuarios)}")

    def enviar_mensagem(self, remetente, conteudo):
        """
        Recebe mensagem do cliente
        
        Args:
            remetente: Nome do remetente
            conteudo: Texto da mensagem
            
        Returns:
            tuple: (sucesso, mensagem)
        """
        valido, msg = validar_mensagem(conteudo)
        if not valido:
            return False, msg
        
        # Rate limiting
        agora = time.time()
        with self.lock:
            # Remove timestamps antigos
            self.message_timestamps[remetente] = [
                ts for ts in self.message_timestamps[remetente]
                if agora - ts < 60
            ]
            
            # Verifica limite
            if len(self.message_timestamps[remetente]) >= MAX_MESSAGES_PER_MINUTE:
                return False, f"⚠️ Limite de {MAX_MESSAGES_PER_MINUTE} msg/min"
            
            self.message_timestamps[remetente].append(agora)

        # Cria mensagem
        msg_obj = Mensagem(remetente, conteudo, datetime.now())

        with self.lock:
            self.usuarios[remetente] = time.time()
            self.mensagens.append(msg_obj)
            self.stats['total_messages'] += 1

            # Limita histórico
            if len(self.mensagens) > MAX_HISTORY_SIZE:
                self.mensagens = self.mensagens[-MAX_HISTORY_SIZE:]

        return True, "✅ Enviada"

    def obter_mensagens(self, usuario, ultimo_id):
        """
        Retorna novas mensagens
        
        Args:
            usuario: Nome do usuário
            ultimo_id: ID da última mensagem recebida
            
        Returns:
            list: Lista de dicionários com mensagens
        """
        with self.lock:
            if usuario in self.usuarios:
                self.usuarios[usuario] = time.time()
            
            novas = self.mensagens[ultimo_id:]
            return [msg.to_dict() for msg in novas]

    def obter_historico(self, limite=20):
        """
        Retorna histórico de mensagens
        
        Args:
            limite: Número de mensagens
            
        Returns:
            list: Lista de mensagens
        """
        with self.lock:
            return [m.to_dict() for m in self.mensagens[-limite:]]

    def obter_usuarios_online(self):
        """
        Retorna lista de usuários online
        
        Returns:
            list: Nomes dos usuários
        """
        with self.lock:
            return sorted(list(self.usuarios.keys()))
    
    def obter_estatisticas(self):
        """
        Retorna estatísticas do servidor
        
        Returns:
            dict: Estatísticas
        """
        with self.lock:
            uptime = datetime.now() - self.stats['start_time']
            return {
                'usuarios_online': len(self.usuarios),
                'total_mensagens': self.stats['total_messages'],
                'total_usuarios_historico': self.stats['total_users'],
                'pico_usuarios': self.stats['peak_users'],
                'uptime_segundos': uptime.total_seconds(),
                'uptime_formatado': str(uptime).split('.')[0]
            }

    def _registrar_sistema(self, texto):
        """Adiciona mensagem de sistema"""
        m = Mensagem("Sistema", texto, datetime.now(), tipo="sistema")
        self.mensagens.append(m)

    def _limpar_inativos(self):
        """Thread que remove usuários inativos"""
        while True:
            time.sleep(30)
            agora = time.time()

            with self.lock:
                remover = [
                    u for u, ts in self.usuarios.items()
                    if agora - ts > CLIENT_TIMEOUT
                ]
                
                for u in remover:
                    del self.usuarios[u]
                    self._registrar_sistema(f"⚠️ {u} desconectado (inatividade)")
                    print(f"[TIMEOUT] '{u}' removido")
                    
                    if u in self.message_timestamps:
                        del self.message_timestamps[u]


def main():
    """Inicia o servidor"""
    print("\n" + "="*60)
    print("🚀 SERVIDOR DO CHAT DISTRIBUÍDO")
    print("="*60 + "\n")

    try:
        print("📡 Conectando ao Name Server...")
        daemon = Pyro4.Daemon()
        ns = Pyro4.locateNS()
        
        print("🔧 Criando servidor...")
        server = ChatServer()

        print("📝 Registrando no Name Server...")
        uri = daemon.register(server)
        ns.register(CHAT_SERVER_NAME, uri)

        print(f"\n✅ Servidor: {CHAT_SERVER_NAME}")
        print(f"📍 URI: {uri}")
        print("\n" + "="*60)
        print("🟢 SERVIDOR ATIVO - Aguardando conexões")
        print("="*60 + "\n")
        print("💡 Ctrl+C para encerrar\n")

        daemon.requestLoop()
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

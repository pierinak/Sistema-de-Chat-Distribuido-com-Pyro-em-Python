"""
Cliente do Chat Distribuído
Interface para usuário se conectar e interagir
"""

import Pyro4
import sys
import os
import time
import threading
from datetime import datetime

# Adiciona pasta pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.models import Mensagem
from config.settings import (
    WELCOME_MESSAGE, HELP_MESSAGE, Colors,
    validar_username, validar_mensagem
)


class ChatClient:
    """Cliente do chat com interface de linha de comando"""
    
    def __init__(self):
        self.servidor = None
        self.nome_usuario = None
        self.rodando = False
        self.ultima_msg_id = 0
    
    def conectar(self):
        """Conecta ao servidor via Name Server"""
        try:
            print("🔍 Localizando servidor...")
            ns = Pyro4.locateNS()
            uri = ns.lookup("chat.server")
            self.servidor = Pyro4.Proxy(uri)
            
            # Testa conexão
            if self.servidor.ping():
                print("✅ Conectado ao servidor!\n")
                return True
                
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            print("\n💡 Certifique-se de que:")
            print("   1. Name Server está rodando: python -m Pyro4.naming")
            print("   2. Servidor está rodando: python server/start_server.py")
            return False
    
    def registrar(self):
        """Registra usuário no servidor"""
        print("="*60)
        print("📝 REGISTRO")
        print("="*60)
        
        while True:
            nome = input("\n👤 Digite seu nome de usuário: ").strip()
            
            # Valida localmente
            valido, msg = validar_username(nome)
            if not valido:
                print(f"{Colors.FAIL}❌ {msg}{Colors.ENDC}")
                continue
            
            # Registra no servidor
            try:
                sucesso, mensagem = self.servidor.registrar_usuario(nome)
                
                if sucesso:
                    self.nome_usuario = nome
                    print(f"{Colors.OKGREEN}✅ {mensagem}{Colors.ENDC}")
                    return True
                else:
                    print(f"{Colors.FAIL}❌ {mensagem}{Colors.ENDC}")
                    
            except Exception as e:
                print(f"{Colors.FAIL}❌ Erro: {e}{Colors.ENDC}")
                return False
    
    def receber_mensagens(self):
        """Thread para receber mensagens do servidor"""
        while self.rodando:
            try:
                # Busca novas mensagens
                mensagens = self.servidor.obter_mensagens(
                    self.nome_usuario, 
                    self.ultima_msg_id
                )
                
                if mensagens:
                    for msg_dict in mensagens:
                        msg = Mensagem.from_dict(msg_dict)
                        self.exibir_mensagem(msg)
                    
                    self.ultima_msg_id += len(mensagens)
                
                time.sleep(0.5)  # Polling a cada 0.5s
                
            except Exception as e:
                if self.rodando:
                    print(f"\n{Colors.FAIL}❌ Erro ao receber mensagens: {e}{Colors.ENDC}")
                    break
    
    def exibir_mensagem(self, msg):
        """Exibe mensagem formatada"""
        hora = msg.timestamp.strftime("%H:%M:%S")
        
        # Define cor baseada no tipo
        if msg.tipo == "sistema":
            cor = Colors.OKCYAN
            print(f"\r{cor}[{hora}] {msg.conteudo}{Colors.ENDC}")
            
        elif msg.tipo == "erro":
            cor = Colors.FAIL
            print(f"\r{cor}[{hora}] ERRO: {msg.conteudo}{Colors.ENDC}")
            
        elif msg.remetente == self.nome_usuario:
            # Mensagem própria
            cor = Colors.OKGREEN
            print(f"\r{cor}[{hora}] Você: {msg.conteudo}{Colors.ENDC}")
            
        else:
            # Mensagem de outro usuário
            cor = Colors.OKBLUE
            print(f"\r{cor}[{hora}] {msg.remetente}: {msg.conteudo}{Colors.ENDC}")
        
        # Reimprime prompt
        print(f"\n{self.nome_usuario}> ", end="", flush=True)
    
    def enviar_mensagem(self, conteudo):
        """Envia mensagem para o servidor"""
        try:
            sucesso, mensagem = self.servidor.enviar_mensagem(
                self.nome_usuario,
                conteudo
            )
            
            if not sucesso:
                print(f"{Colors.FAIL}❌ {mensagem}{Colors.ENDC}")
                
        except Exception as e:
            print(f"{Colors.FAIL}❌ Erro ao enviar: {e}{Colors.ENDC}")
    
    def listar_usuarios(self):
        """Lista usuários online"""
        try:
            usuarios = self.servidor.obter_usuarios_online()
            
            print(f"\n{Colors.BOLD}👥 USUÁRIOS ONLINE ({len(usuarios)}):{Colors.ENDC}")
            for i, usuario in enumerate(usuarios, 1):
                indicador = "👉" if usuario == self.nome_usuario else "  "
                print(f"{indicador} {i}. {usuario}")
            print()
            
        except Exception as e:
            print(f"{Colors.FAIL}❌ Erro: {e}{Colors.ENDC}")
    
    def mostrar_historico(self):
        """Mostra histórico de mensagens"""
        try:
            mensagens = self.servidor.obter_historico(limite=20)
            
            print(f"\n{Colors.BOLD}📜 HISTÓRICO (últimas 20 mensagens):{Colors.ENDC}\n")
            
            for msg_dict in mensagens:
                msg = Mensagem.from_dict(msg_dict)
                self.exibir_mensagem(msg)
            
            print()
            
        except Exception as e:
            print(f"{Colors.FAIL}❌ Erro: {e}{Colors.ENDC}")
    
    def processar_comando(self, texto):
        """Processa comandos especiais"""
        if texto == "/help":
            print(HELP_MESSAGE)
            
        elif texto == "/users":
            self.listar_usuarios()
            
        elif texto == "/history":
            self.mostrar_historico()
            
        elif texto == "/clear":
            os.system('clear' if os.name == 'posix' else 'cls')
            print(WELCOME_MESSAGE)
            
        elif texto == "/quit":
            self.desconectar()
            return False
            
        else:
            print(f"{Colors.FAIL}❌ Comando desconhecido. Use /help{Colors.ENDC}")
        
        return True
    
    def loop_principal(self):
        """Loop de envio de mensagens"""
        print(WELCOME_MESSAGE)
        print(f"{Colors.OKGREEN}✅ Conectado como: {self.nome_usuario}{Colors.ENDC}\n")
        print("💡 Digite /help para ver comandos disponíveis\n")
        
        self.rodando = True
        
        # Inicia thread de recebimento
        thread_receber = threading.Thread(target=self.receber_mensagens, daemon=True)
        thread_receber.start()
        
        try:
            while self.rodando:
                try:
                    texto = input(f"{self.nome_usuario}> ").strip()
                    
                    if not texto:
                        continue
                    
                    # Verifica se é comando
                    if texto.startswith('/'):
                        if not self.processar_comando(texto):
                            break
                    else:
                        # Envia mensagem normal
                        self.enviar_mensagem(texto)
                
                except KeyboardInterrupt:
                    print("\n\n⚠️  Interrompido pelo usuário")
                    break
                    
        finally:
            self.desconectar()
    
    def desconectar(self):
        """Desconecta do servidor"""
        if self.rodando:
            self.rodando = False
            
            try:
                if self.servidor and self.nome_usuario:
                    self.servidor.desconectar_usuario(self.nome_usuario)
                    print(f"\n{Colors.OKCYAN}👋 Desconectado do servidor{Colors.ENDC}")
            except:
                pass
    
    def iniciar(self):
        """Inicia cliente completo"""
        print("="*60)
        print("💬 CLIENTE DO CHAT DISTRIBUÍDO")
        print("="*60)
        
        # Conecta ao servidor
        if not self.conectar():
            return
        
        # Registra usuário
        if not self.registrar():
            return
        
        # Entra no loop principal
        self.loop_principal()


def main():
    """Ponto de entrada do cliente"""
    cliente = ChatClient()
    
    try:
        cliente.iniciar()
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Erro fatal: {e}{Colors.ENDC}")
    finally:
        print("\n✅ Cliente encerrado\n")


if __name__ == "__main__":
    main()
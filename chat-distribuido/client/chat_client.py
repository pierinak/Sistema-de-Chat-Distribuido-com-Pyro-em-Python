"""
Cliente do Chat Distribuído
Interface de linha de comando
"""

import Pyro4
import sys
import os
import time
import threading
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.models import Mensagem
from config.settings import (
    WELCOME_MESSAGE, HELP_MESSAGE, Colors,
    validar_username, validar_mensagem
)


class ChatClient:
    """Cliente do chat"""
    
    def __init__(self):
        """Inicializa cliente"""
        self.servidor = None
        self.nome_usuario = None
        self.rodando = False
        self.ultima_msg_id = 0
        self.conectado = False
    
    def conectar(self):
        """Conecta ao servidor via Name Server"""
        tentativas = 3
        
        for i in range(tentativas):
            try:
                print(f"🔍 Tentativa {i+1}/{tentativas}...")
                ns = Pyro4.locateNS()
                uri = ns.lookup("chat.server")
                self.servidor = Pyro4.Proxy(uri)
                
                if self.servidor.ping():
                    print(f"{Colors.OKGREEN}✅ Conectado!{Colors.ENDC}\n")
                    self.conectado = True
                    return True
                    
            except Exception as e:
                print(f"{Colors.WARNING}⚠️  Falhou: {e}{Colors.ENDC}")
                if i < tentativas - 1:
                    print("⏳ Aguardando...\n")
                    time.sleep(2)
        
        print(f"\n{Colors.FAIL}❌ Não conectou{Colors.ENDC}")
        print("\n💡 Verifique:")
        print("   1. Name Server rodando")
        print("   2. Servidor rodando")
        return False
    
    def registrar(self):
        """Registra usuário no servidor"""
        print("="*60)
        print(f"{Colors.BOLD}📝 REGISTRO{Colors.ENDC}")
        print("="*60)
        print(f"\n{Colors.OKCYAN}ℹ️  3-20 caracteres (letras, números, _){Colors.ENDC}")
        
        tentativas = 0
        max_tentativas = 3
        
        while tentativas < max_tentativas:
            nome = input(f"\n{Colors.BOLD}👤 Nome:{Colors.ENDC} ").strip()
            
            if not nome:
                print(f"{Colors.WARNING}⚠️  Vazio{Colors.ENDC}")
                continue
            
            valido, msg = validar_username(nome)
            if not valido:
                print(f"{Colors.FAIL}❌ {msg}{Colors.ENDC}")
                tentativas += 1
                continue
            
            try:
                sucesso, mensagem = self.servidor.registrar_usuario(nome)
                
                if sucesso:
                    self.nome_usuario = nome
                    print(f"\n{Colors.OKGREEN}{mensagem}{Colors.ENDC}")
                    time.sleep(1)
                    return True
                else:
                    print(f"{Colors.FAIL}{mensagem}{Colors.ENDC}")
                    tentativas += 1
                    
            except Exception as e:
                print(f"{Colors.FAIL}❌ Erro: {e}{Colors.ENDC}")
                return False
        
        print(f"\n{Colors.FAIL}❌ Máximo de tentativas{Colors.ENDC}")
        return False
    
    def receber_mensagens(self):
        """Thread que recebe mensagens"""
        erros = 0
        max_erros = 5
        
        while self.rodando:
            try:
                mensagens = self.servidor.obter_mensagens(
                    self.nome_usuario, 
                    self.ultima_msg_id
                )
                
                if mensagens:
                    for msg_dict in mensagens:
                        msg = Mensagem.from_dict(msg_dict)
                        self.exibir_mensagem(msg)
                    
                    self.ultima_msg_id += len(mensagens)
                
                erros = 0
                time.sleep(0.5)
                
            except Exception as e:
                erros += 1
                
                if erros >= max_erros:
                    if self.rodando:
                        print(f"\n{Colors.FAIL}❌ Conexão perdida{Colors.ENDC}")
                        self.rodando = False
                    break
                
                time.sleep(1)
    
    def exibir_mensagem(self, msg):
        """Exibe mensagem formatada"""
        hora = msg.timestamp.strftime("%H:%M:%S")
        
        if msg.tipo == "sistema":
            cor = Colors.OKCYAN
            texto = f"[{hora}] {msg.conteudo}"
            
        elif msg.tipo == "erro":
            cor = Colors.FAIL
            texto = f"[{hora}] ⚠️  {msg.conteudo}"
            
        elif msg.remetente == self.nome_usuario:
            cor = Colors.OKGREEN
            texto = f"[{hora}] Você: {msg.conteudo}"
            
        else:
            cor = Colors.OKBLUE
            texto = f"[{hora}] {msg.remetente}: {msg.conteudo}"
        
        print(f"\r{cor}{texto}{Colors.ENDC}")
        print(f"{Colors.BOLD}{self.nome_usuario}>{Colors.ENDC} ", end="", flush=True)
    
    def enviar_mensagem(self, conteudo):
        """Envia mensagem"""
        valido, msg = validar_mensagem(conteudo)
        if not valido:
            print(f"{Colors.FAIL}❌ {msg}{Colors.ENDC}")
            return
        
        try:
            sucesso, mensagem = self.servidor.enviar_mensagem(
                self.nome_usuario,
                conteudo
            )
            
            if not sucesso:
                print(f"{Colors.FAIL}{mensagem}{Colors.ENDC}")
                
        except Exception as e:
            print(f"{Colors.FAIL}❌ Erro: {e}{Colors.ENDC}")
    
    def listar_usuarios(self):
        """Lista usuários online"""
        try:
            usuarios = self.servidor.obter_usuarios_online()
            
            print(f"\n{Colors.HEADER}{'='*50}{Colors.ENDC}")
            print(f"{Colors.BOLD}👥 ONLINE ({len(usuarios)}){Colors.ENDC}")
            print(f"{Colors.HEADER}{'='*50}{Colors.ENDC}\n")
            
            for i, usuario in enumerate(usuarios, 1):
                if usuario == self.nome_usuario:
                    print(f"{Colors.OKGREEN}  👉 {i}. {usuario}{Colors.ENDC}")
                else:
                    print(f"{Colors.OKBLUE}     {i}. {usuario}{Colors.ENDC}")
            
            print()
            
        except Exception as e:
            print(f"{Colors.FAIL}❌ Erro: {e}{Colors.ENDC}")
    
    def mostrar_historico(self):
        """Mostra histórico"""
        try:
            mensagens = self.servidor.obter_historico(limite=20)
            
            print(f"\n{Colors.HEADER}{'='*50}{Colors.ENDC}")
            print(f"{Colors.BOLD}📜 HISTÓRICO{Colors.ENDC}")
            print(f"{Colors.HEADER}{'='*50}{Colors.ENDC}\n")
            
            if not mensagens:
                print(f"{Colors.WARNING}  Vazio{Colors.ENDC}\n")
                return
            
            for msg_dict in mensagens:
                msg = Mensagem.from_dict(msg_dict)
                hora = msg.timestamp.strftime("%H:%M:%S")
                
                if msg.tipo == "sistema":
                    print(f"{Colors.OKCYAN}  [{hora}] {msg.conteudo}{Colors.ENDC}")
                else:
                    print(f"  [{hora}] {msg.remetente}: {msg.conteudo}")
            
            print()
            
        except Exception as e:
            print(f"{Colors.FAIL}❌ Erro: {e}{Colors.ENDC}")
    
    def mostrar_estatisticas(self):
        """Mostra estatísticas"""
        try:
            stats = self.servidor.obter_estatisticas()
            
            print(f"\n{Colors.HEADER}{'='*50}{Colors.ENDC}")
            print(f"{Colors.BOLD}📊 ESTATÍSTICAS{Colors.ENDC}")
            print(f"{Colors.HEADER}{'='*50}{Colors.ENDC}\n")
            
            print(f"  👥 Online: {stats['usuarios_online']}")
            print(f"  💬 Mensagens: {stats['total_mensagens']}")
            print(f"  📈 Pico: {stats['pico_usuarios']}")
            print(f"  ⏱️  Uptime: {stats['uptime_formatado']}")
            print()
            
        except Exception as e:
            print(f"{Colors.FAIL}❌ Erro: {e}{Colors.ENDC}")
    
    def processar_comando(self, texto):
        """Processa comandos"""
        comando = texto.lower().strip()
        
        if comando == "/help":
            print(HELP_MESSAGE)
            
        elif comando == "/users":
            self.listar_usuarios()
            
        elif comando == "/history":
            self.mostrar_historico()
            
        elif comando == "/stats":
            self.mostrar_estatisticas()
            
        elif comando == "/clear":
            os.system('clear' if os.name == 'posix' else 'cls')
            print(WELCOME_MESSAGE)
            print(f"{Colors.OKGREEN}✅ Conectado: {self.nome_usuario}{Colors.ENDC}\n")
            
        elif comando == "/quit" or comando == "/exit":
            print(f"\n{Colors.OKCYAN}👋 Saindo...{Colors.ENDC}")
            self.desconectar()
            return False
            
        else:
            print(f"{Colors.FAIL}❌ Comando desconhecido{Colors.ENDC}")
            print(f"{Colors.WARNING}💡 Use /help{Colors.ENDC}")
        
        return True
    
    def loop_principal(self):
        """Loop principal do chat"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(WELCOME_MESSAGE)
        print(f"{Colors.OKGREEN}✅ Conectado: {Colors.BOLD}{self.nome_usuario}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}💡 /help para comandos{Colors.ENDC}\n")
        
        self.rodando = True
        
        thread = threading.Thread(target=self.receber_mensagens, daemon=True)
        thread.start()
        
        try:
            while self.rodando:
                try:
                    texto = input(f"{Colors.BOLD}{self.nome_usuario}>{Colors.ENDC} ").strip()
                    
                    if not texto:
                        continue
                    
                    if texto.startswith('/'):
                        if not self.processar_comando(texto):
                            break
                    else:
                        self.enviar_mensagem(texto)
                
                except KeyboardInterrupt:
                    print(f"\n\n{Colors.WARNING}⚠️  Interrompido{Colors.ENDC}")
                    break
                except EOFError:
                    print(f"\n\n{Colors.WARNING}⚠️  EOF{Colors.ENDC}")
                    break
                    
        finally:
            self.desconectar()
    
    def desconectar(self):
        """Desconecta"""
        if self.rodando:
            self.rodando = False
            
            try:
                if self.servidor and self.nome_usuario:
                    self.servidor.desconectar_usuario(self.nome_usuario)
                    print(f"{Colors.OKCYAN}👋 Desconectado{Colors.ENDC}")
            except:
                pass
    
    def iniciar(self):
        """Inicia cliente"""
        print("\n" + "="*60)
        print(f"{Colors.HEADER}{Colors.BOLD}💬 CLIENTE DO CHAT{Colors.ENDC}")
        print("="*60 + "\n")
        
        if not self.conectar():
            return
        
        if not self.registrar():
            return
        
        self.loop_principal()


def main():
    """Ponto de entrada"""
    cliente = ChatClient()
    
    try:
        cliente.iniciar()
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ Erro: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
    finally:
        print(f"\n{Colors.OKGREEN}✅ Encerrado{Colors.ENDC}\n")


if __name__ == "__main__":
    main()

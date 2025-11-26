"""
Launcher Universal - Inicia todo o sistema
Funciona em Windows, Linux e Mac
"""

import subprocess
import sys
import time
import os


class Colors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_success(text):
    print(f"{Colors.OKGREEN}✅ {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")


def print_info(text):
    print(f"{Colors.WARNING}ℹ️  {text}{Colors.ENDC}")


def check_dependencies():
    """Verifica Pyro4"""
    try:
        import Pyro4
        print_success("Pyro4 instalado")
        return True
    except ImportError:
        print_error("Pyro4 não encontrado")
        print_info("Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True


def start_nameserver():
    """Inicia Name Server"""
    print_info("Iniciando Name Server...")
    
    if sys.platform == "win32":
        process = subprocess.Popen(
            [sys.executable, "-m", "Pyro4.naming"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        process = subprocess.Popen(
            [sys.executable, "-m", "Pyro4.naming"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    time.sleep(2)
    
    if process.poll() is None:
        print_success("Name Server OK")
        return process
    else:
        print_error("Falha no Name Server")
        return None


def start_server():
    """Inicia Servidor"""
    print_info("Iniciando Servidor...")
    
    if sys.platform == "win32":
        process = subprocess.Popen(
            [sys.executable, "-m", "server.start_server"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        process = subprocess.Popen(
            [sys.executable, "-m", "server.start_server"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    
    time.sleep(2)
    
    if process.poll() is None:
        print_success("Servidor OK")
        return process
    else:
        print_error("Falha no Servidor")
        return None


def start_client(num):
    """Inicia Cliente"""
    print_info(f"Iniciando Cliente {num}...")
    
    if sys.platform == "win32":
        process = subprocess.Popen(
            [sys.executable, "-m", "client.start_client"],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        # Tenta terminais comuns no Linux/Mac
        terminals = ['gnome-terminal', 'xterm', 'konsole']
        for terminal in terminals:
            try:
                if terminal == 'gnome-terminal':
                    process = subprocess.Popen([
                        terminal, '--', 'python3', '-m', 'client.start_client'
                    ])
                else:
                    process = subprocess.Popen([
                        terminal, '-e', 'python3 -m client.start_client'
                    ])
                time.sleep(1)
                return process
            except FileNotFoundError:
                continue
        
        # Fallback
        print_info("Nenhum terminal gráfico, usando atual")
        process = subprocess.Popen([sys.executable, "-m", "client.start_client"])
    
    time.sleep(1)
    return process


def main():
    """Função principal"""
    print_header("LAUNCHER DO CHAT DISTRIBUÍDO")
    
    # Verifica dependências
    if not check_dependencies():
        return
    
    processes = []
    
    try:
        # Name Server
        ns = start_nameserver()
        if ns:
            processes.append(ns)
        else:
            print_error("Impossível iniciar Name Server")
            return
        
        # Servidor
        server = start_server()
        if server:
            processes.append(server)
        else:
            print_error("Impossível iniciar Servidor")
            return
        
        # Menu
        print_header("SISTEMA INICIADO")
        print(f"{Colors.BOLD}Opções:{Colors.ENDC}")
        print("1. Iniciar Cliente")
        print("2. Iniciar Múltiplos Clientes")
        print("3. Encerrar")
        
        client_count = 0
        
        while True:
            choice = input(f"\n{Colors.WARNING}>{Colors.ENDC} ").strip()
            
            if choice == "1":
                client_count += 1
                client = start_client(client_count)
                processes.append(client)
                print_success(f"Cliente {client_count} iniciado")
                
            elif choice == "2":
                num = input("Quantos? ").strip()
                try:
                    num = int(num)
                    for i in range(num):
                        client_count += 1
                        client = start_client(client_count)
                        processes.append(client)
                        time.sleep(0.5)
                    print_success(f"{num} clientes iniciados")
                except ValueError:
                    print_error("Número inválido")
                    
            elif choice == "3":
                break
            else:
                print_error("Opção inválida")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido")
    
    finally:
        print_info("Encerrando processos...")
        for p in processes:
            try:
                p.terminate()
                p.wait(timeout=3)
            except:
                try:
                    p.kill()
                except:
                    pass
        print_success("Encerrado")


if __name__ == "__main__":
    main()

import socket
import time

addr = ('localhost', 9051)
nickname = input("Digite seu nickname: ")

def connection_try(client_socket, address):
    try:
        client_socket.connect(address)
    except Exception as e:
        if e:
            print(e)
            print("Tentando conexão novamente...")
            time.sleep(5)
            connection_try(client_socket, address)

def client_wrap():
    def create_client(address):
        print("Cliente iniciado. Conectando ao servidor...")
        try:
            client_socket.connect(address)
        except:
            connection_try(client_socket, addr)
        print("Cliente conectado.")
        return

    client_socket = socket.socket()
    create_client(addr)

    def send_message(address, client_socket):
        try:
            message = input("Mensagem: ")
            client_socket.sendall(message.encode("UTF-8"))
        except socket.error as e:
            print("Erro no socket: %s" %str(e))
        except Exception as e:
            print("Exceção: %s" %str(e))

    while True:
        send_message(addr, client_socket)

client_wrap()
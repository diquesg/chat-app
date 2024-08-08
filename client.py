import socket

addr = ('localhost', 9051)

def client_wrap():
    def create_client(address):
        print("Cliente iniciado. Conectando ao servidor...")
        try:
            client_socket.connect(address)
        except Exception as e:
            print(e)
            exit()
        print("Cliente conectado.")
        return

    client_socket = socket.socket()
    create_client(addr)

    def client(address, client_socket):
        try:
            message = (input("Digite a mensagem a ser enviada: "))
            client_socket.sendall(message.encode("UTF-8"))
            print("Mensagem enviada.")
        except socket.error as e:
            print("Erro no socket: %s" %str(e))
        except Exception as e:
            print("Exceção: %s" %str(e))

    while True:
        client(addr, client_socket)

client_wrap()
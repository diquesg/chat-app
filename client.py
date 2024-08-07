import socket

addr = ('localhost', 9051)

def client(address):
    client_socket = socket.socket()
    print("Cliente criado. Conectando ao servidor...")
    try:
        client_socket.connect(address)
    except Exception as e:
        print(e)
        exit()
    print("Cliente conectado.")
    try:
        message = (input("Digite a mensagem a ser enviada: "))
        print("Enviando mensagem...")
        client_socket.sendall(message.encode("UTF-8"))
        print("Mensagem enviada.")
    except socket.error as e:
        print("Erro no socket: %s" %str(e))
    except Exception as e:
        print("Exceção: %s" %str(e))

client(addr)
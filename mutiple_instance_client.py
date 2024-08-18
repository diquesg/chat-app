import socket
import time
import threading
import sys

addr = ('localhost', 6322)
nickname = input("Nickname: ")

def connection_try(client_socket, address):
    try:
        client_socket.connect(address)
    except Exception as e:
        if e:
            print(e)
            print("Tentando conexão novamente...")
            time.sleep(5)
            connection_try(client_socket, address)

def client_wrap(address):
    def create_client(address):
        print("Cliente iniciado. Conectando ao servidor...")
        try:
            client_socket.connect(address)
        except:
            connection_try(client_socket, address)
        print("Cliente conectado.")

    client_socket = socket.socket() # Criação do cliente
    create_client(addr)
    client_socket.sendall(nickname.encode('utf-8'))

    def send_message(address, client_socket):
        try:
            while True:
                message = input("Mensagem: ")
                client_socket.sendall(message.encode("UTF-8"))
        except socket.error as e:
            print("Erro no socket: %s" % str(e))
        except Exception as e:
            print("Exceção: %s" % str(e))

    def receive_message():
        while True:
            try:
                message = client_socket.recv(2048).decode("UTF-8")
                if message:
                    # Move o cursor para a próxima linha e exibe a mensagem recebida
                    sys.stdout.write('\r' + ' ' * len(input_prompt) + '\r')
                    print(message)
                    # Reimprime o prompt de entrada para o usuário continuar digitando
                    sys.stdout.write(input_prompt)
                    sys.stdout.flush()
                else:
                    break
            except Exception as e:
                print(f"Erro ao receber mensagem: {e}")
                break

    # Define o prompt de entrada
    input_prompt = "Mensagem: "

    # Inicia a thread para receber mensagens
    rcv_message = threading.Thread(target=receive_message, daemon=True)
    rcv_message.start()

    # Loop de envio de mensagens
    send_message(addr, client_socket)


if __name__ == "__main__":
    client_wrap(addr)

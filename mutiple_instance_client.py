import socket
import threading
import sys
import time

addr = ('localhost', 9051)
nickname = input("Nickname: ")

def connection_try(client_socket, address):
    while True:
        try:
            client_socket.connect(address)
            break
        except Exception as e:
            print(f"Erro: {e}")
            print("Tentando conexão novamente...")
            time.sleep(5)

def client_wrap(address):
    def create_client(address):
        print("Cliente iniciado. Conectando ao servidor...")
        connection_try(client_socket, address)
        print("Cliente conectado.")
        client_socket.sendall(nickname.encode('utf-8'))

    client_socket = socket.socket()  # Criação do cliente
    create_client(addr)

    def send_message():
        while True:
            try:
                message = input(prompt)  # Exibe o prompt e lê a entrada
                if message.strip():  # Envia a mensagem somente se não estiver vazia
                    client_socket.sendall(message.encode("UTF-8"))
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
                break

    def receive_message():
        while True:
            try:
                message = client_socket.recv(2048).decode("UTF-8")
                if message:
                    print(message)
            except Exception as e:
                print(f"Erro ao receber mensagem: {e}")
                break

    def handle_received_message(message):
        sys.stdout.write('\r' + ' ' * (len(prompt) + 80) + '\r')  # Limpa a linha do prompt anterior
        sys.stdout.write(f"{message}\n")  # Imprime a mensagem recebida
        sys.stdout.write(prompt)  # Reimprime o prompt
        sys.stdout.flush()

    # Define o prompt de entrada
    prompt = "Mensagem: "
    sys.stdout.write(prompt)
    sys.stdout.flush()

    # Inicia a thread para receber mensagens
    rcv_message = threading.Thread(target=receive_message, daemon=True)
    rcv_message.start()

    # Loop de envio de mensagens
    send_message()

if __name__ == "__main__":
    client_wrap(addr)

import socket
import threading

addr = ("localhost", 6322)
data_limit = 2048

print("Criando servidor...")

server_socket = socket.create_server(addr)  # Cria um novo socket de servidor definido como "server_socket"
server_socket.listen()  # Coloca o servidor em estado de espera por solicitações
print("Servidor criado. Aguardando conexões...")

clientes_conectados = {}

def client_handler(client_socket, client_address, nickname):  # Lida com mensagens do cliente e transmite para os outros clientes
    while True:
        try:
            message = client_socket.recv(data_limit).decode("UTF-8")  # Recebe a mensagem
            if message:
                print(f"Mensagem de {nickname}: {message}")
            else:
                break
            server_broadcast(message, client_socket, nickname)
        except Exception:
            break
    try: # Remove o cliente da lista e fecha o socket
        del clientes_conectados[client_socket]
        client_socket.close()
    except ValueError:
        pass
    disconnected = nickname+" se desconectou."
    disconnected_message(disconnected)

def server_broadcast(message, sender_socket, nickname):
    for cliente in list(clientes_conectados):  # Criar uma cópia da lista para evitar modificação durante a iteração
        if cliente != sender_socket:
            try:
                formatted_message = f"{nickname}: {message}"
                cliente.sendall(formatted_message.encode("UTF-8"))
                print("Mensagem transmitida.")
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
                try:
                    cliente.close()
                    clientes_conectados.remove(cliente)
                except ValueError:
                    pass

def disconnected_message(message):
    for cliente in list(clientes_conectados):  # Criar uma cópia da lista para evitar modificação durante a iteração
            try:
                cliente.sendall(message.encode("UTF-8"))
                print("Mensagem transmitida.")
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
                try:
                    cliente.close()
                    clientes_conectados.remove(cliente)
                except ValueError:
                    pass

def server_run():
    while True:
        client_socket, client_address = server_socket.accept()  # Aceita conexões de clientes
        nickname = client_socket.recv(data_limit).decode('utf-8')
        clientes_conectados[client_socket] = nickname
        print(f"Nova conexão de {nickname}")
        client_thread = threading.Thread(target=client_handler, args=(client_socket, client_address, nickname))
        client_thread.start()

server_run()

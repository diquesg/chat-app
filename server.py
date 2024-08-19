import socket
import threading

addr = ('localhost', 9051)
data_limit = 2048

print("Criando servidor...")

server_socket = socket.create_server(addr)  # Cria um novo socket de servidor
server_socket.listen()  # Coloca o servidor em estado de espera por solicitações
print("Servidor criado. Aguardando conexões...")

clientes_conectados = []

def get_client_list():
    # Retorna a lista de nicknames dos clientes conectados
    return [nickname for _, nickname in clientes_conectados]

def client_handler(client_socket, nickname):  # Lida com mensagens do cliente e transmite para os outros clientes
    global clientes_conectados  # Declara clientes_conectados como global

    # Envia a lista de clientes para o novo cliente
    def connected_list():
        cliente_list = ', '.join(get_client_list())
        client_socket.sendall(f"Clientes no chat: {cliente_list}".encode("UTF-8"))
    
    connected_list()

    while True:
        try:
            message = client_socket.recv(data_limit).decode("UTF-8")  # Recebe a mensagem
            if message:
                print(f"{nickname}: {message}")
                server_broadcast(f"{nickname}: {message}", client_socket)
            else:
                break
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            break

    try:
        clientes_conectados.remove((client_socket, nickname))
        client_socket.close()
        server_broadcast(f"{nickname} saiu do chat.", client_socket)  # Envia mensagem de saída para todos os clientes
    except ValueError:
        pass
    print(f"Conexão com {nickname} encerrada.")

def server_broadcast(message, sender_socket):
    global clientes_conectados  # Declara clientes_conectados como global
    for cliente_socket, _ in list(clientes_conectados):
        if cliente_socket != sender_socket:
            try:
                cliente_socket.sendall(message.encode("UTF-8"))
                print("Mensagem transmitida.")
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
                try:
                    cliente_socket.close()
                    clientes_conectados = [(cs, nn) for cs, nn in clientes_conectados if cs != cliente_socket]
                except ValueError:
                    pass

def server_run():
    while True:
        client_socket, client_address = server_socket.accept()  # Aceita conexões de clientes
        nickname = client_socket.recv(data_limit).decode("UTF-8")  # Recebe o nickname
        print(f"Nova conexão de {nickname}")
        clientes_conectados.append((client_socket, nickname))  # Adiciona o novo cliente à lista de conexões
        client_thread = threading.Thread(target=client_handler, args=(client_socket, nickname))
        client_thread.start()

server_run()

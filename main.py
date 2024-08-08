import socket
import threading

address = ('localhost', 9051)

data_limit = 2048
print("Criando servidor...")
server_socket = socket.socket() #Cria um novo socket definido como "server_socket"
server_socket.bind(address) #Associa o socket ao endereço do serviddor
server_socket.listen() #Coloca o servidor em estado de espera por solicitações
print("Servidor criado. Aguardando solicitações...")

def client_handler(client_socket):
    while True:
        try:
            message = client_socket.recv(data_limit).decode("UTF-8")
            if message:
                print(message)
            else:
                break
        except Exception as e:
            print(e)
            break
    client_socket.close()

while True:
    client_socket, client_address = server_socket.accept() #Aceita conexões de clientes, retornando o endereço da solicitação
    print("Nova conexão")
    client_thread = threading.Thread(target=client_handler(client_socket))
    client_thread.start()
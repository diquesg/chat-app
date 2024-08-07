import socket

addr = ('localhost', 9051)

def server(address):
    data_limit = 2048
    print("Criando servidor...")
    server_socket = socket.socket() #Cria um novo socket definido como "server"
    server_socket.bind(address) #Associa o socket ao endereço do serviddor
    server_socket.listen() #Coloca o servidor em estado de espera por solicitações
    print("Servidor criado. Aguardando solicitações...")
    client, address = server_socket.accept() #Aceita conexões de clientes, retornando o endereço da solicitação
    message = client.recv(data_limit)
    print("Mensagem: " + message.decode("UTF-8"))
    print("Endereço: " + str(address))

server(addr)

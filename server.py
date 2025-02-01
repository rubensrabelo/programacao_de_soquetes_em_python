import socket


def run_server():
    # Cria um objeto socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    port = 8000

    # Vincula o socket para um especifico endereco e porta
    server.bind(server_ip, port)

    # Escuta as conexões recebidas
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")

    # Aceitar conexoes de entrada
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # Recebe dados do cliente
    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8")  # Converte bytes para string

        # Se recebemos "close" do client, entao saimos do loop
        # e fechamos a conexao
        if request.lower() == "close":
            # Envia resposta ao cliente que reconhece
            # que a conexão deve ser fechada e sair do loop
            client_socket.send("closed".encode("utf-8"))
            break
        print(f"Received: {request}")
        response = "accepted".encode("utf-8")
        # Converte e envia a resposta de aceitação ao cliente 
        client_socket.send(response)

    # Fecha o socket com o client
    client_socket.close()
    print("Connection to client closed")
    server.close()


run_server()

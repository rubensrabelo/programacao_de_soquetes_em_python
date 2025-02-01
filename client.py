import socket


def run_client():
    # Cria um objeto socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    port = 8000

    # Estabelecendo conexão com o servidor
    client.connect((server_ip, port))

    while True:
        # Insere a mensagem e envia ao servidor
        msg = input("Enter a message: ")
        client.send(msg.encode("utf-8")[:1024])

        response = client.recv(1024)
        response = response.decode("utf-8")

        if response.lower() == "closed":
            break

        print(f"Received: {response}")

    client.close()
    print("Connection to server closed")


if __name__ == "__main__":
    run_client()

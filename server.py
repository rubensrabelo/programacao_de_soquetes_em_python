import socket
import threading
import pandas as pd
import bcrypt
import os

USERS_FILE = "users.csv"

if not os.path.exists(USERS_FILE):
    df = pd.DataFrame(columns=["email", "password"])
    df.to_csv(USERS_FILE, index=False)


def hash_password(password):
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
        ).decode("utf-8")


def check_password(email, password):
    df = pd.read_csv(USERS_FILE)
    user = df[df["email"] == email]
    if not user.empty:
        stored_hash = user["password"].values[0]
        return bcrypt.checkpw(password.encode("utf-8"),
                              stored_hash.encode("utf-8"))
    return False


def handle_client(client_socket, addr):
    try:
        while True:
            # Recebe e tranforma em string a mensagem do cliente
            request = client_socket.recv(1024).decode("utf-8")
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break
            print(f"Received: {request}")

            # converte e envia resposta de aceitação ao cliente
            response = "accepted"
            client_socket.send(response.encode("utf-8"))
    except Exception as e:
        print(f"Error when handling client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


def run_server():
    server_ip = "127.0.0.1"
    port = 8000

    try:
        # Cria um objeto socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Vincula o socket para um especifico endereco e porta
        server.bind((server_ip, port))

        # Escuta as conexões recebidas
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        # Recebe dados do cliente
        while True:
            # Aceitar conexoes de entrada
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")

            thread = threading.Thread(target=handle_client, args=(
                client_socket,
                addr,
            ))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


if __name__ == "__main__":
    run_server()

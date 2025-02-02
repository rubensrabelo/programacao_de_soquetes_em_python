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


def register_user(email, password):
    if check_user_exists(email):
        return False
    hashed_password = hash_password(password)
    with open(USERS_FILE, "a", newline="", encoding="utf-8") as file:
        file.write(f"{email},{hashed_password}\n")
    return True


def check_user_exists(email):
    df = pd.read_csv(USERS_FILE)
    return email in df["email"].values


def handle_client(client_socket, addr):
    try:
        client_socket.send("Do you have an account? (yes/no): "
                           .encode("utf-8"))
        choice = client_socket.recv(1024).decode("utf-8").strip().lower()

        if choice == "no":
            client_socket.send("Enter email: ".encode("utf-8"))
            email = (client_socket.recv(1024).decode("utf-8")
                     .strip().lower())
            client_socket.send("Enter password: ".encode("utf-8"))
            password = client_socket.recv(1024).decode("utf-8").strip()

            if register_user(email, password):
                client_socket.send("Registration successful! Please log in."
                                   .encode("utf-8"))
            else:
                client_socket.send("Email already registered. Try logging in."
                                   .encode("utf-8"))
                client_socket.close()
                return

        client_socket.send("Enter email: ".encode("utf-8"))
        email = client_socket.recv(1024).decode("utf-8").strip()
        client_socket.send("Enter password: ".encode("utf-8"))
        password = client_socket.recv(1024).decode("utf-8").strip()

        if check_password(email, password):
            client_socket.send("authenticated".encode("utf-8"))
        else:
            client_socket.send("denied".encode("utf-8"))
            client_socket.close()
            return

        while True:
            request = client_socket.recv(1024).decode("utf-8")
            print(request)
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break
            print(f"Received from {email}: {request}")

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
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((server_ip, port))
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
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

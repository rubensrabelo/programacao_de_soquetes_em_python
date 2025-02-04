import socket
import threading
from services.handle_client import HandleClient
from services.user_manager import UserManager
from services.financial_manager import FinancialManager


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

            handle_client = HandleClient(
                client_socket,
                addr,
                UserManager(),
                FinancialManager(),
                user_id=None
                )
            thread = threading.Thread(target=handle_client.handle_client)
            thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


if __name__ == "__main__":
    run_server()

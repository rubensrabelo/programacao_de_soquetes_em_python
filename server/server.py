import socket
import threading
from services.handle_client import HandleClient
from services.user_manager import UserManager
from services.financial_manager import FinancialManager


def broadcast_listener(port=8000):
    """ Responde às requisições de descoberta de clientes """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(("", port))

        while True:
            data, addr = s.recvfrom(1024)
            if data == b"DISCOVERY_REQUEST":
                s.sendto(b"DISCOVERY_RESPONSE", addr)


def run_server():
    server_ip = "0.0.0.0"  # Aceita conexões de qualquer IP na rede local
    port = 8000

    # Inicia a thread para responder ao discovery dos clientes
    threading.Thread(target=broadcast_listener, daemon=True).start()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((server_ip, port))
            server.listen()
            print(f"Listening on {server_ip}:{port}")

            while True:
                client_socket, addr = server.accept()
                print(f"Accepted connection from {addr[0]}:{addr[1]}")

                try:
                    client_ip = client_socket.recv(1024).decode("utf-8")
                    print(f"Client's local IP: {client_ip}")
                except Exception as e:
                    print(f"Failed to receive client IP: {e}")

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


if __name__ == "__main__":
    run_server()

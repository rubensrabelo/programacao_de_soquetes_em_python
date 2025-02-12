import socket
from screen.display import Display


def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        print(f"Could not determine local IP: {e}")
        return "Unknown"


def discover_server_ip(port=8000):
    print("Searching for the server on the network...")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.settimeout(3)

        try:
            s.sendto(b"DISCOVERY_REQUEST", ("255.255.255.255", port))
            data, addr = s.recvfrom(1024)  # Aguarda resposta do servidor
            return addr[0]  # Retorna o IP do servidor que respondeu
        except socket.timeout:
            print("No response from server.")
            return None


def connect_to_server():
    server_ip = discover_server_ip()

    if not server_ip:
        server_ip = input("Enter the server IP: ").strip()

    port = 8000
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((server_ip, port))
        print(f"Connected to the server at {server_ip}:{port}")

        # Obtém o IP local correto e envia ao servidor
        client_ip = get_local_ip()
        client.send(client_ip.encode("utf-8"))

        return client
    except Exception as e:
        print(f"Error connecting to server: {e}")
        return None


def run_client():
    try:
        while True:
            client = connect_to_server()
            if not client:
                retry = input("Connection failed. Try again? (yes/no): ").strip().lower()
                if retry != "yes":
                    return
                continue  # Volta para tentar de novo

            retry_choice = "no"
            register_success = True
            display = Display(client)

            while True:
                response = client.recv(1024).decode("utf-8")
                print(response)
                choice = input(">> ")
                client.send(choice.encode("utf-8"))

                if choice.lower() == "no":
                    register_success = display.handle_registration()
                    if not register_success:
                        break

                if display.handle_login():
                    break

                retry_choice = input("Login failed. Do you want to try again? (yes/no): ").strip()
                if retry_choice.lower() != "yes":
                    client.close()
                    return

                print("Reconnecting...")
                client.close()
                break

            if retry_choice.lower() == "yes" or not register_success:
                continue

            if client:
                display.interact_with_server()
                client.close()
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if "client" in locals() and client:
            client.close()
            print("Connection to server closed")


if __name__ == "__main__":
    run_client()

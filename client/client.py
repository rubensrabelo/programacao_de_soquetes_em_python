import socket
from screen.display import Display


def get_local_ip():
    """ Obtém o IP local correto da rede (não 127.0.0.1) """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Conexão temporária para determinar o IP local
            return s.getsockname()[0]
    except Exception as e:
        print(f"Could not determine local IP: {e}")
        return "Unknown"


def connect_to_server(server_ip="127.0.0.1", port=8000):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))
    
    # Obtém o IP local correto e envia ao servidor
    client_ip = get_local_ip()
    client.send(client_ip.encode("utf-8"))
    
    return client


def run_client():
    try:
        while True:
            client = connect_to_server()
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
        if "client" in locals():
            client.close()
            print("Connection to server closed")


if __name__ == "__main__":
    run_client()

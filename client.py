import socket


def run_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = "127.0.0.1"
    port = 8000

    client.connect((server_ip, port))

    try:
        response = client.recv(1024).decode("utf-8")
        print(response)
        choice = input(">> ")
        client.send(choice.encode("utf-8"))

        if choice.lower() == "no":
            response = client.recv(1024).decode("utf-8")
            print(response)
            email = input(">> ")
            client.send(email.encode("utf-8"))

            response = client.recv(1024).decode("utf-8")
            print(response)
            password = input(">> ")
            client.send(password.encode("utf-8"))

            response = client.recv(1024).decode("utf-8")
            print(response)

        response = client.recv(1024).decode("utf-8")
        print(response)
        email = input(">> ")
        client.send(email.encode("utf-8"))

        response = client.recv(1024).decode("utf-8")
        print(response)
        password = input(">> ")
        client.send(password.encode("utf-8"))

        auth_response = client.recv(1024).decode("utf-8")
        if auth_response == "denied":
            print("Login failed. Closing connection.")
            client.close()
            return

        print("Login successful!")

        while True:
            msg = input("Enter a message: ")
            client.send(msg.encode("utf-8")[:1024])

            response = client.recv(1024)
            response = response.decode("utf-8")

            if not response:
                print("SServer did not respond")
                break

            if response.lower() == "closed":
                break

            print(f"Received: {response}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if "server" in locals():
            client.close()
            print("Connection to server closed")


if __name__ == "__main__":
    run_client()

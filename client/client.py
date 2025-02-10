import socket


def connect_to_server(server_ip="127.0.0.1", port=8000):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))
    return client


def handle_registration(client):
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


def handle_login(client):
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
        return False

    print("Login successful!")
    return True


def interact_with_server(client):
    while True:
        text = """Enter one of the options: [1] 'Financial' or [2] 'Exit'"""
        print(text)
        choice = input(">> ")
        client.send(choice.encode("utf-8")[:1024])

        response = client.recv(1024).decode("utf-8")

        if not response:
            print("Server did not respond")
            break

        if choice == "1":
            handle_financial_manager(client)
        elif choice == "2":
            print("Exiting...")
            break
        else:
            print("Invalid option. Try again.")

        # print(f"Received: {response}")


def handle_financial_manager(client):
    while True:
        response = client.recv(1024).decode("utf-8")
        if "Choose an option" in response:
            print(response)
            choice = input(">> ")
            client.send(choice.encode("utf-8"))

            if choice.lower() == "add":
                handle_add_transaction(client)
            elif choice.lower() == "edit":
                handle_update_transaction(client)
            elif choice.lower() == "remove":
                handle_remove_transaction(client)
            elif choice.lower() == "view":
                handle_view_today_transaction(client)
            elif choice.lower() == "calculate":
                handle_calculate_installment(client)
            elif choice.lower() == "close":
                print("Closing connection...")
                break
            else:
                print("Invalid option. Try again.\n")


def handle_add_transaction(client):
    response = client.recv(1024).decode("utf-8")
    print(response)
    tr_flow = input(">> ")
    client.send(tr_flow.encode("utf-8"))

    response = client.recv(1024).decode("utf-8")
    print(response)
    category = input(">> ")
    client.send(category.encode("utf-8"))

    response = client.recv(1024).decode("utf-8")
    print(response)
    value = input(">> ")
    client.send(value.encode("utf-8"))

    response = client.recv(1024).decode("utf-8")
    print(response)


def handle_update_transaction(client):
    response = client.recv(1024).decode("utf-8")
    print(response)
    id_data = input(">> ")
    client.send(id_data.encode("utf-8"))

    response = client.recv(1024).decode("utf-8")
    print(response)
    tr_flow = input(">> ")
    client.send(tr_flow.encode("utf-8"))

    response = client.recv(1024).decode("utf-8")
    print(response)
    category = input(">> ")
    client.send(category.encode("utf-8"))

    response = client.recv(1024).decode("utf-8")
    print(response)
    value = input(">> ")
    client.send(value.encode("utf-8"))

    response = client.recv(1024).decode("utf-8")
    print(response)


def handle_remove_transaction(client):
    response = client.recv(1024).decode("utf-8")
    print(response)
    id_data = input(">> ")
    client.send(id_data.encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    print(response)


def handle_view_today_transaction(client):
    client.send("today_transactions".encode("utf-8"))
    response = client.recv(4096).decode("utf-8")

    if response == "No transactions found for today.":
        print(response)
    else:
        transactions = response.split("\n")
        print("\n".join(transactions))


def handle_calculate_installment(client):
    response = client.recv(1024).decode("utf-8")
    print(response)

    response = client.recv(1024).decode("utf-8")
    print(response)

    num_installments = input(">> ")
    client.send(num_installments.encode("utf-8"))

    response = client.recv(4096).decode("utf-8")
    print(response)


def run_client():
    # server_ip = "127.0.0.1"
    # port = 8000
    try:
        while True:
            client = connect_to_server()
            retry_choice = "no"
            register_success = True

            while True:
                response = client.recv(1024).decode("utf-8")
                print(response)
                choice = input(">> ")
                client.send(choice.encode("utf-8"))

                if choice.lower() == "no":
                    register_success = handle_registration(client)
                    if not register_success:
                        break

                if handle_login(client):
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
                interact_with_server(client)
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

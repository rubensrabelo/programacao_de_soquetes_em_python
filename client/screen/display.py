class Display:
    def __init__(self, client):
        self.client = client

    def handle_registration(self):
        response = self.client.recv(1024).decode("utf-8")
        print(response)
        email = input(">> ")
        self.client.send(email.encode("utf-8"))

        response = self.client.recv(1024).decode("utf-8")
        print(response)
        password = input(">> ")
        self.client.send(password.encode("utf-8"))

        response = self.client.recv(1024).decode("utf-8")
        print(response)

    def handle_login(self):
        response = self.client.recv(1024).decode("utf-8")
        print(response)
        email = input(">> ")
        self.client.send(email.encode("utf-8"))

        response = self.client.recv(1024).decode("utf-8")
        print(response)
        password = input(">> ")
        self.client.send(password.encode("utf-8"))

        auth_response = self.client.recv(1024).decode("utf-8")
        if auth_response == "denied":
            print("Login failed. Closing connection.")
            self.client.close()
            return False

        print("Login successful!")
        return True

    def interact_with_server(self):
        while True:
            print("Enter one of the options: [1] 'Financial' or [2] 'Exit'")
            choice = input(">> ")
            self.client.send(choice.encode("utf-8")[:1024])

            response = self.client.recv(1024).decode("utf-8")

            if not response:
                print("Server did not respond")
                break

            if choice == "1":
                self.handle_financial_manager()
            elif choice == "2":
                print("Exiting...")
                return
            else:
                print("Invalid option. Try again.")

    def handle_financial_manager(self):
        while True:
            response = self.client.recv(1024).decode("utf-8")
            if "Choose an option" in response:
                print(response)
                choice = input(">> ")
                self.client.send(choice.encode("utf-8"))

                if choice.lower() == "add":
                    self.handle_add_transaction()
                elif choice.lower() == "edit":
                    self.handle_update_transaction()
                elif choice.lower() == "remove":
                    self.handle_remove_transaction()
                elif choice.lower() == "view":
                    self.handle_view_today_transaction()
                elif choice.lower() == "calculate":
                    self.handle_calculate_installment()
                elif choice.lower() == "close":
                    print("Closing connection...")
                    return
                else:
                    print("Invalid option. Try again.\n")

    def handle_add_transaction(self):
        response = self.client.recv(1024).decode("utf-8")
        print(response)
        tr_flow = input(">> ")
        self.client.send(tr_flow.encode("utf-8"))

        response = self.client.recv(1024).decode("utf-8")
        print(response)
        category = input(">> ")
        self.client.send(category.encode("utf-8"))

        response = self.client.recv(1024).decode("utf-8")
        print(response)
        value = input(">> ")
        self.client.send(value.encode("utf-8"))

        response = self.client.recv(1024).decode("utf-8")
        print(response)

    def handle_update_transaction(self):
        response = self.client.recv(1024).decode("utf-8")
        print(response)
        id_data = input(">> ")
        self.client.send(id_data.encode("utf-8"))

        response = self.client.recv(1024).decode("utf-8")
        print(response)
        tr_flow = input(">> ")
        self.client.send(tr_flow.encode("utf-8"))

        response = self.client.recv(1024).decode("utf-8")
        print(response)
        category = input(">> ")
        self.client.send(category.encode("utf-8"))

        response = self.client.recv(1024).decode("utf-8")
        print(response)
        value = input(">> ")
        self.client.send(value.encode("utf-8"))

        response = self.client.recv(1024).decode("utf-8")
        print(response)

    def handle_remove_transaction(self):
        response = self.client.recv(1024).decode("utf-8")
        print(response)
        id_data = input(">> ")
        self.client.send(id_data.encode("utf-8"))
        response = self.client.recv(1024).decode("utf-8")
        print(response)

    def handle_view_today_transaction(self):
        response = self.client.recv(4096).decode("utf-8")
        print(response)

        response = self.client.recv(4096).decode("utf-8")
        if response == "No transactions found for today.":
            print(response)
        else:
            transactions = response.split("\n")
            print("\n".join(transactions))

    def handle_calculate_installment(self):
        response = self.client.recv(1024).decode("utf-8")
        print(response)

        response = self.client.recv(1024).decode("utf-8")
        print(response)

        num_installments = input(">> ")
        self.client.send(num_installments.encode("utf-8"))

        response = self.client.recv(4096).decode("utf-8")
        print(response)

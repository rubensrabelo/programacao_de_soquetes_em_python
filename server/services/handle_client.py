class HandleClient:
    def __init__(
            self,
            client_socket,
            addr,
            user_manager,
            financial_manager,
            user_id
            ):
        self.client_socket = client_socket
        self.addr = addr
        self.user_manager = user_manager
        self.financial_manager = financial_manager
        self.user_id = user_id

    def handle_client(self):
        try:
            self.client_socket.send("Do you have an account? (yes/no): "
                                    .encode("utf-8"))
            choice = (self.client_socket.recv(1024)
                      .decode("utf-8").strip().lower())

            if choice == "no":
                if not self.register_client():
                    return

            if not self.login_client():
                return

            while True:
                self.client_socket.send(
                    "Choose an option: [add, remove, edit, view, calculate, close]:"
                    .encode("utf-8")
                )
                request = self.client_socket.recv(1024).decode("utf-8")

                if request.lower() == "add":
                    self.add_data()
                elif request.lower() == "remove":
                    self.remove_data()
                elif request.lower() == "edit":
                    self.update_data()
                elif request.lower() == "view":
                    self.get_today_values()
                elif request.lower() == "calculate":
                    self.calculate_installment()
                elif request.lower() == "close":
                    self.client_socket.send("closed".encode("utf-8"))
                    break
                else:
                    self.client_socket.send("Invalid option. Try again."
                                            .encode("utf-8"))
                print(f"Received from client: {request}")

                response = "accepted\n"
                self.client_socket.send(response.encode("utf-8"))
        except Exception as e:
            print(f"Error when handling client: {e}")
        finally:
            self.client_socket.close()
            print(
                f"Connection to client ({self.addr[0]}:{self.addr[1]}) closed")

    def register_client(self):
        self.client_socket.send("Enter email: ".encode("utf-8"))
        email = (self.client_socket.recv(1024)
                 .decode("utf-8")
                 .strip().lower())
        self.client_socket.send("Enter password: ".encode("utf-8"))
        password = (self.client_socket.recv(1024)
                    .decode("utf-8").strip())

        if self.user_manager.register_user(email, password):
            self.client_socket.send(
                "Registration successful! Please log in."
                .encode("utf-8"))
            return True
        else:
            self.client_socket.send(
                "Email already registered. Try logging in."
                .encode("utf-8"))
            return False

    def login_client(self):
        self.client_socket.send("Enter email: ".encode("utf-8"))
        email = self.client_socket.recv(1024).decode("utf-8").strip()
        self.client_socket.send("Enter password: ".encode("utf-8"))
        password = self.client_socket.recv(1024).decode("utf-8").strip()

        user_id = self.user_manager.get_user_id(email)
        if self.user_manager.check_password(email, password):
            self.client_socket.send("authenticated".encode("utf-8"))
            self.user_id = user_id
            return True
        else:
            self.client_socket.send("denied".encode("utf-8"))
            self.client_socket.close()
            return False

    def add_data(self):
        self.client_socket.send("Enter transaction type: ".encode("utf-8"))
        tr_flow = self.client_socket.recv(1024).decode("utf-8").strip()

        self.client_socket.send("Enter category name: ".encode("utf-8"))
        category = self.client_socket.recv(1024).decode("utf-8").strip()

        self.client_socket.send("Enter value: ".encode("utf-8"))
        value = self.client_socket.recv(1024).decode("utf-8").strip()

        id_data = self.financial_manager.add_data(
            tr_flow,
            category,
            value,
            self.user_id
            )
        self.client_socket.send(f"Transaction added with ID: {id_data}"
                                .encode("utf-8"))

    def update_data(self):
        self.client_socket.send("Enter transaction ID to edit: "
                                .encode("utf-8"))
        id_data = self.client_socket.recv(1024).decode("utf-8").strip()

        self.client_socket.send(
            "Enter new transaction type (leave empty to keep current): "
            .encode("utf-8"))
        tr_flow = self.client_socket.recv(1024).decode("utf-8").strip() or None

        self.client_socket.send(
            "Enter new category (leave empty to keep current): "
            .encode("utf-8"))
        category = (
            self.client_socket.recv(1024).decode("utf-8").strip() or None
            )

        self.client_socket.send(
            "Enter new value (leave empty to keep current): "
            .encode("utf-8"))
        value = self.client_socket.recv(1024).decode("utf-8").strip()
        value = float(value) if value else None
        if self.financial_manager.update_data(int(id_data),
                                              tr_flow,
                                              category,
                                              value):
            self.client_socket.send("Transaction updated successfully."
                                    .encode("utf-8"))
        else:
            self.client_socket.send("Transaction not found."
                                    .encode("utf-8"))

    def remove_data(self):
        self.client_socket.send("Enter category ID to remove: "
                                .encode("utf-8"))
        id_data = int(self.client_socket.recv(1024).decode("utf-8").strip())

        if self.financial_manager.remove_data(id_data):
            self.client_socket.send("Transaction removed successfully."
                                    .encode("utf-8"))
        else:
            self.client_socket.send("Transaction not found.".encode("utf-8"))

    def get_today_values(self):
        self.client_socket.send("today_transactions".encode("utf-8"))

        values = self.financial_manager.get_today_values(self.user_id)
        if not values:
            self.client_socket.send(
                "No transactions found for today.\n".encode("utf-8")
                )
            return
        response = "\n".join(
            [
                f"Type: {entry['transfer_flow']}, "
                f"Category: {entry['category']}, Value: {entry['value']}"
                for entry in values
                ]
        )
        self.client_socket.send(response.encode("utf-8"))

    def calculate_installment(self):
        self.client_socket.send("Calculate Installment:".encode("utf-8"))
        self.client_socket.send(
            "Enter number of installments: ".encode("utf-8")
            )
        num_installments = (self.client_socket.recv(1024).decode("utf-8").strip())

        try:
            num_installments = int(num_installments)
        except ValueError:
            self.client_socket.send(f"Invalid number of installments. Please enter a valid integer.".encode("utf-8"))
            return

        annual_interest_rate = 0.1

        installment_details = self.financial_manager.calculate_installment(
            self.user_id,
            annual_interest_rate,
            num_installments
            )

        response = "\n".join(
            [
                f"Month: {detail['Month']}, Installments: {detail['Installments']}, "
                f"Fees: {detail['Fees']}, Amortization: {detail['Amortization']}, "
                f"Debit balance: {detail['Debit balance']}"
                for detail in installment_details
            ]
        )
        self.client_socket.send(response.encode("utf-8"))

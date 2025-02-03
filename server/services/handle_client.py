class HandleClient:
    def __init__(self, client_socket, addr, user_csv):
        self.client_socket = client_socket
        self.addr = addr
        self.user_csv = user_csv

    def handle_client(self):
        try:
            self.client_socket.send("Do you have an account? (yes/no): "
                                    .encode("utf-8"))
            choice = (self.client_socket.recv(1024)
                      .decode("utf-8").strip().lower())

            if choice == "no":
                self.client_socket.send("Enter email: ".encode("utf-8"))
                email = (self.client_socket.recv(1024)
                         .decode("utf-8")
                         .strip().lower())
                self.client_socket.send("Enter password: ".encode("utf-8"))
                password = (self.client_socket.recv(1024)
                            .decode("utf-8").strip())

                if self.user_csv.register_user(email, password):
                    self.client_socket.send(
                        "Registration successful! Please log in."
                        .encode("utf-8"))
                else:
                    self.client_socket.send(
                        "Email already registered. Try logging in."
                        .encode("utf-8"))
                    self.client_socket.close()
                    return

            self.client_socket.send("Enter email: ".encode("utf-8"))
            email = self.client_socket.recv(1024).decode("utf-8").strip()
            self.client_socket.send("Enter password: ".encode("utf-8"))
            password = self.client_socket.recv(1024).decode("utf-8").strip()

            if self.user_csv.check_password(email, password):
                self.client_socket.send("authenticated".encode("utf-8"))
            else:
                self.client_socket.send("denied".encode("utf-8"))
                self.client_socket.close()
                return

            while True:
                request = self.client_socket.recv(1024).decode("utf-8")
                print(request)
                if request.lower() == "close":
                    self.client_socket.send("closed".encode("utf-8"))
                    break
                print(f"Received from {email}: {request}")

                response = "accepted"
                self.client_socket.send(response.encode("utf-8"))
        except Exception as e:
            print(f"Error when handling client: {e}")
        finally:
            self.client_socket.close()
            print(
                f"Connection to client ({self.addr[0]}:{self.addr[1]}) closed")

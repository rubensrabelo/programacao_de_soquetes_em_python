import pandas as pd
import bcrypt
import os


class UserManager():
    USERS_FILE = "users.csv"

    def __init__(self):
        if not os.path.exists(self.USERS_FILE):
            df = pd.DataFrame(columns=["id", "email", "password"])
            df.to_csv(self.USERS_FILE, index=False)

    def hash_password(self, password):
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
            ).decode("utf-8")

    def check_password(self, email, password):
        df = pd.read_csv(self.USERS_FILE)
        user = df[df["email"] == email]
        if not user.empty:
            stored_hash = user["password"].values[0]
            return bcrypt.checkpw(password.encode("utf-8"),
                                  stored_hash.encode("utf-8"))
        return False

    def register_user(self, email, password):
        if self.check_user_exists(email):
            return False
        df = pd.read_csv(self.USERS_FILE)
        if df.empty:
            id_user = 1
        else:
            id_user = int(df["id"].max() + 1)
        hashed_password = self.hash_password(password)
        with open(self.USERS_FILE, "a", newline="", encoding="utf-8") as file:
            file.write(f"{id_user},{email},{hashed_password}\n")
        return True

    def check_user_exists(self, email):
        df = pd.read_csv(self.USERS_FILE)
        return email in df["email"].values

    def get_user_id(self, email):
        df = pd.read_csv(self.USERS_FILE)
        user = df[df["email"] == email]
        if not user.empty:
            return int(user["id"].values[0])
        return None

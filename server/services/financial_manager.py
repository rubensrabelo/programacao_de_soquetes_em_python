import pandas as pd
import os
import datetime


class FinancialManager():
    FINANCIAL_MANAGER = "financial.csv"
    COLUMNS = [
        "id", "timestamp", "transfer_flow", "category", "value", "user_id"
        ]

    def __init__(self):
        if not os.path.exists(self.FINANCIAL_MANAGER):
            df = pd.DataFrame(columns=self.COLUMNS)
            df.to_csv(self.FINANCIAL_MANAGER, index=False)

    def get_next_id(self):
        df = pd.read_csv(self.FINANCIAL_MANAGER)
        return 1 if df.empty else int(df["id"].max() + 1)

    def add_data(self, tr_flow, category, value, user_id):
        id = self.get_next_id()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = f"{id},{timestamp},{tr_flow},{category},{value},{user_id}\n"

        with open(self.FINANCIAL_MANAGER,
                  "a", newline="", encoding="utf-8") as file:
            file.write(data)
        return id

    def update_data(self, id_data, tr_flow, category, value):
        df = pd.read_csv(self.FINANCIAL_MANAGER)
        if id_data in df["id"].values:
            index = df[df["id"] == id_data].index[0]
            if tr_flow:
                df.at[index, "transfer_flow"] = tr_flow
            if category:
                df.at[index, "category"] = category
            if value is not None:
                df.at[index, "value"] = value
            df.to_csv(self.FINANCIAL_MANAGER, index=False)
            return True
        return False

    def remove_data(self, id):
        df = pd.read_csv(self.FINANCIAL_MANAGER)
        id = int(id)
        if id in df["id"].values:
            df = df[df["id"] != id]
            df.to_csv(self.FINANCIAL_MANAGER, index=False)
            return True
        return False

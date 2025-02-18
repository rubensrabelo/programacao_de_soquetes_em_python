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

    def get_today_values(self, user_id):
        if not os.path.exists(self.FINANCIAL_MANAGER):
            return []

        df = pd.read_csv(self.FINANCIAL_MANAGER)

        filtered_df = df[
            (df["user_id"] == user_id)
            ]

        filtered_df = filtered_df.loc[:,
                                      [
                                          "id",
                                          "transfer_flow",
                                          "category",
                                          "value"
                                          ]
                                      ].to_dict(orient="records")

        return filtered_df

    def calculate_installment(
            self, user_id, annual_interest_rate, num_installments
            ):
        if not os.path.exists(self.FINANCIAL_MANAGER):
            return []

        df = pd.read_csv(self.FINANCIAL_MANAGER)
        user_transactions = df[df["user_id"] == user_id]

        total_value = user_transactions["value"].sum()
        monthly_interest_rate = (annual_interest_rate / 100) / 12

        amortization = total_value / num_installments
        debit_balance = total_value
        installment_details = []

        for month in range(1, num_installments + 1):
            fees = debit_balance * monthly_interest_rate
            installment = amortization + fees
            debit_balance -= amortization

            installment_details.append({
                "Month": month,
                "Installments": round(installment, 2),
                "Fees": round(fees, 2),
                "Amortization": round(amortization, 2),
                "Debit balance": round(debit_balance, 2) if debit_balance > 0 else 0.0
            })

        return installment_details

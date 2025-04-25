import random
from models.account import Bankaccount
from typing import List
from models.transaction import Transaction


class User:
    user_id: int
    username: str
    surname: str
    accounts: List[Bankaccount]

    def __init__(self, username: str, surname: str, user_id: int) -> None:
        self.username = username
        self.surname = surname
        self.accounts: List[Bankaccount] = []
        self.user_id = user_id

    def get_user_id(self):
        # Повертає user_id
        return self.user_id

    def __repr__(self):
        return f"UserName: {self.username}, Surname: {self.surname}, UserId: {self.user_id}"

    def add_account(self, account) -> None:
        # Додає акаунт до користувача
        self.accounts.append(account)

    def get_total_balance(self) -> float:
        # Отримує баланс з усіх акаунтів
        return sum(account.get_balance() for account in self.accounts)

    def get_account(self) -> List[Bankaccount]:
        # Отримує список акаунтів користувача
        return self.accounts

    def get_account_by_id(self, account_id):
        for account in self.accounts:
            print(f"Account verification: {account}")  # додай це
            if isinstance(account, Bankaccount) and account.get_account_id() == account_id:
                return account
        return None


    def get_balances_by_currency(self) -> dict:
        balances = {}
        for account in self.accounts:
            currency = account.currency
            if currency in balances:
                balances[currency] += account.get_balance()
            else:
                balances[currency] = account.get_balance()
        return balances

    def print_summary(self):
        print(f"=== User report ===")
        print(f"Name: {self.username} {self.surname}")
        print(f"User ID: {self.get_user_id()}")
        print(f"General balance: {self.get_total_balance()}")
        print("Balance by currencies:")

        for currency, balance in self.get_balances_by_currency().items():
            print(f"  {currency}: {balance}")
        print("\n--- Accounts ---")
        for account in self.accounts:
            print(f"account ID: {account.get_account_id()}, balance: {account.get_balance()} {account.currency}")
            print("Transactions:")
            if not account.get_transactions():
                print("(No transactions)")
            else:
                for t in account.get_transactions():
                    print("   ",t.get_transaction_detail())
            print("-" * 30)

    @staticmethod
    def from_dict(data):
        user = User(username=data["username"],surname=data["surname"],user_id=data["user_id"])

        for acc_data in data.get("accounts",[]):
            account = Bankaccount(account_id=acc_data["account_id"],
                                  balance=acc_data["balance"],
                                  currency=acc_data["currency"])
            for tr_data in acc_data.get("transactions",[]):
                transaction = Transaction.from_dict(tr_data)
                account.transactions.append(transaction)
            user.add_account(account)
        return user

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "surname": self.surname,
            "accounts": [a.to_dict() for a in self.accounts]
        }

from datetime import datetime
from os import access
from typing import List
from models.transaction import Transaction

class Bankaccount:
    account_id: int
    balance: int
    currency:str

    def __init__(self, account_id, balance, currency)->None:
        self.account_id = account_id
        self.balance = balance
        self.currency = currency
        self.transactions: List[Transaction] = []


    def get_account_id(self)->int:
        return self.account_id

    def deposit(self, amount, currency)->None:
        # Add money to account and write transaction
        # Тобто у нас э акаунт на який ми хочемо покласти гроші self.balance += amount
        # Після чого ми створюємо транзакцію прописуємо тип транзакції та час поповнення
        # Також не забуваємо про транзакшн айді те що айді завжди на 1 збільшується
        self.balance += amount
        transaction = Transaction(transaction_id=len(self.transactions)+1,
                                  amount = amount,
                                  currency= currency ,
                                  transaction_type="deposit",
                                  time_stamp=datetime.now())
        self.transactions.append(transaction)

    def withdraw(self, amount, currency) -> str:
       try:
           if not isinstance(amount,(int,float)):
               raise ValueError("Value must be a number")

           if amount < 0:
               raise ValueError("Amount cannot be negative")

           if currency != self.currency:
               raise ValueError("Currency cannot be changed")

           if amount > self.balance:
               raise ValueError("Amount cannot be greater than balance")

           self.balance -= amount
           withdraw_transaction = Transaction(transaction_id=len(self.transactions)+1,
                                              amount = amount,
                                              currency= currency,
                                              transaction_type="withdraw",
                                              time_stamp=datetime.now())
           self.transactions.append(withdraw_transaction)
           return "Withdrawal was successful"
       except Exception as e:
           return f"Withdrawal error:{e}"

    def transfer( self,target_account,amount: float,currency: str):
        try:
            if amount <= 0:
                raise ValueError("The transfer amount must be greater than 0..")

            if currency != self.currency:
                raise ValueError("The amount must be in your account currency..")

            if amount > self.balance:
                raise ValueError("Insufficient funds for transfer.")

            exchange_rate = self.get_exchange_rate(
                self.currency,target_account.currency)
            if exchange_rate is None:
                raise ValueError("Unable to transfer: no exchange rate available.")

            converted_amount = round(amount * exchange_rate,2)

            # Знімаємо з поточного акаунта
            self.balance -= amount
            self.transactions.append(
                Transaction(
                    transaction_id=len(self.transactions) + 1,
                    amount=amount,
                    currency=self.currency,
                    transaction_type=f"transfer_to_{target_account.get_account_id()}",
                    time_stamp=datetime.now()))

            # Додаємо на акаунт одержувача
            target_account.balance += converted_amount
            target_account.transactions.append(
                Transaction(transaction_id=len(target_account.transactions) + 1,
                    amount=converted_amount,
                    currency=target_account.currency,
                    transaction_type=f"transfer_from_{self.get_account_id()}",
                    time_stamp=datetime.now()
                ))

            return f"Transfer completed. {amount} {self.currency} → {converted_amount} {target_account.currency}"

        except ValueError as e:
            return f"Transfer error: {str(e)}"


    @staticmethod
    def get_exchange_rate(from_currency: str, to_currency: str) -> float:
        exchange_rates = {
            ('USD', 'UAN'): 39.5,
            ('UAN', 'USD'): 1 / 39.5,
            ('USD', 'EUR'): 0.92,
            ('EUR', 'USD'): 1 / 0.92,
            ('UAN', 'EUR'): (1 / 39.5) * 0.92,
            ('EUR', 'UAN'): (1 / 0.92) * 39.5,
        }
        if from_currency == to_currency:
            return 1.0

        return exchange_rates.get((from_currency, to_currency), None)

    def get_balance(self):
        return self.balance

    def get_transactions(self):
        return self.transactions


    def to_dict(self):
        return {"account_id": self.account_id,
                "balance": self.balance,
                "currency": self.currency,
                "transactions": [t.to_dict() for t in self.transactions]}

    @staticmethod
    def from_dict(data):
        account = Bankaccount(
            account_id=data["account_id"],
            balance=data["balance"],
            currency=data["currency"]
        )
        for tr_data in data.get("transactions", []):
            transaction = Transaction.from_dict(tr_data)
            account.transactions.append(transaction)
            return account


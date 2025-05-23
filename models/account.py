# pylint: disable=C0301

"""Defines the BankAccount model with operations for deposit, withdrawal,
transfer, and transaction history."""

from datetime import datetime
from typing import List, Optional
from models.transaction import Transaction


class BankAccount:
    """
    Represents a bank account with basic operations such as deposit, withdrawal, and transfer.
    Stores a list of transaction history.
    """

    account_id: int
    balance: float
    currency: str

    def __init__(self, account_id: int, balance: float, currency: str) -> None:
        """
        Initialize a bank account with the given ID, starting balance, and currency.

        :param account_id: Unique identifier for the account
        :param balance: Initial balance of the account
        :param currency: Currency type (e.g., 'USD', 'EUR', 'UAN')
        """

        self.account_id = account_id
        self.balance = balance
        self.currency = currency
        self.transactions: List[Transaction] = []

    def get_account_id(self) -> int:
        """
        Returns the account ID.

        :return: Account identifier
        """
        return self.account_id

    def deposit(self, amount: float, currency: str) -> str:
        """
        Deposits a specified amount to the account, if the currency matches and amount is valid.

        :param amount: The amount to deposit (must be positive number)
        :param currency: The currency of the deposit (must match account's currency)
        :return: Result message indicating success or error
        """
        # Code borrowed from: https://github.com/Pavansomisetty21/Online-Banking-System-using-Python-and-MongoDB/blob/main/banking.py
        # Author: Pavansomisetty21
        # Date downloaded: 2025-04-25
        # License: MIT
        #
        # Modifications  by Alina Upyrova:
        # - Removed MongoDB write operations
        # - Added type annotations and error handling
        # - Refactored transaction recording using local list

        try:
            if not isinstance(amount, (int, float)):
                raise ValueError("Amount must be of type int or float")

            if amount < 0:
                raise ValueError("Amount cannot be negative")

            if currency != self.currency:
                raise ValueError("Currency mismatch")

            self.balance += amount
            transaction = Transaction(
                transaction_id=len(self.transactions) + 1,
                amount=amount,
                currency=currency,
                transaction_type="deposit",
                time_stamp=datetime.now(),
            )
            self.transactions.append(transaction)

            return "Deposit successful"
        except ValueError as e:
            return f"Deposit error: {e}"

    def withdraw(self, amount: float, currency: str) -> str:
        """
        Withdraws a specified amount from the account if sufficient funds and currency match.

        :param amount: The amount to withdraw (must be positive number)
        :param currency: The currency of the withdrawal (must match account's currency)
        :return: Result message indicating success or error
        """

        # Code borrowed from: https://github.com/Pavansomisetty21/Online-Banking-System-using-Python-and-MongoDB/blob/main/banking.py
        # Author: Pavansomisetty21
        # Date downloaded: 2025-04-25
        # License: MIT
        #
        # Modifications by Alina Upyrova:
        # - Removed MongoDB write operations
        # - Added type annotations and error handling
        # - Refactored transaction recording using local list
        try:
            if not isinstance(amount, (int, float)):
                raise ValueError("Value must be a number")

            if amount < 0:
                raise ValueError("Amount cannot be negative")

            if currency != self.currency:
                raise ValueError("Currency cannot be changed")

            if amount > self.balance:
                raise ValueError("Amount cannot be greater than balance")

            self.balance -= amount
            withdraw_transaction = Transaction(
                transaction_id=len(self.transactions) + 1,
                amount=amount,
                currency=currency,
                transaction_type="withdraw",
                time_stamp=datetime.now(),
            )
            self.transactions.append(withdraw_transaction)
            return "Withdrawal was successful"
        except ValueError as e:
            return f"Withdrawal error:{e}"

    def transfer(
        self, target_account: "BankAccount", amount: float, currency: str
    ) -> str:
        """
        Transfers a specified amount from this account to another account,
        including currency exchange.

        :param target_account: The target Bankaccount object to receive funds
        :param amount: The amount to transfer
        :param currency: The currency of the transfer (must match this account's currency)
        :return: Result message indicating success or error
        """
        # Code borrowed from: https://github.com/Pavansomisetty21/Online-Banking-System-using-Python-and-MongoDB/blob/main/banking.py
        # Author: Pavansomisetty21
        # Date of download: 2025-04-25
        # License: MIT
        #
        # Modifications by Alina Upyrova:
        # - Removed MongoDB integration and all database dependencies
        # - Added static typing annotations
        # - Reorganized and simplified method structure
        # - Added exception handling for input validation
        # - Refactored method and variable names to follow PEP8
        # - Separated data model (Transaction) from logic
        # - Improved currency conversion handling

        try:
            if amount <= 0:
                raise ValueError("The transfer amount must be greater than 0..")

            if currency != self.currency:
                raise ValueError("The amount must be in your account currency..")

            if amount > self.balance:
                raise ValueError("Insufficient funds for transfer.")

            exchange_rate = self.get_exchange_rate(
                self.currency, target_account.currency
            )
            if exchange_rate is None:
                raise ValueError("Unable to transfer: no exchange rate available.")

            converted_amount = round(amount * exchange_rate, 2)

            self.balance -= amount
            self.transactions.append(
                Transaction(
                    transaction_id=len(self.transactions) + 1,
                    amount=amount,
                    currency=self.currency,
                    transaction_type=f"transfer_to_{target_account.get_account_id()}",
                    time_stamp=datetime.now(),
                )
            )

            target_account.balance += converted_amount
            target_account.transactions.append(
                Transaction(
                    transaction_id=len(target_account.transactions) + 1,
                    amount=converted_amount,
                    currency=target_account.currency,
                    transaction_type=f"transfer_from_{self.get_account_id()}",
                    time_stamp=datetime.now(),
                )
            )

            formated_amount = (
                int(converted_amount)
                if converted_amount.is_integer()
                else converted_amount
            )
            return (
                f"Transfer completed. {amount} {self.currency} → {formated_amount} "
                f"{target_account.currency}"
            )

        except ValueError as e:
            return f"Transfer error: {str(e)}"

    @staticmethod
    def get_exchange_rate(from_currency: str, to_currency: str) -> Optional[float]:
        """
        Retrieves the exchange rate between two currencies.

        :param from_currency: Currency to convert from
        :param to_currency: Currency to convert to
        :return: Exchange rate as a float, or None if unavailable
        """

        exchange_rates = {
            ("USD", "UAN"): 39.5,
            ("UAN", "USD"): 1 / 39.5,
            ("USD", "EUR"): 0.92,
            ("EUR", "USD"): 1 / 0.92,
            ("UAN", "EUR"): (1 / 39.5) * 0.92,
            ("EUR", "UAN"): (1 / 0.92) * 39.5,
        }
        if from_currency == to_currency:
            return 1.0

        return exchange_rates.get((from_currency, to_currency), None)

    def get_balance(self) -> float:
        """
        Returns the current balance of the account.

        :return: Current account balance
        """
        return self.balance

    def get_transactions(self) -> List[Transaction]:
        """
        Returns a list of all transaction objects associated with this account.

        :return: List of Transaction objects
        """
        return self.transactions

    def to_dict(self):
        """
        Converts the account data to a dictionary format for serialization.
        :return: Dictionary with account data
        """
        # Code borrowed from: https://github.com/pjastr/PFsample/blob/master/src/user.py
        # Author: pjastr
        # Date of download: 2025-04-25
        # License: MIT
        #
        # Modifications by Alina Upyrova:
        # - Only the conceptual idea (serialization/deserialization) was reused
        # - Completely rewrote the implementation for a different domain (BankAccount instead of User)
        # - Changed return type from JSON string to Python dictionary
        # - Removed all JSON-related logic (json.dumps/json.loads)
        # - Added support for nested object serialization (Transaction list)
        # - Added error handling for missing or invalid data
        # - Applied PEP8 naming and static typing
        return {
            "account_id": self.account_id,
            "balance": self.balance,
            "currency": self.currency,
            "transactions": [t.to_dict() for t in self.transactions],
        }

    @staticmethod
    def from_dict(data) -> Optional["BankAccount"]:
        """
        Creates a Bankaccount instance from a dictionary of saved data.
        :param data: Dictionary with keys 'account_id', 'balance', 'currency', and 'transactions'
        :return: Bankaccount instance or None if error occurs
        """
        # Code borrowed from: https://github.com/pjastr/PFsample/blob/master/src/user.py
        # Author: pjastr
        # Date of download: 2025-04-25
        # License: MIT
        #
        # Modifications by Alina Upyrova:
        # - Only the conceptual idea (serialization/deserialization) was reused
        # - Completely rewrote the implementation for a different domain (BankAccount instead of User)
        # - Changed return type from JSON string to Python dictionary
        # - Removed all JSON-related logic (json.dumps/json.loads)
        # - Added support for nested object serialization (Transaction list)
        # - Added error handling for missing or invalid data
        # - Applied PEP8 naming and static typing

        try:
            account = BankAccount(
                account_id=data["account_id"],
                balance=data["balance"],
                currency=data["currency"],
            )

            for tr_data in data.get("transactions", []):
                transaction = Transaction.from_dict(tr_data)
                account.transactions.append(transaction)

            return account
        except (ValueError, KeyError):
            print("Error loading account from dict")
            return None

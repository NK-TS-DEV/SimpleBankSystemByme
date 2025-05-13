"""Unit tests for the BankAccount class. Covers deposit, withdrawal,
transfer, exchange rates, serialization, and transaction history.
"""

import unittest
from models.account import BankAccount


class DepositTests(unittest.TestCase):
    """Tests for the deposit method of BankAccount."""

    def setUp(self):
        """Initialize a test account before each test."""
        self.account = BankAccount(account_id=1, balance=500, currency="USD")

    def test_valid_deposit(self):
        """Test depositing a valid amount updates balance and logs transaction."""
        self.account.deposit(100, "USD")
        self.assertEqual(self.account.get_balance(), 600)
        self.assertEqual(len(self.account.get_transactions()), 1)
        self.assertEqual(self.account.get_transactions()[0].transaction_type, "deposit")

    def test_negative_deposit(self):
        """Test depositing a negative amount does not change the balance."""
        self.account.deposit(-50, "USD")
        self.assertEqual(self.account.get_balance(), 500)

    def test_none_amount_deposit(self):
        """Test depositing None as amount returns error message."""
        result = self.account.deposit(None, "USD")
        self.assertIn("Amount must be of type int or float", result)

    def test_wrong_currency_deposit(self):
        """Test depositing with wrong currency returns error and no change."""
        result = self.account.deposit(100, "EUR")
        self.assertIn("Deposit error: Currency mismatch", result)
        self.assertEqual(self.account.get_balance(), 500)
        self.assertEqual(len(self.account.get_transactions()), 0)


class WithdrawTests(unittest.TestCase):
    """Tests for the withdraw method of BankAccount."""

    def setUp(self):
        """Initialize a test account before each test."""
        self.account = BankAccount(account_id=1, balance=500, currency="USD")

    def test_valid_withdrawal(self):
        """Test successful withdrawal updates balance and logs transaction."""
        result = self.account.withdraw(200, "USD")
        self.assertEqual(result, "Withdrawal was successful")
        self.assertEqual(self.account.get_balance(), 300)

    def test_negative_withdrawal(self):
        """Test withdrawing a negative amount returns error."""
        result = self.account.withdraw(-100, "USD")
        self.assertIn("Amount cannot be negative", result)

    def test_insufficient_funds(self):
        """Test withdrawing more than balance returns error."""
        result = self.account.withdraw(1000, "USD")
        self.assertIn("Amount cannot be greater than balance", result)

    def test_invalid_currency_withdrawal(self):
        """Test withdrawal with invalid currency returns error."""
        result = self.account.withdraw(100, "EUR")
        self.assertIn("Currency cannot be changed", result)

    def test_invalid_amount_type(self):
        """Test withdrawal with invalid amount type returns error."""
        result = self.account.withdraw("abc", "USD")
        self.assertIn("Value must be a number", result)

    def test_none_amount_withdrawal(self):
        """Test withdrawal with None as amount returns error."""
        result = self.account.withdraw(None, "USD")
        self.assertIn("Value must be a number", result)

    def test_none_currency_withdrawal(self):
        """Test withdrawal with None as currency returns error."""
        result = self.account.withdraw(100, None)
        self.assertIn("Currency cannot be changed", result)


class TransferTests(unittest.TestCase):
    """Tests for the transfer method of BankAccount."""

    def setUp(self):
        """Initialize two accounts before each test."""
        self.account1 = BankAccount(account_id=1, balance=500, currency="USD")
        self.account2 = BankAccount(account_id=2, balance=300, currency="USD")

    def test_successful_transfer(self):
        """Test successful transfer updates balances and logs transactions."""
        result = self.account1.transfer(self.account2, 100, "USD")
        self.assertEqual(result, "Transfer completed. 100 USD → 100 USD")
        self.assertEqual(self.account1.get_balance(), 400)
        self.assertEqual(self.account2.get_balance(), 400)

    def test_invalid_amount_transfer(self):
        """Test transferring non-positive amount returns error."""
        result = self.account1.transfer(self.account2, 0, "USD")
        self.assertIn("The transfer amount must be greater than 0", result)

    def test_insufficient_funds_transfer(self):
        """Test transferring more than balance returns error."""
        result = self.account1.transfer(self.account2, 999, "USD")
        self.assertIn("Insufficient funds", result)

    def test_different_currency_transfer(self):
        """Test transferring with mismatched currency returns error."""
        result = self.account1.transfer(self.account2, 100, "EUR")
        self.assertIn("The amount must be in your account currency", result)

    def test_transfer_to_different_currency_account(self):
        """Test transferring to different currency account with conversion."""
        eur_account = BankAccount(account_id=3, balance=0, currency="EUR")
        result = self.account1.transfer(eur_account, 99, "USD")
        self.assertIn("USD →", result)
        expected = round(99 * 0.92, 2)
        self.assertEqual(eur_account.get_balance(), expected)

    def test_transfer_unsupported_currency(self):
        """Test transferring to account with unsupported currency returns error."""
        inr_account = BankAccount(account_id=3, balance=0, currency="INR")
        result = self.account1.transfer(inr_account, 100, "USD")
        self.assertIn("no exchange rate available", result)

    def test_transfer_transaction_type(self):
        """Test that transaction types for both accounts are correct."""
        self.account1.transfer(self.account2, 50, "USD")
        tx1 = self.account1.get_transactions()[-1]
        tx2 = self.account2.get_transactions()[-1]
        self.assertTrue(tx1.transaction_type.startswith("transfer_to"))
        self.assertTrue(tx2.transaction_type.startswith("transfer_from"))

    def test_transfer_transaction_details(self):
        """Test that transaction fields after transfer match expected data."""
        self.account1.transfer(self.account2, 50, "USD")
        tx1 = self.account1.get_transactions()[-1]
        tx2 = self.account2.get_transactions()[-1]
        self.assertEqual(tx1.amount, 50)
        self.assertEqual(tx2.amount, 50)
        self.assertEqual(tx1.currency, "USD")
        self.assertEqual(tx2.currency, "USD")


class AccountDataTests(unittest.TestCase):
    """Tests for serialization and deserialization of BankAccount."""

    def setUp(self):
        """Initialize a test account."""
        self.account = BankAccount(account_id=1, balance=500, currency="USD")

    def test_to_dict_structure(self):
        """Test that to_dict returns a dictionary with expected structure."""
        self.account.deposit(123, "USD")
        data = self.account.to_dict()
        self.assertIn("account_id", data)
        self.assertIn("balance", data)
        self.assertIn("currency", data)
        self.assertIn("transactions", data)

    def test_from_dict_successful(self):
        """Test that from_dict correctly restores a BankAccount."""
        self.account.deposit(200, "USD")
        data = self.account.to_dict()
        restored = BankAccount.from_dict(data)
        self.assertEqual(restored.get_balance(), self.account.get_balance())
        self.assertEqual(len(restored.get_transactions()), 1)

    def test_from_dict_missing_key(self):
        """Test that from_dict with missing required keys returns None."""
        data = {"balance": 100, "currency": "USD"}
        account = BankAccount.from_dict(data)
        self.assertIsNone(account)


class ExchangeRateTests(unittest.TestCase):
    """Tests for exchange rate functionality."""

    def test_valid_exchange_rate(self):
        """Test known exchange rate returns correct value."""
        rate = BankAccount.get_exchange_rate("USD", "UAN")
        self.assertEqual(rate, 39.5)

    def test_same_currency_exchange_rate(self):
        """Test exchange rate between same currencies is 1.0."""
        rate = BankAccount.get_exchange_rate("USD", "USD")
        self.assertEqual(rate, 1.0)

    def test_invalid_exchange_rate(self):
        """Test unknown currency pair returns None."""
        rate = BankAccount.get_exchange_rate("USD", "GBP")
        self.assertIsNone(rate)


class TransactionTests(unittest.TestCase):
    """Tests for transaction history and format."""

    def setUp(self):
        """Initialize a test account."""
        self.account = BankAccount(account_id=1, balance=500, currency="USD")

    def test_transaction_repr(self):
        """Test that transaction __repr__ returns readable format."""
        self.account.deposit(150, "USD")
        tx = self.account.get_transactions()[0]
        self.assertIsInstance(repr(tx), str)
        self.assertIn("Transaction(ID=", repr(tx))

    def test_transaction_history_order(self):
        """Test that transactions are recorded in correct order."""
        self.account.deposit(100, "USD")
        self.account.withdraw(30, "USD")
        self.account.deposit(50, "USD")
        tx = self.account.get_transactions()
        self.assertEqual(tx[0].transaction_type, "deposit")
        self.assertEqual(tx[1].transaction_type, "withdraw")
        self.assertEqual(tx[2].transaction_type, "deposit")


if __name__ == "__main__":
    unittest.main()

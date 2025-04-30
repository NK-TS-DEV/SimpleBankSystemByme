import unittest
from models.user import User
from models.account import Bankaccount
from models.transaction import Transaction
from datetime import datetime
from unittest.mock import patch
import io


class TestUser(unittest.TestCase):
    def setUp(self):
        """Set up a user with two accounts before each test."""
        self.user = User(username="Alice", surname="Smith", user_id=1)
        self.account1 = Bankaccount(account_id=101, balance=200.0, currency="USD")
        self.account2 = Bankaccount(account_id=102, balance=300.0, currency="EUR")
        self.user.add_account(self.account1)
        self.user.add_account(self.account2)

    def test_user_initialization(self):
        """Test correct initialization of User attributes."""
        self.assertEqual(self.user.username, "Alice")
        self.assertEqual(self.user.surname, "Smith")
        self.assertEqual(self.user.get_user_id(), 1)
        self.assertEqual(len(self.user.get_account()), 2)

    def test_add_account(self):
        """Test that an account can be added to the user."""
        new_account = Bankaccount(account_id=103, balance=0.0, currency="UAH")
        self.user.add_account(new_account)
        self.assertIn(new_account, self.user.get_account())

    def test_get_total_balance(self):
        """Test calculation of total balance across accounts."""
        self.assertEqual(self.user.get_total_balance(), 500.0)

    def test_get_balances_by_currency(self):
        """Test balance grouping by currency."""
        balances = self.user.get_balances_by_currency()
        self.assertEqual(balances["USD"], 200.0)
        self.assertEqual(balances["EUR"], 300.0)

    def test_get_account_by_id_found(self):
        """Test retrieval of an existing account by ID."""
        found = self.user.get_account_by_id(102)
        self.assertIsNotNone(found)
        self.assertEqual(found.get_account_id(), 102)

    def test_get_account_by_id_not_found(self):
        """Test result when account ID is not found."""
        not_found = self.user.get_account_by_id(999)
        self.assertIsNone(not_found)

    def test_repr(self):
        """Test string representation (__repr__) of User."""
        text = repr(self.user)
        self.assertIn("UserName: Alice", text)
        self.assertIn("UserId: 1", text)

    def test_to_dict(self):
        """Test conversion of User to dictionary format."""
        data = self.user.to_dict()
        self.assertEqual(data["username"], "Alice")
        self.assertEqual(len(data["accounts"]), 2)

    def test_from_dict(self):
        """Test creating a User from a dictionary with account and transaction data."""
        input_data = {
            "user_id": 2,
            "username": "Bob",
            "surname": "Johnson",
            "accounts": [
                {
                    "account_id": 201,
                    "balance": 100.0,
                    "currency": "USD",
                    "transactions": [
                        {
                            "transaction_id": 1,
                            "amount": 100.0,
                            "currency": "USD",
                            "transaction_type": "deposit",
                            "time_stamp": "2023-01-01T12:00:00"
                        }
                    ]
                }
            ]
        }
        user = User.from_dict(input_data)
        self.assertEqual(user.username, "Bob")
        self.assertEqual(len(user.accounts), 1)
        self.assertEqual(len(user.accounts[0].get_transactions()), 1)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_summary_output(self, mock_stdout):
        """Test the textual summary output of a User."""
        self.user.print_summary()
        output = mock_stdout.getvalue()
        self.assertIn("=== User report ===", output)
        self.assertIn("Name: Alice Smith", output)
        self.assertIn("account ID: 101", output)
        self.assertIn("balance: 200.0 USD", output)

    def test_transaction_details_display(self):
        """Test display of transaction details from an account."""
        tx = Transaction(transaction_id=1, amount=50.0, transaction_type="deposit", time_stamp=datetime.now(), currency="USD")
        self.account1.transactions.append(tx)
        self.assertEqual(len(self.account1.get_transactions()), 1)
        self.assertIn("deposit", self.account1.get_transactions()[0].get_transaction_detail())

    def test_total_balance_empty(self):
        """Test total balance when user has no accounts."""
        user = User(username="Empty", surname="User", user_id=5)
        self.assertEqual(user.get_total_balance(), 0.0)

    def test_get_balances_by_currency_same_currency_multiple_accounts(self):
        """Test balance aggregation when multiple accounts have same currency."""
        account3 = Bankaccount(account_id=103, balance=50.0, currency="USD")
        self.user.add_account(account3)
        balances = self.user.get_balances_by_currency()
        self.assertEqual(balances["USD"], 250.0)


    def test_get_account_returns_list_of_accounts(self):
        """Test that get_account returns a list of Bankaccount instances."""
        accounts = self.user.get_account()
        self.assertIsInstance(accounts, list)
        for acc in accounts:
            self.assertIsInstance(acc, Bankaccount)

    def test_get_account_by_id_with_invalid_type(self):
        """Test handling of invalid account_id type (e.g. string)."""
        result = self.user.get_account_by_id("not-an-id")
        self.assertIsNone(result)

    def test_round_trip_dict_conversion(self):
        """Test conversion to dict and back preserves User data."""
        data = self.user.to_dict()
        new_user = User.from_dict(data)
        self.assertEqual(new_user.username, self.user.username)
        self.assertEqual(len(new_user.accounts), len(self.user.accounts))

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_summary_with_transactions(self, mock_stdout):
        """Test printed summary includes transaction details."""
        self.account1.deposit(100, "USD")
        self.user.print_summary()
        output = mock_stdout.getvalue()
        self.assertIn("Transactions:", output)
        self.assertIn("Amount:", output)

    def test_from_dict_missing_field(self):
        """Test that missing required fields raise KeyError in from_dict."""
        incomplete_data = {
            "user_id": 3,
            "username": "NoSurname"}
        with self.assertRaises(KeyError):
            User.from_dict(incomplete_data)

    def test_get_balances_by_currency_empty(self):
        """Test get_balances_by_currency returns empty dict for no accounts."""
        user = User(username="New", surname="User", user_id=10)
        self.assertEqual(user.get_balances_by_currency(), {})

    def test_to_dict_structure_keys(self):
        """Test that to_dict contains expected keys."""
        user_dict = self.user.to_dict()
        self.assertIn("user_id", user_dict)
        self.assertIn("username", user_dict)
        self.assertIn("surname", user_dict)
        self.assertIn("accounts", user_dict)


    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_summary_no_transactions(self, mock_stdout):
        """Test printed summary mentions '(No transactions)' when none exist."""
        self.user.print_summary()
        output = mock_stdout.getvalue()
        self.assertIn("(No transactions)", output)

    def test_from_dict_account_without_transactions(self):
        """Test from_dict handles accounts with empty transactions list."""
        data = {
            "user_id": 4,
            "username": "Kate",
            "surname": "Doe",
            "accounts": [
                {
                    "account_id": 301,
                    "balance": 150.0,
                    "currency": "USD",
                    "transactions": []
                }
            ]
        }
        user = User.from_dict(data)
        self.assertEqual(user.username, "Kate")
        self.assertEqual(len(user.accounts), 1)
        self.assertEqual(user.accounts[0].get_balance(), 150.0)

    def test_get_account_by_id_non_bankaccount(self):
        """Test get_account_by_id ignores non-Bankaccount objects in list."""
        self.user.accounts.append("fake")
        result = self.user.get_account_by_id(999)
        self.assertIsNone(result)

    def test_user_repr_format(self):
        """Test __repr__ string format of User instance."""
        rep = repr(self.user)
        self.assertTrue("UserName: Alice" in rep)
        self.assertTrue("Surname: Smith" in rep)
        self.assertTrue("UserId: 1" in rep)

if __name__ == "__main__":
    unittest.main()

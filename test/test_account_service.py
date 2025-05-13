"""
Unit tests for the AccountService class in the SimpleBankSystem application.
"""

import unittest
from unittest.mock import patch, MagicMock
from service.account_service import AccountService
from models.account import BankAccount
from models.user import User


class TestAccountService(unittest.TestCase):
    """Unit tests for AccountService logic."""

    def setUp(self):
        """Set up a test user with two bank accounts."""
        self.user = User(user_id=1, username="test", surname="User")
        self.account1 = BankAccount(account_id=101, balance=500.0, currency="USD")
        self.account2 = BankAccount(account_id=102, balance=300.0, currency="USD")
        self.user.add_account(self.account1)
        self.user.add_account(self.account2)

    def test_create_bank_account(self):
        """Test creation of a new bank account."""
        acc = AccountService.create_bank_account(
            account_id=999, initial_balance=100.0, currency="EUR"
        )
        self.assertEqual(acc.account_id, 999)
        self.assertEqual(acc.get_balance(), 100.0)
        self.assertEqual(acc.currency, "EUR")

    def test_deposit_to_account(self):
        """Test depositing funds to an account."""
        AccountService.deposit_to_account(self.account1, 200.0, "USD")
        self.assertEqual(self.account1.get_balance(), 700.0)

    def test_withdraw_from_account(self):
        """Test withdrawing funds from an account."""
        result = AccountService.withdraw_from_account(self.account1, 100.0, "USD")
        self.assertIn("successful", result.lower())
        self.assertEqual(self.account1.get_balance(), 400.0)

    def test_transfer_between_accounts(self):
        """Test transferring funds between two accounts."""
        result = AccountService.transfer_between_accounts(
            self.account1, self.account2, 100.0, "USD"
        )
        self.assertIn("Transfer completed", result)
        self.assertEqual(self.account1.get_balance(), 400.0)
        self.assertEqual(self.account2.get_balance(), 400.0)

    @patch("service.account_service.FileManager.save_all_users")
    @patch("service.account_service.FileManager.load_all_users")
    def test_withdraw_success(self, mock_load, mock_save):
        """Test CLI-based withdrawal with valid user and account."""
        mock_load.return_value = [self.user]

        args = MagicMock()
        args.user_id = 1
        args.account_id = 101
        args.amount = 50.0

        with patch("builtins.print") as mock_print:
            AccountService.withdraw(args)
            mock_print.assert_called()
            mock_save.assert_called_once()

    @patch("service.account_service.FileManager.save_all_users")
    @patch("service.account_service.FileManager.load_all_users")
    def test_create_account(self, mock_load, mock_save):
        """Test CLI-based account creation."""
        mock_load.return_value = [self.user]

        args = MagicMock()
        args.user_id = 1
        args.account_id = 999
        args.currency = "USD"

        with patch("builtins.print") as mock_print:
            AccountService.create_account(args)
            self.assertTrue(
                any(acc.account_id == 999 for acc in self.user.get_account())
            )
            mock_print.assert_called_with("Creating account ID 999 by user test")
            mock_save.assert_called_once()

    @patch("service.account_service.FileManager.save_all_users")
    @patch("service.account_service.FileManager.load_all_users")
    def test_deposit(self, mock_load, mock_save):
        """Test CLI-based deposit operation."""
        mock_load.return_value = [self.user]

        args = MagicMock()
        args.user_id = 1
        args.account_id = 101
        args.amount = 100.0
        args.currency = "USD"

        with patch("builtins.print") as mock_print:
            AccountService.deposit(args)
            self.assertEqual(self.account1.get_balance(), 600.0)
            mock_print.assert_called()
            mock_save.assert_called_once()

    @patch("service.account_service.FileManager.save_all_users")
    @patch("service.account_service.FileManager.load_all_users")
    def test_transfer(self, mock_load, mock_save):
        """Test CLI-based transfer between user accounts."""
        mock_load.return_value = [self.user]

        args = MagicMock()
        args.user_id = 1
        args.from_id = 101
        args.to_id = 102
        args.amount = 100.0

        with patch("builtins.print") as mock_print:
            AccountService.transfer(args)
            mock_print.assert_called()
            self.assertEqual(self.account1.get_balance(), 400.0)
            self.assertEqual(self.account2.get_balance(), 400.0)
            mock_save.assert_called_once()

    @patch("service.account_service.FileManager.load_all_users", return_value=[])
    def test_withdraw_user_not_found(self, _mock_load):
        """Test withdraw when user is not found."""
        args = MagicMock(user_id=99, account_id=101, amount=50.0)
        with patch("builtins.print") as mock_print:
            AccountService.withdraw(args)
            mock_print.assert_called_with("User not found")

    def test_from_dict_missing_key(self):
        """Test account creation from incomplete dictionary."""
        data = {"balance": 100, "currency": "USD"}
        account = BankAccount.from_dict(data)
        self.assertIsNone(account)

    @patch("service.account_service.FileManager.load_all_users")
    def test_withdraw_account_not_found(self, mock_load):
        """Test withdraw when account is not found."""
        mock_load.return_value = [self.user]
        args = MagicMock(user_id=1, account_id=999, amount=50.0)
        with patch("builtins.print") as mock_print:
            AccountService.withdraw(args)
            mock_print.assert_called_with("Account not found")

    @patch("service.account_service.FileManager.load_all_users", return_value=[])
    def test_create_account_user_not_found(self, _mock_load):
        """Test account creation when user does not exist."""
        args = MagicMock(user_id=99, account_id=1000, currency="USD")
        with patch("builtins.print") as mock_print:
            AccountService.create_account(args)
            mock_print.assert_called_with("User not found")

    @patch("service.account_service.FileManager.load_all_users")
    def test_deposit_account_not_found(self, mock_load):
        """Test deposit when account does not exist."""
        mock_load.return_value = [self.user]
        args = MagicMock(user_id=1, account_id=999, amount=100.0, currency="USD")
        with patch("builtins.print") as mock_print:
            AccountService.deposit(args)
            mock_print.assert_called_with("Account not found")

    @patch("service.account_service.FileManager.load_all_users")
    def test_transfer_account_not_found(self, mock_load):
        """Test transfer when one of the accounts does not exist."""
        mock_load.return_value = [self.user]
        args = MagicMock(user_id=1, from_id=101, to_id=999, amount=50.0)
        with patch("builtins.print") as mock_print:
            AccountService.transfer(args)
            mock_print.assert_called_with("One of the accounts was not found.")


if __name__ == "__main__":
    unittest.main()

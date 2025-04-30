import unittest
from unittest.mock import patch, MagicMock
from service.account_service import AccountService
from models.account import Bankaccount
from models.user import User


class TestAccountService(unittest.TestCase):

    def setUp(self):
        self.user = User(user_id=1, username="Test", surname="User")
        self.account1 = Bankaccount(account_id=101, balance=500.0, currency="USD")
        self.account2 = Bankaccount(account_id=102, balance=300.0, currency="USD")
        self.user.add_account(self.account1)
        self.user.add_account(self.account2)

    def test_create_bank_account(self):
        acc = AccountService.create_bank_account(account_id=999, initial_balance=100.0, currency="EUR")
        self.assertEqual(acc.account_id, 999)
        self.assertEqual(acc.get_balance(), 100.0)
        self.assertEqual(acc.currency, "EUR")

    def test_deposit_to_account(self):
        AccountService.deposit_to_account(self.account1,200.0,"USD")
        self.assertEqual(self.account1.get_balance(), 700.0)

    def test_withdraw_from_account(self):
        result = AccountService.withdraw_from_account(self.account1, 100.0, "USD")
        self.assertIn("successful", result.lower())
        self.assertEqual(self.account1.get_balance(), 400.0)

    def test_transfer_between_accounts(self):
        result = AccountService.transfer_between_accounts(self.account1, self.account2, 100.0, "USD")
        self.assertIn("Transfer completed", result)
        self.assertEqual(self.account1.get_balance(), 400.0)
        self.assertEqual(self.account2.get_balance(), 400.0)


    @patch("service.account_service.FileManager.save_all_users")
    @patch("service.account_service.FileManager.load_all_users")
    def test_withdraw_success(self, mock_load, mock_save):
        mock_load.return_value = [self.user]

        args = MagicMock()
        args.user_id = 1
        args.account_id = 101
        args.amount = 50.0

        with patch("builtins.print") as mock_print:
            AccountService.withdraw(args)
            mock_print.assert_called()

    @patch("service.account_service.FileManager.save_all_users")
    @patch("service.account_service.FileManager.load_all_users")
    def test_create_account(self, mock_load, mock_save):
        mock_load.return_value = [self.user]

        args = MagicMock()
        args.user_id = 1
        args.account_id = 999
        args.currency = "USD"

        with patch("builtins.print") as mock_print:
            AccountService.create_account(args)
            self.assertTrue(any(acc.account_id == 999 for acc in self.user.get_account()))
            mock_print.assert_called_with(f"🏦 Creating account ID 999 by user Test")

    @patch("service.account_service.FileManager.save_all_users")
    @patch("service.account_service.FileManager.load_all_users")
    def test_deposit(self, mock_load, mock_save):
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

    @patch("service.account_service.FileManager.save_all_users")
    @patch("service.account_service.FileManager.load_all_users")
    def test_transfer(self, mock_load, mock_save):
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

    @patch("service.account_service.FileManager.load_all_users", return_value=[])
    def test_withdraw_user_not_found(self, mock_load):
        args = MagicMock(user_id=99, account_id=101, amount=50.0)
        with patch("builtins.print") as mock_print:
            AccountService.withdraw(args)
            mock_print.assert_called_with("User not found")

    def test_from_dict_missing_key(self):
        data = {
            "balance": 100,
            "currency": "USD"
        }
        account = Bankaccount.from_dict(data)
        self.assertIsNone(account)


    @patch("service.account_service.FileManager.load_all_users")
    def test_withdraw_account_not_found(self, mock_load):
        mock_load.return_value = [self.user]
        args = MagicMock(user_id=1, account_id=999, amount=50.0)
        with patch("builtins.print") as mock_print:
            AccountService.withdraw(args)
            mock_print.assert_called_with("Account not found")

    @patch("service.account_service.FileManager.load_all_users", return_value=[])
    def test_create_account_user_not_found(self, mock_load):
        args = MagicMock(user_id=99, account_id=1000, currency="USD")
        with patch("builtins.print") as mock_print:
            AccountService.create_account(args)
            mock_print.assert_called_with("User not found")

    @patch("service.account_service.FileManager.load_all_users")
    def test_deposit_account_not_found(self, mock_load):
        mock_load.return_value = [self.user]
        args = MagicMock(user_id=1, account_id=999, amount=100.0, currency="USD")
        with patch("builtins.print") as mock_print:
            AccountService.deposit(args)
            mock_print.assert_called_with("Account not found")

    @patch("service.account_service.FileManager.load_all_users")
    def test_transfer_account_not_found(self,mock_load):
        mock_load.return_value = [self.user]
        args = MagicMock(
            user_id=1,
            from_id=101,
            to_id=999,
            amount=50.0)
        with patch("builtins.print") as mock_print:
            AccountService.transfer(args)
            mock_print.assert_called_with("One of the accounts was not found.")


if __name__ == "__main__":
    unittest.main()

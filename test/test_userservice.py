"""Unit tests for the Userservice class responsible for user registration and login."""

import unittest
from unittest.mock import patch, MagicMock
from service.user_service import Userservice
from models.user import User


class TestUserService(unittest.TestCase):
    """Set up a mock user list before each test."""

    def setUp(self):
        self.existing_user = User(user_id=1, username="Alice", surname="Smith")
        self.users = [self.existing_user]

    @patch("service.user_service.FileManager.save_all_users")
    @patch("service.user_service.FileManager.load_all_users")
    def test_register_new_user(self, mock_load, mock_save):
        """test that a new user is registered and saved correctly when users already exist."""
        mock_load.return_value = self.users

        mock_args = MagicMock()
        mock_args.username = "Bob"
        mock_args.surname = "Johnson"

        Userservice.register(mock_args)

        self.assertEqual(mock_save.call_count, 1)
        saved_users = mock_save.call_args[0][0]
        self.assertEqual(len(saved_users), 2)
        self.assertEqual(saved_users[1].username, "Bob")
        self.assertEqual(saved_users[1].surname, "Johnson")
        self.assertEqual(saved_users[1].user_id, 2)

    @patch("service.user_service.FileManager.load_all_users")
    def test_login_success(self, mock_load):
        """test successful login when user ID exists."""
        mock_load.return_value = self.users

        mock_args = MagicMock()
        mock_args.user_id = 1

        with patch("builtins.print") as mock_print:
            Userservice.login(mock_args)
            mock_print.assert_called_with("Hi, Alice Smith!")

    @patch("service.user_service.FileManager.load_all_users")
    def test_login_failure(self, mock_load):
        """test login failure when user ID does not exist."""
        mock_load.return_value = self.users

        mock_args = MagicMock()
        mock_args.user_id = 999

        with patch("builtins.print") as mock_print:
            Userservice.login(mock_args)
            mock_print.assert_called_with("User not found")

    @patch("service.user_service.FileManager.save_all_users")
    @patch("service.user_service.FileManager.load_all_users", return_value=[])
    def test_register_first_user(self, _mock_load, mock_save):
        """test registration when no users exist — should assign ID 1."""
        mock_args = MagicMock()
        mock_args.username = "Charlie"
        mock_args.surname = "Brown"

        Userservice.register(mock_args)

        saved_users = mock_save.call_args[0][0]
        self.assertEqual(saved_users[0].user_id, 1)
        self.assertEqual(saved_users[0].username, "Charlie")

    @patch("service.user_service.FileManager.save_all_users")
    @patch("service.user_service.FileManager.load_all_users")
    def test_existing_user_not_lost_on_register(self, mock_load, mock_save):
        """Ensure existing users are not removed when a new user is registered."""
        mock_load.return_value = self.users

        mock_args = MagicMock(username="Diana", surname="Prince")

        Userservice.register(mock_args)

        saved_users = mock_save.call_args[0][0]
        self.assertEqual(saved_users[0].username, "Alice")
        self.assertEqual(saved_users[1].username, "Diana")

    @patch("service.user_service.FileManager.load_all_users")
    def test_login_with_invalid_user_id_type(self, mock_load):
        """test login fails gracefully with invalid user ID type."""
        mock_load.return_value = self.users
        mock_args = MagicMock()
        mock_args.user_id = "one"

        with patch("builtins.print") as mock_print:
            Userservice.login(mock_args)
            mock_print.assert_called_with("User not found")

    @patch("service.user_service.FileManager.save_all_users")
    @patch("service.user_service.FileManager.load_all_users")
    def test_register_auto_increment_id(self, mock_load, mock_save):
        """test user ID auto-increments correctly even with gaps in user IDs."""
        self.users.append(User(user_id=5, username="Zoe", surname="Last"))
        mock_load.return_value = self.users

        mock_args = MagicMock(username="Max", surname="Newman")
        Userservice.register(mock_args)

        saved_users = mock_save.call_args[0][0]
        self.assertEqual(saved_users[-1].user_id, 6)

    @patch("service.user_service.FileManager.save_all_users")
    @patch("service.user_service.FileManager.load_all_users")
    def test_register_creates_user_instance(self, mock_load, mock_save):
        """Ensure that a new user is an instance of User after registration."""
        mock_load.return_value = self.users

        mock_args = MagicMock(username="Olivia", surname="Stone")
        Userservice.register(mock_args)

        saved_users = mock_save.call_args[0][0]
        self.assertIsInstance(saved_users[-1], User)


if __name__ == "__main__":
    unittest.main()

"""Unit tests for the FileManager class in the SimpleBankSystem application."""

import unittest
from unittest.mock import patch, mock_open
import json
from service.file_manager import FileManager
from models.user import User


class TestFileManager(unittest.TestCase):
    """Unit tests for the FileManager class."""

    def setUp(self):
        """Set up test data with two sample users."""
        self.user1 = User(user_id=1, username="Alice", surname="Smith")
        self.user2 = User(user_id=2, username="Bob", surname="Johnson")
        self.users = [self.user1, self.user2]

    @patch("service.file_manager.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_all_users(self, mock_json_dump, mock_file, mock_makedirs):
        """
        test saving a list of users to a file.

        Checks:
        - Directory creation with `os.makedirs`
        - File is opened correctly
        - Data is serialized and written via `json.dump`
        """
        FileManager.save_all_users(self.users)

        mock_makedirs.assert_called_once_with("data", exist_ok=True)
        mock_file.assert_called_once_with(FileManager.USERS_FILE, "w", encoding="utf-8")

        expected_data = [user.to_dict() for user in self.users]
        mock_json_dump.assert_called_once_with(
            expected_data, mock_file(), indent=4, ensure_ascii=False
        )

    @patch("service.file_manager.os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    def test_load_all_users(self, mock_file, _mock_exists):
        """
        test loading users from a file when it exists.

        Checks:
        - JSON is correctly deserialized
        - Users are returned with correct attributes
        """
        mock_data = json.dumps(
            [
                {"user_id": 1, "username": "Alice", "surname": "Smith", "accounts": []},
                {"user_id": 2, "username": "Bob", "surname": "Johnson", "accounts": []},
            ]
        )
        mock_file().read.return_value = mock_data

        users = FileManager.load_all_users()

        self.assertEqual(len(users), 2)
        self.assertEqual(users[0].username, "Alice")
        self.assertEqual(users[1].surname, "Johnson")

    @patch("service.file_manager.os.path.exists", return_value=False)
    def test_load_all_users_file_not_exist(self, _mock_exists):
        """
        test loading users when the file does not exist.

        Should return an empty list.
        """
        users = FileManager.load_all_users()
        self.assertEqual(users, [])


if __name__ == "__main__":
    unittest.main()

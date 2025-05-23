"""Unit tests for the Transaction class, including serialization,
validation, and utility methods."""

import unittest
from datetime import datetime
from models.transaction import Transaction


def generate_transaction_data(
    transaction_id=1,
    amount=100.0,
    transaction_type="deposit",
    currency="USD",
    time_stamp="2023-05-17T10:30:00",
):
    """Generate a dictionary representing transaction data for testing purposes."""
    return {
        "transaction_id": transaction_id,
        "amount": amount,
        "transaction_type": transaction_type,
        "currency": currency,
        "time_stamp": time_stamp,
    }


class TestTransaction(unittest.TestCase):  # pylint: disable=too-many-public-methods
    """Unit tests for the Transaction class."""

    def setUp(self):
        """Set up a sample transaction for testing."""
        self.transaction = Transaction(
            transaction_id=1,
            amount=100.0,
            transaction_type="deposit",
            time_stamp=datetime(2023, 5, 17, 10, 30, 0),
            currency="USD",
        )

    def test_get_transaction_id(self):
        """test that transaction ID is returned correctly."""
        self.assertEqual(self.transaction.get_transaction_id(), 1)

    def test_get_transaction_type(self):
        """test that transaction type is returned correctly."""
        self.assertEqual(self.transaction.get_transaction_type(), "deposit")

    def test_get_transaction_detail(self):
        """test that the transaction detail string is formatted correctly."""
        expected_detail = (
            "Amount: 100.0 Currency USD, "
            "Transaction type: deposit, Time= 2023-05-17 10:30:00"
        )
        self.assertEqual(self.transaction.get_transaction_detail(), expected_detail)

    def test_to_dict(self):
        """test serialization of transaction to dictionary."""
        expected_dict = {
            "transaction_id": 1,
            "amount": 100.0,
            "transaction_type": "deposit",
            "currency": "USD",
            "time_stamp": "2023-05-17T10:30:00",
        }
        self.assertEqual(self.transaction.to_dict(), expected_dict)

    def test_from_dict(self):
        """test deserialization from dictionary to Transaction object."""
        data = generate_transaction_data(
            transaction_id=1, amount=100.0, transaction_type="deposit", currency="USD"
        )
        new_transaction = Transaction.from_dict(data)
        self.assertEqual(new_transaction.get_transaction_id(), 1)
        self.assertEqual(new_transaction.amount, 100.0)
        self.assertEqual(new_transaction.transaction_type, "deposit")
        self.assertEqual(new_transaction.currency, "USD")
        self.assertEqual(new_transaction.time_stamp, datetime(2023, 5, 17, 10, 30, 0))

    def test_batch_dict_conversion(self):
        """test batch conversion to and from dict works for many transactions."""
        tx_list = [self.transaction for _ in range(100)]
        dicts = [tx.to_dict() for tx in tx_list]
        restored = [Transaction.from_dict(d) for d in dicts]
        self.assertEqual(len(restored), 100)
        for r in restored:
            self.assertEqual(r.get_transaction_type(), "deposit")

    def test_round_trip_dict_conversion(self):
        """test that to_dict followed by from_dict retains original data."""
        data = self.transaction.to_dict()
        new_obj = Transaction.from_dict(data)
        self.assertEqual(
            self.transaction.get_transaction_detail(), new_obj.get_transaction_detail()
        )

    def test_repr(self):
        """test the __repr__ output format."""
        expected_repr = (
            "Transaction(ID=1, Type=deposit, Amount=100.0, Time=2023-05-17 10:30:00)"
        )
        self.assertEqual(repr(self.transaction), expected_repr)

    def test_str_output(self):
        """test that __str__ returns a valid string."""
        string_output = str(self.transaction)
        self.assertIsInstance(string_output, str)
        self.assertIn("Transaction", string_output)

    def test_different_transaction_types(self):
        """test that different transaction types are accepted."""
        for t_type in ["deposit", "withdraw", "transfer"]:
            with self.subTest(t_type=t_type):
                tx = Transaction(
                    transaction_id=2,
                    amount=50.0,
                    transaction_type=t_type,
                    time_stamp=datetime.now(),
                    currency="EUR",
                )
                self.assertEqual(tx.get_transaction_type(), t_type)

    def test_invalid_transaction_id_type(self):
        """test that invalid transaction_id type raises TypeError."""
        with self.assertRaises(TypeError):
            Transaction("one", 100.0, "deposit", datetime.now(), "USD")

    def test_missing_timestamp_raises(self):
        """test that passing None as timestamp raises TypeError."""
        with self.assertRaises(TypeError):
            Transaction(1, 100.0, "deposit", None, "USD")

    def test_transaction_detail_contains_fields(self):
        """test that detail string contains key fields."""
        detail = self.transaction.get_transaction_detail()
        self.assertIn("Amount", detail)
        self.assertIn("Currency", detail)
        self.assertIn("Time", detail)

    def test_invalid_amount_type(self):
        """test that non-float amount raises TypeError."""
        with self.assertRaises(TypeError):
            Transaction(1, "one hundred", "deposit", datetime.now(), "USD")

    def test_invalid_currency_type(self):
        """test that non-string currency raises TypeError."""
        with self.assertRaises(TypeError):
            Transaction(1, 100.0, "deposit", datetime.now(), 100)

    def test_invalid_transaction_type_type(self):
        """test that non-string transaction_type raises TypeError."""
        with self.assertRaises(TypeError):
            Transaction(1, 100.0, 123, datetime.now(), "USD")

    def test_from_dict_missing_timestamp(self):
        """test that missing timestamp key in dict raises KeyError."""
        data = {
            "transaction_id": 5,
            "amount": 100.0,
            "transaction_type": "deposit",
            "currency": "USD",
        }
        with self.assertRaises(KeyError):
            Transaction.from_dict(data)

    def test_from_dict_exact_timestamp_parsing(self):
        """test correct parsing of ISO timestamp from dict."""
        data = {
            "transaction_id": 2,
            "amount": 123.45,
            "transaction_type": "withdraw",
            "currency": "EUR",
            "time_stamp": "2023-08-01T14:45:00",
        }
        tx = Transaction.from_dict(data)
        self.assertEqual(tx.time_stamp, datetime(2023, 8, 1, 14, 45))

    def test_transaction_fields_types(self):
        """test that all fields have correct types."""
        self.assertIsInstance(self.transaction.transaction_id, int)
        self.assertIsInstance(self.transaction.amount, float)
        self.assertIsInstance(self.transaction.transaction_type, str)
        self.assertIsInstance(self.transaction.currency, str)
        self.assertIsInstance(self.transaction.time_stamp, datetime)

    def test_empty_transaction_type(self):
        """test that empty string for transaction_type raises ValueError."""
        with self.assertRaises(ValueError):
            Transaction(1, 100.0, "", datetime.now(), "USD")


if __name__ == "__main__":
    unittest.main()

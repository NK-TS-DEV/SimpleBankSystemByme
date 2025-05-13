"""Parameterized tests for the Transaction model's initialization and validation."""

from datetime import datetime
import pytest
from models.transaction import Transaction


@pytest.mark.parametrize(
    "transaction_id, amount, transaction_type, currency",
    [
        (10, 99.99, "deposit", "USD"),
        (20, 123.45, "withdraw", "EUR"),
        (30, 1000, "transfer", "UAN"),
    ],
)
def test_transaction_creation_valid_data(
    transaction_id, amount, transaction_type, currency
):
    """
    test creating transactions with valid data using parameterization.
    """
    now = datetime.now()
    tx = Transaction(
        transaction_id=transaction_id,
        amount=amount,
        transaction_type=transaction_type,
        time_stamp=now,
        currency=currency,
    )
    assert tx.transaction_id == transaction_id
    assert tx.amount == amount
    assert tx.transaction_type == transaction_type
    assert tx.currency == currency
    assert isinstance(tx.time_stamp, datetime)


@pytest.mark.parametrize(
    "invalid_value, expected_exception",
    [
        ("not-int", TypeError),
        (None, TypeError),
    ],
)
def test_transaction_invalid_id(invalid_value, expected_exception):
    """
    test that invalid transaction_id raises the correct exception.
    """
    with pytest.raises(expected_exception):
        Transaction(
            transaction_id=invalid_value,
            amount=100.0,
            transaction_type="deposit",
            time_stamp=datetime.now(),
            currency="USD",
        )


@pytest.mark.parametrize("amount", ["invalid", None, [], {}])
def test_transaction_invalid_amount_types(amount):
    """
    test that invalid amount types raise TypeError.
    """
    with pytest.raises(TypeError):
        Transaction(
            transaction_id=1,
            amount=amount,
            transaction_type="deposit",
            time_stamp=datetime.now(),
            currency="USD",
        )


@pytest.mark.parametrize("timestamp", ["not-a-date", 123456, None])
def test_transaction_from_dict_invalid_timestamp(timestamp):
    """
    test that from_dict raises ValueError or TypeError on invalid timestamp.
    """
    data = {
        "transaction_id": 1,
        "amount": 100.0,
        "transaction_type": "deposit",
        "currency": "USD",
        "time_stamp": timestamp,
    }

    with pytest.raises((TypeError, ValueError)):
        if isinstance(timestamp, str):
            Transaction.from_dict(data)
        else:
            # Manually construct if timestamp isn't even a string
            Transaction(
                transaction_id=1,
                amount=100.0,
                transaction_type="deposit",
                time_stamp=timestamp,
                currency="USD",
            )

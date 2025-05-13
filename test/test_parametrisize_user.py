"""Parameterized tests for the User model and its methods related to accounts and balances."""

import pytest
from models.user import User
from models.account import BankAccount


@pytest.mark.parametrize(
    "user_id, username, surname, expected_fullname",
    [
        (1, "Alice", "Smith", "Alice Smith"),
        (2, "Bob", "Johnson", "Bob Johnson"),
        (3, "Charlie", "Brown", "Charlie Brown"),
    ],
)
def test_user_initialization_and_repr(user_id, username, surname, expected_fullname):
    """
    test that user is initialized correctly and __repr__ returns proper format.
    """
    user = User(username=username, surname=surname, user_id=user_id)
    assert user.username == username
    assert user.surname == surname
    assert user.get_user_id() == user_id
    assert expected_fullname.split()[0] in repr(user)
    assert expected_fullname.split()[1] in repr(user)


@pytest.mark.parametrize(
    "account_data",
    [
        [(101, 100.0, "USD")],
        [(201, 300.0, "EUR"), (202, 200.0, "EUR")],
        [(301, 50.0, "USD"), (302, 75.0, "EUR"), (303, 25.0, "USD")],
    ],
)
def test_user_total_balance(account_data):
    """
    test total balance calculation across user accounts.
    """
    user = User(username="test", surname="User", user_id=5)
    for acc_id, balance, currency in account_data:
        acc = BankAccount(account_id=acc_id, balance=balance, currency=currency)
        user.add_account(acc)

    expected_balance = sum(balance for _, balance, _ in account_data)
    assert user.get_total_balance() == expected_balance
    assert isinstance(user.get_total_balance(), float)


@pytest.mark.parametrize(
    "accounts, expected_dict",
    [
        ([(101, 50.0, "USD")], {"USD": 50.0}),
        ([(201, 100.0, "EUR"), (202, 50.0, "EUR")], {"EUR": 150.0}),
        ([(301, 25.0, "USD"), (302, 75.0, "EUR")], {"USD": 25.0, "EUR": 75.0}),
    ],
)
def test_balances_by_currency(accounts, expected_dict):
    """
    test that balances are grouped correctly by currency.
    """
    user = User(username="Tester", surname="Multi", user_id=6)
    for acc_id, bal, cur in accounts:
        user.add_account(BankAccount(account_id=acc_id, balance=bal, currency=cur))

    result = user.get_balances_by_currency()
    assert result == expected_dict
    assert isinstance(result, dict)
    assert all(isinstance(k, str) for k in result)


@pytest.mark.parametrize(
    "account_id, expected_result",
    [
        (999, None),
        ("string", None),
        (-1, None),
    ],
)
def test_get_account_by_invalid_id(account_id, expected_result):
    """
    test that searching for invalid account IDs returns None.
    """
    user = User(username="Alice", surname="Smith", user_id=1)
    user.add_account(BankAccount(account_id=101, balance=100.0, currency="USD"))
    result = user.get_account_by_id(account_id)
    assert result is expected_result


@pytest.mark.parametrize(
    "input_data, should_fail",
    [
        ({"username": "Missing", "user_id": 1}, True),  # Missing surname
        ({"surname": "Missing", "user_id": 1}, True),  # Missing username
        ({"username": "Ok", "surname": "Now", "user_id": 1}, False),
    ],
)
def test_user_from_dict_required_fields(input_data, should_fail):
    """
    test that from_dict fails if required fields are missing.
    """
    if should_fail:
        with pytest.raises(KeyError):
            User.from_dict(input_data)
    else:
        user = User.from_dict(input_data)
        assert isinstance(user, User)

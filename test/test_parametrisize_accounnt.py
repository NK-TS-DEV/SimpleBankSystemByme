"""
Parameterized unit tests for BankAccount deposit and withdrawal operations.
"""

import pytest
from models.account import BankAccount


@pytest.mark.parametrize(
    "initial_balance, deposit_amount, currency, expected_balance",
    [(1000, 500, "USD", 1500), (0, 100, "EUR", 100), (50, 0, "UAN", 50)],
)
def test_deposit_success(initial_balance, deposit_amount, currency, expected_balance):
    """
    test successful deposits:
    - Ensures the balance is updated correctly.
    - A 'deposit' transaction is created and recorded.
    """
    account = BankAccount(account_id=1, balance=initial_balance, currency=currency)
    result = account.deposit(deposit_amount, currency)
    assert result == "Deposit successful"
    assert account.get_balance() == expected_balance
    assert len(account.get_transactions()) == 1
    assert account.get_transactions()[0].transaction_type == "deposit"


@pytest.mark.parametrize(
    "initial_balance, withdraw_amount, currency, expected_balance",
    [
        (1000, 300, "USD", 700),
        (500, 500, "EUR", 0),
    ],
)
def test_withdraw_success(initial_balance, withdraw_amount, currency, expected_balance):
    """
    test successful withdrawals:
    - Verifies that the balance decreases correctly.
    - A 'withdraw' transaction is recorded.
    """
    account = BankAccount(account_id=2, balance=initial_balance, currency=currency)
    result = account.withdraw(withdraw_amount, currency)
    assert result == "Withdrawal was successful"
    assert account.get_balance() == expected_balance
    assert len(account.get_transactions()) == 1
    assert account.get_transactions()[0].transaction_type == "withdraw"


@pytest.mark.parametrize(
    "amount, currency, expected_error",
    [
        (-100, "USD", "Amount cannot be negative"),
        (200, "EUR", "Currency cannot be changed"),
        (10000, "USD", "Amount cannot be greater than balance"),
    ],
)
def test_withdraw_errors(amount, currency, expected_error):
    """
    test various withdrawal error scenarios:
    - Negative withdrawal amount
    - Currency mismatch
    - Insufficient funds
    """
    account = BankAccount(account_id=3, balance=500, currency="USD")
    result = account.withdraw(amount, currency)
    assert expected_error in result


@pytest.mark.parametrize(
    "actions, expected_types",
    [
        ([("deposit", 200), ("withdraw", 100)], ["deposit", "withdraw"]),
        (
            [("deposit", 50), ("deposit", 150), ("withdraw", 100)],
            ["deposit", "deposit", "withdraw"],
        ),
    ],
)
def test_transaction_history(actions, expected_types):
    """
    Test that all transactions are recorded in correct order and type.
    """
    account = BankAccount(account_id=5, balance=500, currency="USD")
    for action, amount in actions:
        if action == "deposit":
            account.deposit(amount, "USD")
        else:
            account.withdraw(amount, "USD")

    transactions = account.get_transactions()
    assert [t.transaction_type for t in transactions] == expected_types

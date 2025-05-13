"""Tests for AccountService operations using parameterized inputs."""

import pytest
from models.account import BankAccount
from service.account_service import AccountService


@pytest.mark.parametrize(
    "account_id, balance, currency",
    [
        (1, 0.0, "USD"),
        (2, 100.5, "EUR"),
        (3, 9999.99, "UAN"),
    ],
)
def test_create_bank_account(account_id, balance, currency):
    """
    Test that a bank account is created with correct initial data.
    """
    account = AccountService.create_bank_account(account_id, balance, currency)
    assert isinstance(account, BankAccount)
    assert account.account_id == account_id
    assert account.balance == balance
    assert account.currency == currency


@pytest.mark.parametrize(
    "initial_balance, deposit_amount, currency, expected_balance",
    [
        (100, 50, "USD", 150),
        (0, 500, "EUR", 500),
        (20, 0, "UAN", 20),
    ],
)
def test_deposit_to_account(
    initial_balance, deposit_amount, currency, expected_balance
):
    """
    Test that depositing to an account updates the balance correctly.
    """
    account = BankAccount(account_id=1, balance=initial_balance, currency=currency)
    AccountService.deposit_to_account(account, deposit_amount, currency)
    assert account.get_balance() == expected_balance
    assert account.get_transactions()[-1].transaction_type == "deposit"


# pylint: disable=too-many-arguments
@pytest.mark.parametrize(
    "from_balance, to_balance, amount, currency, expected_from, expected_to",
    [
        (1000, 500, 200, "USD", 800, 700),
        (50, 0, 25, "EUR", 25, 25),
    ],
)
# pylint: disable=too-many-arguments, too-many-positional-arguments
def test_transfer_between_accounts(
    from_balance, to_balance, amount, currency, expected_from, expected_to
):
    """
    Test that transfers between accounts update balances correctly.
    """
    acc1 = BankAccount(account_id=1, balance=from_balance, currency=currency)
    acc2 = BankAccount(account_id=2, balance=to_balance, currency=currency)
    result = AccountService.transfer_between_accounts(acc1, acc2, amount, currency)
    assert "Transfer completed" in result
    assert acc1.get_balance() == expected_from
    assert acc2.get_balance() == expected_to
    assert acc1.get_transactions()[-1].transaction_type.startswith("transfer_to")
    assert acc2.get_transactions()[-1].transaction_type.startswith("transfer_from")


@pytest.mark.parametrize(
    "initial_balance, withdraw_amount, currency, expected_balance",
    [
        (200, 100, "USD", 100),
        (300, 300, "EUR", 0),
    ],
)
def test_withdraw_from_account(
    initial_balance, withdraw_amount, currency, expected_balance
):
    """
    Test successful withdrawals using AccountService.
    """
    account = BankAccount(account_id=1, balance=initial_balance, currency=currency)
    result = AccountService.withdraw_from_account(account, withdraw_amount, currency)
    assert result == "Withdrawal was successful"
    assert account.get_balance() == expected_balance
    assert account.get_transactions()[-1].transaction_type == "withdraw"

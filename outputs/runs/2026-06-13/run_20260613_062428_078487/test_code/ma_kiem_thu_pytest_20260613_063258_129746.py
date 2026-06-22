from inline_snapshot import snapshot

import pytest

from source_under_test import BankAccount

# ===== Tests for BankAccount.deposit =====
def test_bankaccount_deposit_positive_amount():
    account = BankAccount(100)
    assert account.deposit(50) == snapshot(150)

def test_bankaccount_deposit_negative_amount():
    with pytest.raises(ValueError, match="deposit amount must be positive"):
        account = BankAccount(100)
        account.deposit(-50)


# ===== Tests for BankAccount.withdraw =====
def test_bankaccount_withdraw_positive_amount():
    account = BankAccount(100)
    assert account.withdraw(50) == snapshot(50)

def test_bankaccount_withdraw_negative_amount():
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        account = BankAccount(100)
        account.withdraw(-50)

def test_bankaccount_withdraw_insufficient_funds():
    with pytest.raises(ValueError, match="insufficient funds"):
        account = BankAccount(100)
        account.withdraw(150)

from source_under_test import transfer

# ===== Tests for transfer =====
def test_transfer_different_accounts():
    source_account = BankAccount(100)
    target_account = BankAccount(200)
    assert transfer(source_account, target_account, 50) == snapshot((50, 250))

def test_transfer_same_account():
    account = BankAccount(100)
    with pytest.raises(ValueError, match="cannot transfer to same account"):
        transfer(account, account, 50)
import pytest

from source_under_test import BankAccount, transfer

# ===== Tests for BankAccount.deposit =====
def test_bankaccount_deposit_positive():
    """Kiểm tra deposit với số tiền dương, trả về số dư mới."""
    account = BankAccount(50)
    new_balance = account.deposit(30)
    assert new_balance == 80
    assert account.balance == 80

def test_bankaccount_deposit_zero_amount():
    """Kiểm tra deposit với số tiền không dương, phải ném ValueError."""
    account = BankAccount(10)
    with pytest.raises(ValueError) as exc:
        account.deposit(0)
    assert str(exc.value) == "deposit amount must be positive"

def test_bankaccount_deposit_negative_amount():
    """Kiểm tra deposit với số tiền âm, phải ném ValueError."""
    account = BankAccount(10)
    with pytest.raises(ValueError) as exc:
        account.deposit(-5)
    assert str(exc.value) == "deposit amount must be positive"


# ===== Tests for BankAccount.withdraw =====
def test_bankaccount_withdraw_positive():
    """Kiểm tra withdraw với số tiền hợp lệ, trả về số dư mới."""
    account = BankAccount(100)
    new_balance = account.withdraw(40)
    assert new_balance == 60
    assert account.balance == 60

def test_bankaccount_withdraw_zero_amount():
    """Kiểm tra withdraw với số tiền không dương, phải ném ValueError."""
    account = BankAccount(20)
    with pytest.raises(ValueError) as exc:
        account.withdraw(0)
    assert str(exc.value) == "withdraw amount must be positive"

def test_bankaccount_withdraw_negative_amount():
    """Kiểm tra withdraw với số tiền âm, phải ném ValueError."""
    account = BankAccount(20)
    with pytest.raises(ValueError) as exc:
        account.withdraw(-10)
    assert str(exc.value) == "withdraw amount must be positive"

def test_bankaccount_withdraw_insufficient_funds():
    """Kiểm tra withdraw khi số tiền lớn hơn số dư, phải ném ValueError."""
    account = BankAccount(30)
    with pytest.raises(ValueError) as exc:
        account.withdraw(50)
    assert str(exc.value) == "insufficient funds"


# ===== Tests for transfer =====
def test_transfer_success():
    """Kiểm tra transfer giữa hai tài khoản khác nhau, trả về tuple số dư mới."""
    src = BankAccount(100)
    tgt = BankAccount(20)
    result = transfer(src, tgt, 30)
    assert result == (70, 50)
    assert src.balance == 70
    assert tgt.balance == 50

def test_transfer_same_account():
    """Kiểm tra transfer khi source và target là cùng một tài khoản, phải ném ValueError."""
    acc = BankAccount(50)
    with pytest.raises(ValueError) as exc:
        transfer(acc, acc, 10)
    assert str(exc.value) == "cannot transfer to same account"
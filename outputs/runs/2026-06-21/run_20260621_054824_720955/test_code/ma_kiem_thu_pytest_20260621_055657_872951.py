import pytest

from source_under_test import BankAccount, transfer

# ===== Tests for BankAccount.deposit =====
def test_bankaccount_deposit_success():
    # Kiểm tra nạp tiền với số tiền dương, trả về số dư mới
    account = BankAccount(balance=100.0)
    assert account.deposit(50.0) == 150.0

def test_bankaccount_deposit_invalid_amount():
    # Kiểm tra nạp tiền với số tiền không dương, phải ném ValueError
    account = BankAccount(balance=100.0)
    with pytest.raises(ValueError) as exc:
        account.deposit(0)
    assert str(exc.value) == "deposit amount must be positive"
    with pytest.raises(ValueError) as exc2:
        account.deposit(-10)
    assert str(exc2.value) == "deposit amount must be positive"


# ===== Tests for BankAccount.withdraw =====
def test_bankaccount_withdraw_success():
    # Kiểm tra rút tiền hợp lệ, trả về số dư mới
    account = BankAccount(balance=200.0)
    assert account.withdraw(80.0) == 120.0

def test_bankaccount_withdraw_invalid_amount():
    # Kiểm tra rút tiền với số tiền không dương, phải ném ValueError
    account = BankAccount(balance=200.0)
    with pytest.raises(ValueError) as exc:
        account.withdraw(0)
    assert str(exc.value) == "withdraw amount must be positive"
    with pytest.raises(ValueError) as exc2:
        account.withdraw(-5)
    assert str(exc2.value) == "withdraw amount must be positive"

def test_bankaccount_withdraw_insufficient_funds():
    # Kiểm tra rút tiền vượt quá số dư, phải ném ValueError
    account = BankAccount(balance=100.0)
    with pytest.raises(ValueError) as exc:
        account.withdraw(150.0)
    assert str(exc.value) == "insufficient funds"


# ===== Tests for transfer =====
def test_transfer_success():
    # Kiểm tra chuyển tiền giữa hai tài khoản khác nhau, trả về tuple số dư mới
    src = BankAccount(balance=300.0)
    tgt = BankAccount(balance=100.0)
    result = transfer(src, tgt, 50.0)
    assert result == (250.0, 150.0)
    # Kiểm tra số dư sau chuyển
    assert src.balance == 250.0
    assert tgt.balance == 150.0

def test_transfer_same_account():
    # Kiểm tra chuyển tiền tới cùng một tài khoản, phải ném ValueError
    acc = BankAccount(balance=200.0)
    with pytest.raises(ValueError) as exc:
        transfer(acc, acc, 30.0)
    assert str(exc.value) == "cannot transfer to same account"
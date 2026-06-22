# ===== Tests for BankAccount.deposit =====
from source_under_test import BankAccount

def test_bankaccount_deposit_positive_amount():
    # Kiểm tra nạp tiền số lượng dương
    account = BankAccount(100)
    result = account.deposit(50)
    assert result == 150
    assert account.balance == 150

def test_bankaccount_deposit_zero_amount():
    # Kiểm tra nạp tiền số lượng 0 sẽ ném ValueError
    account = BankAccount(100)
    import pytest
    with pytest.raises(ValueError, match="deposit amount must be positive"):
        account.deposit(0)

def test_bankaccount_deposit_negative_amount():
    # Kiểm tra nạp tiền số lượng âm sẽ ném ValueError
    account = BankAccount(100)
    import pytest
    with pytest.raises(ValueError, match="deposit amount must be positive"):
        account.deposit(-20)

# ===== Tests for BankAccount.withdraw =====

def test_bankaccount_withdraw_valid_amount():
    # Kiểm tra rút tiền hợp lệ
    account = BankAccount(200)
    result = account.withdraw(80)
    assert result == 120
    assert account.balance == 120

def test_bankaccount_withdraw_zero_amount():
    # Kiểm tra rút tiền số lượng 0 sẽ ném ValueError
    account = BankAccount(200)
    import pytest
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        account.withdraw(0)

def test_bankaccount_withdraw_insufficient_funds():
    # Kiểm tra rút tiền vượt quá số dư sẽ ném ValueError
    account = BankAccount(50)
    import pytest
    with pytest.raises(ValueError, match="insufficient funds"):
        account.withdraw(100)

from source_under_test import transfer

# ===== Tests for transfer =====
from source_under_test import BankAccount, transfer

def test_transfer_between_accounts():
    # Kiểm tra chuyển tiền giữa hai tài khoản khác nhau
    source = BankAccount(150)
    target = BankAccount(30)
    result = transfer(source, target, 50)
    assert result == (100, 80)
    assert source.balance == 100
    assert target.balance == 80

def test_transfer_same_account():
    # Kiểm tra chuyển tiền cho chính tài khoản sẽ ném ValueError
    account = BankAccount(100)
    import pytest
    with pytest.raises(ValueError, match="cannot transfer to same account"):
        transfer(account, account, 10)
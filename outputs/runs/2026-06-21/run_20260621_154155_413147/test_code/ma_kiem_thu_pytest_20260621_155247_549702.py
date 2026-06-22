# ===== Tests for BankAccount.deposit =====
from source_under_test import BankAccount

# Kiểm tra deposit với số tiền dương hợp lệ
def test_bankaccount_deposit_positive_amount():
    # Tạo tài khoản với số dư ban đầu là 50
    account = BankAccount(50)
    # Gửi tiền 30 vào tài khoản
    result = account.deposit(30)
    # Số dư sau khi gửi phải là 80
    assert result == 80.0
    assert account.balance == 80.0

# Kiểm tra deposit với số tiền bằng 0 ném ValueError
def test_bankaccount_deposit_zero_amount():
    # Tạo tài khoản với số dư ban đầu là 50
    account = BankAccount(50)
    # Gửi tiền 0 phải ném ValueError
    import pytest
    with pytest.raises(ValueError, match="deposit amount must be positive"):
        account.deposit(0)

# Kiểm tra deposit với số tiền âm ném ValueError
def test_bankaccount_deposit_negative_amount():
    # Tạo tài khoản với số dư ban đầu là 50
    account = BankAccount(50)
    # Gửi tiền âm phải ném ValueError
    import pytest
    with pytest.raises(ValueError, match="deposit amount must be positive"):
        account.deposit(-10)

# ===== Tests for BankAccount.withdraw =====

# Kiểm tra withdraw với số tiền hợp lệ
def test_bankaccount_withdraw_valid_amount():
    # Tạo tài khoản với số dư ban đầu là 100
    account = BankAccount(100)
    # Rút tiền 40 từ tài khoản
    result = account.withdraw(40)
    # Số dư sau khi rút phải là 60
    assert result == 60.0
    assert account.balance == 60.0

# Kiểm tra withdraw với số tiền bằng 0 ném ValueError
def test_bankaccount_withdraw_zero_amount():
    # Tạo tài khoản với số dư ban đầu là 100
    account = BankAccount(100)
    # Rút tiền 0 phải ném ValueError
    import pytest
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        account.withdraw(0)

# Kiểm tra withdraw với số tiền âm ném ValueError
def test_bankaccount_withdraw_negative_amount():
    # Tạo tài khoản với số dư ban đầu là 100
    account = BankAccount(100)
    # Rút tiền âm phải ném ValueError
    import pytest
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        account.withdraw(-5)

# Kiểm tra withdraw với số tiền vượt quá số dư ném ValueError
def test_bankaccount_withdraw_insufficient_funds():
    # Tạo tài khoản với số dư ban đầu là 30
    account = BankAccount(30)
    # Rút tiền 50 khi chỉ có 30 phải ném ValueError
    import pytest
    with pytest.raises(ValueError, match="insufficient funds"):
        account.withdraw(50)

from source_under_test import transfer

# ===== Tests for transfer =====
from source_under_test import BankAccount, transfer

# Kiểm tra transfer giữa hai tài khoản khác nhau
def test_transfer_between_different_accounts():
    # Tạo tài khoản nguồn với số dư 100
    source = BankAccount(100)
    # Tạo tài khoản đích với số dư 50
    target = BankAccount(50)
    # Chuyển 30 từ nguồn sang đích
    result = transfer(source, target, 30)
    # Số dư nguồn phải là 70, đích phải là 80
    assert result == (70.0, 80.0)
    assert source.balance == 70.0
    assert target.balance == 80.0

# Kiểm tra transfer tới cùng một tài khoản ném ValueError
def test_transfer_same_account():
    # Tạo một tài khoản duy nhất
    acct = BankAccount(100)
    # Chuyển tiền cho chính nó phải ném ValueError
    import pytest
    with pytest.raises(ValueError, match="cannot transfer to same account"):
        transfer(acct, acct, 10)
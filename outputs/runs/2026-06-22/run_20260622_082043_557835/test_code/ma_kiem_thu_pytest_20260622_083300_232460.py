# ===== Tests for BankAccount.deposit =====
from source_under_test import BankAccount
import pytest

# Kiểm tra rằng constructor từ chối số dư âm
def test_bankaccount_deposit_init_negative_balance():
    # Kiểm tra BankAccount(-100) ném ValueError với thông điệp "initial balance cannot be negative"
    with pytest.raises(ValueError, match="initial balance cannot be negative"):
        BankAccount(-100)

# Kiểm tra deposit từ chối số tiền không dương
def test_bankaccount_deposit_rejects_non_positive_amount():
    # Kiểm tra deposit(0) ném ValueError với thông điệp "deposit amount must be positive"
    account = BankAccount(50)
    with pytest.raises(ValueError, match="deposit amount must be positive"):
        account.deposit(0)

# Kiểm tra deposit từ chối số tiền âm
def test_bankaccount_deposit_rejects_negative_amount():
    # Kiểm tra deposit(-10) ném ValueError với thông điệp "deposit amount must be positive"
    account = BankAccount(50)
    with pytest.raises(ValueError, match="deposit amount must be positive"):
        account.deposit(-10)

# Kiểm tra deposit hợp lệ trả về số dư đã cập nhật
def test_bankaccount_deposit_valid_amount():
    # Kiểm tra deposit(50) trả về 100 khi balance ban đầu là 50
    account = BankAccount(50)
    result = account.deposit(50)
    assert result == 100
    assert account.balance == 100

# Kiểm tra deposit nhiều lần tích lũy đúng
def test_bankaccount_deposit_multiple_times():
    # Kiểm tra việc gọi deposit nhiều lần tích lũy đúng số dư
    account = BankAccount(100)
    account.deposit(25)
    account.deposit(25)
    assert account.balance == 150

# ===== Tests for BankAccount.withdraw =====

# Kiểm tra withdraw từ chối số tiền không dương
def test_bankaccount_withdraw_rejects_non_positive_amount():
    # Kiểm tra withdraw(0) ném ValueError với thông điệp "withdraw amount must be positive"
    account = BankAccount(30)
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        account.withdraw(0)

# Kiểm tra withdraw từ chối số tiền âm
def test_bankaccount_withdraw_rejects_negative_amount():
    # Kiểm tra withdraw(-10) ném ValueError với thông điệp "withdraw amount must be positive"
    account = BankAccount(30)
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        account.withdraw(-10)

# Kiểm tra withdraw từ chối số tiền lớn hơn số dư
def test_bankaccount_withdraw_insufficient_funds():
    # Kiểm tra withdraw(50) ném ValueError với thông điệp "insufficient funds" khi balance là 30
    account = BankAccount(30)
    with pytest.raises(ValueError, match="insufficient funds"):
        account.withdraw(50)

# Kiểm tra withdraw hợp lệ trả về số dư đã cập nhật
def test_bankaccount_withdraw_valid_amount():
    # Kiểm tra withdraw(40) trả về 60 khi balance ban đầu là 100
    account = BankAccount(100)
    result = account.withdraw(40)
    assert result == 60
    assert account.balance == 60

# Kiểm tra withdraw toàn bộ số dư
def test_bankaccount_withdraw_full_balance():
    # Kiểm tra withdraw(100) trả về 0 khi balance ban đầu là 100
    account = BankAccount(100)
    result = account.withdraw(100)
    assert result == 0
    assert account.balance == 0

from source_under_test import transfer

# ===== Tests for transfer =====
from source_under_test import BankAccount, transfer

# Kiểm tra transfer ném lỗi khi source và target là cùng một đối tượng
def test_transfer_same_account_raises_error():
    # Kiểm tra transfer(account, account, 10) ném ValueError với thông điệp "cannot transfer to same account"
    account = BankAccount(100)
    with pytest.raises(ValueError, match="cannot transfer to same account"):
        transfer(account, account, 10)

# Kiểm tra transfer thành công giữa hai tài khoản khác nhau
def test_transfer_between_different_accounts():
    # Kiểm tra transfer(source, target, 70) trả về (130, 120) khi source.balance=200, target.balance=50
    source = BankAccount(200)
    target = BankAccount(50)
    result = transfer(source, target, 70)
    assert result == (130, 120)
    assert source.balance == 130
    assert target.balance == 120

# Kiểm tra transfer với số tiền nhỏ
def test_transfer_small_amount():
    # Kiểm tra transfer với số tiền 10 từ tài khoản 100 sang 50
    source = BankAccount(100)
    target = BankAccount(50)
    result = transfer(source, target, 10)
    assert result == (90, 60)

# Kiểm tra transfer toàn bộ số dư
def test_transfer_full_balance():
    # Kiểm tra transfer toàn bộ số dư từ source sang target
    source = BankAccount(100)
    target = BankAccount(50)
    result = transfer(source, target, 100)
    assert result == (0, 150)

# Kiểm tra transfer ném lỗi khi số tiền rút không hợp lệ (source không đủ tiền)
def test_transfer_insufficient_funds():
    # Kiểm tra transfer ném lỗi khi source không đủ tiền
    source = BankAccount(30)
    target = BankAccount(50)
    with pytest.raises(ValueError, match="insufficient funds"):
        transfer(source, target, 50)
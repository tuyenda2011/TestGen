# ===== Tests for BankAccount.deposit =====
from source_under_test import BankAccount
import pytest

# Kiểm tra khởi tạo tài khoản với số dư không âm thành công
def test_bankaccount_deposit_init_non_negative_balance():
    # Kiểm tra rằng đối tượng được tạo và thuộc tính balance bằng 100
    account = BankAccount(100)
    assert account.balance == 100

# Kiểm tra khởi tạo tài khoản với số dư âm ném ra ngoại lệ
def test_bankaccount_deposit_init_negative_balance_raises():
    # Kiểm tra rằng ValueError được ném khi số dư âm
    with pytest.raises(ValueError, match="initial balance cannot be negative"):
        BankAccount(-50)

# Kiểm tra nạp tiền dương cập nhật số dư đúng
def test_bankaccount_deposit_positive_amount_updates_balance():
    # Kiểm tra phương thức trả về số dư mới và thuộc tính balance được cập nhật
    account = BankAccount(100)
    result = account.deposit(50)
    assert result == 150
    assert account.balance == 150

# Kiểm tra nạp tiền bằng hoặc nhỏ hơn không ném ra ngoại lệ
@pytest.mark.parametrize("amount", [0, -10])
def test_bankaccount_deposit_zero_or_negative_raises(amount):
    # Kiểm tra rằng ValueError được ném khi số tiền nạp không dương
    account = BankAccount(100)
    with pytest.raises(ValueError, match="deposit amount must be positive"):
        account.deposit(amount)

# ===== Tests for BankAccount.withdraw =====

# Kiểm tra rút tiền dương trong số dư thành công
def test_bankaccount_withdraw_positive_amount_within_balance():
    # Kiểm tra phương thức trả về số dư mới và thuộc tính balance được cập nhật
    account = BankAccount(200)
    result = account.withdraw(80)
    assert result == 120
    assert account.balance == 120

# Kiểm tra rút tiền bằng hoặc nhỏ hơn không ném ra ngoại lệ
@pytest.mark.parametrize("amount", [0, -10])
def test_bankaccount_withdraw_zero_or_negative_raises(amount):
    # Kiểm tra rằng ValueError được ném khi số tiền rút không dương
    account = BankAccount(200)
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        account.withdraw(amount)

# Kiểm tra rút tiền lớn hơn số dư ném ra ngoại lệ
def test_bankaccount_withdraw_amount_exceeds_balance_raises():
    # Kiểm tra rằng ValueError được ném khi không đủ số dư
    account = BankAccount(100)
    with pytest.raises(ValueError, match="insufficient funds"):
        account.withdraw(150)

from source_under_test import transfer

# ===== Tests for transfer =====
from source_under_test import BankAccount, transfer

# Kiểm tra chuyển tiền giữa hai tài khoản khác nhau thành công
def test_transfer_between_different_accounts_succeeds():
    # Kiểm tra hàm trả về tuple số dư đúng và cả hai tài khoản được cập nhật
    account1 = BankAccount(300)
    account2 = BankAccount(100)
    result = transfer(account1, account2, 50)
    assert result == (250, 150)
    assert account1.balance == 250
    assert account2.balance == 150

# Kiểm tra chuyển tiền đến cùng một tài khoản ném ra ngoại lệ
def test_transfer_to_same_account_raises():
    # Kiểm tra rằng ValueError được ném khi chuyển đến chính tài khoản nguồn
    account = BankAccount(200)
    with pytest.raises(ValueError, match="cannot transfer to same account"):
        transfer(account, account, 30)
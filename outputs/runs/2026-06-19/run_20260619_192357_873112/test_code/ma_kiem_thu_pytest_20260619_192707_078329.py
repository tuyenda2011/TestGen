# ===== Tests for BankAccount.deposit =====
from source_under_test import BankAccount
import pytest

def test_bankaccount_deposit_positive_tc003():
    """Ki?m tra n?p ti?n v?i s? ti?n duong, c?p nh?t s? du d�ng."""
    account = BankAccount(balance=100)
    new_balance = account.deposit(50)
    assert new_balance == 150
    assert account.balance == 150

def test_bankaccount_deposit_zero_amount_tc004():
    """Ki?m tra n?p ti?n v?i s? ti?n b?ng 0, ph?i n�m ValueError."""
    account = BankAccount(balance=100)
    with pytest.raises(ValueError, match="deposit amount must be positive"):
        account.deposit(0)

def test_bankaccount_deposit_negative_amount_tc005():
    """Ki?m tra n?p ti?n v?i s? ti?n �m, ph?i n�m ValueError."""
    account = BankAccount(balance=100)
    with pytest.raises(ValueError, match="deposit amount must be positive"):
        account.deposit(-20)

# ===== Tests for BankAccount.withdraw =====

def test_bankaccount_withdraw_positive_tc006():
    """Ki?m tra r�t ti?n h?p l?, s? du gi?m d�ng."""
    account = BankAccount(balance=200)
    new_balance = account.withdraw(80)
    assert new_balance == 120
    assert account.balance == 120

def test_bankaccount_withdraw_zero_amount_tc007():
    """Ki?m tra r�t ti?n v?i s? ti?n 0, ph?i n�m ValueError."""
    account = BankAccount(balance=200)
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        account.withdraw(0)

def test_bankaccount_withdraw_negative_amount_tc008():
    """Ki?m tra r�t ti?n v?i s? ti?n �m, ph?i n�m ValueError."""
    account = BankAccount(balance=200)
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        account.withdraw(-30)

def test_bankaccount_withdraw_insufficient_funds_tc009():
    """Ki?m tra r�t ti?n vu?t qu� s? du, ph?i n�m ValueError."""
    account = BankAccount(balance=100)
    with pytest.raises(ValueError, match="insufficient funds"):
        account.withdraw(150)

# ===== Tests for transfer =====
from source_under_test import transfer, BankAccount

def test_transfer_successful_tc010():
    """Ki?m tra chuy?n ti?n th�nh c�ng gi?a hai t�i kho?n kh�c nhau."""
    source = BankAccount(balance=300)
    target = BankAccount(balance=50)
    result = transfer(source, target, 100)
    assert result == (200, 150)
    assert source.balance == 200
    assert target.balance == 150

def test_transfer_same_account_tc011():
    """Ki?m tra chuy?n ti?n t?i c�ng m?t t�i kho?n, ph?i n�m ValueError."""
    account = BankAccount(balance=200)
    with pytest.raises(ValueError, match="cannot transfer to same account"):
        transfer(account, account, 50)

def test_transfer_insufficient_funds_tc012():
    """Ki?m tra chuy?n ti?n khi s? du ngu?n kh�ng d?, ph?i n�m ValueError t? withdraw."""
    source = BankAccount(balance=40)
    target = BankAccount(balance=10)
    with pytest.raises(ValueError, match="insufficient funds"):
        transfer(source, target, 60)

def test_transfer_zero_amount_tc013():
    """Ki?m tra chuy?n ti?n v?i s? ti?n 0, g�y l?i withdraw amount must be positive."""
    source = BankAccount(balance=100)
    target = BankAccount(balance=100)
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        transfer(source, target, 0)

# ===== Traceability top-up tests =====

# Covers constructor validation branch around source line 4.

def test_bankaccount_init_valid_tc_001():  # TC-001
    account = BankAccount(balance=100)
    assert account.balance == 100

def test_bankaccount_init_negative_tc_002():  # TC-002
    with pytest.raises(ValueError, match='initial balance cannot be negative'):
        BankAccount(balance=-1)
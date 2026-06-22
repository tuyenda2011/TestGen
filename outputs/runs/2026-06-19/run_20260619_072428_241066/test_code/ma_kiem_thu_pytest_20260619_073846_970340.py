# ===== Tests for BankAccount.deposit =====
from source_under_test import BankAccount

def test_bankaccount_deposit_TC001():
    # Ki?m tra kh?i t?o t�i kho?n v?i s? du h?p l?.
    account = BankAccount(100)
    assert account.balance == 100

def test_bankaccount_deposit_TC002():
    # Ki?m tra kh?i t?o t�i kho?n v?i s? du �m, ph?i n�m ValueError.
    import pytest
    with pytest.raises(ValueError, match="initial balance cannot be negative"):
        BankAccount(-50)

def test_bankaccount_deposit_TC003():
    # Ki?m tra n?p ti?n s? du duong, tr? v? s? du m?i.
    account = BankAccount(100)
    result = account.deposit(50)
    assert result == 150
    assert account.balance == 150

def test_bankaccount_deposit_TC004():
    # Ki?m tra n?p ti?n s? 0, ph?i n�m ValueError.
    import pytest
    account = BankAccount(100)
    with pytest.raises(ValueError, match="deposit amount must be positive"):
        account.deposit(0)

def test_bankaccount_deposit_TC005():
    # Ki?m tra n?p ti?n s? �m, ph?i n�m ValueError.
    import pytest
    account = BankAccount(100)
    with pytest.raises(ValueError, match="deposit amount must be positive"):
        account.deposit(-20)

# ===== Tests for BankAccount.withdraw =====

def test_bankaccount_withdraw_TC006():
    # Ki?m tra r�t ti?n h?p l? nh? hon s? du, tr? v? s? du m?i.
    account = BankAccount(200)
    result = account.withdraw(80)
    assert result == 120
    assert account.balance == 120

def test_bankaccount_withdraw_TC007():
    # Ki?m tra r�t ti?n s? 0, ph?i n�m ValueError.
    import pytest
    account = BankAccount(200)
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        account.withdraw(0)

def test_bankaccount_withdraw_TC008():
    # Ki?m tra r�t ti?n s? �m, ph?i n�m ValueError.
    import pytest
    account = BankAccount(200)
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        account.withdraw(-30)

def test_bankaccount_withdraw_TC009():
    # Ki?m tra r�t ti?n l?n hon s? du, ph?i n�m ValueError.
    import pytest
    account = BankAccount(150)
    with pytest.raises(ValueError, match="insufficient funds"):
        account.withdraw(200)

from source_under_test import transfer

# ===== Tests for transfer =====
from source_under_test import BankAccount, transfer

def test_transfer_TC010():
    # Ki?m tra chuy?n ti?n gi?a hai t�i kho?n kh�c nhau, tr? v? tuple s? du.
    source = BankAccount(300)
    target = BankAccount(100)
    result = transfer(source, target, 120)
    assert result == (180, 220)
    assert source.balance == 180
    assert target.balance == 220

def test_transfer_TC011():
    # Ki?m tra chuy?n ti?n cho c�ng m?t t�i kho?n, ph?i n�m ValueError.
    import pytest
    account = BankAccount(200)
    with pytest.raises(ValueError, match="cannot transfer to same account"):
        transfer(account, account, 50)

def test_transfer_TC012():
    # Ki?m tra chuy?n ti?n l?n hon s? du ngu?n, ph?i n�m ValueError.
    import pytest
    source = BankAccount(80)
    target = BankAccount(50)
    with pytest.raises(ValueError, match="insufficient funds"):
        transfer(source, target, 100)

def test_transfer_TC013():
    # Ki?m tra chuy?n ti?n s? 0, ph?i n�m ValueError do withdraw validation.
    import pytest
    source = BankAccount(150)
    target = BankAccount(150)
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        transfer(source, target, 0)

def test_transfer_TC014():
    # Ki?m tra chuy?n ti?n s? �m, ph?i n�m ValueError do withdraw validation.
    import pytest
    source = BankAccount(150)
    target = BankAccount(150)
    with pytest.raises(ValueError, match="withdraw amount must be positive"):
        transfer(source, target, -20)
// Plan: TC-001, TC-002, TC-003, TC-004

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.Executable;
import static org.junit.jupiter.api.Assertions.*;

public class BankAccountTest {

    // TC-001: Kiểm tra getter getAccountNumber trả về accountNumber đã khởi tạo
    @Test
    void TC_001_getAccountNumber_returnsInitializedAccountNumber() {
        BankAccount account = new BankAccount("ACC123", 0.0);
        assertEquals("ACC123", account.getAccountNumber());
    }

    // TC-002: Kiểm tra getter getBalance trả về số dư hiện tại
    @Test
    void TC_002_getBalance_returnsCurrentBalance() {
        BankAccount account = new BankAccount("ACC456", 500.0);
        assertEquals(500.0, account.getBalance(), 0.001);
    }

    // TC-003: Kiểm tra getter isActive trả về true cho tài khoản mới được tạo
    @Test
    void TC_003_isActive_returnsTrueForNewlyCreatedAccount() {
        BankAccount account = new BankAccount("ACC789", 0.0);
        assertTrue(account.isActive());
    }

    // TC-004: Kiểm tra checkActive ném IllegalStateException khi tài khoản không active
    @Test
    void TC_004_checkActive_throwsExceptionWhenAccountInactive() {
        BankAccount account = new BankAccount("ACC000", 0.0);
        account.deactivate();
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> account.deposit(100.0));
        assertEquals("Account is inactive", exception.getMessage());
    }


    // ===== Targeted retry tests =====

// TC-005: Kiểm tra constructor ném IllegalArgumentException khi accountNumber là null
    @Test
    void COV_retry_2_constructor_throwsExceptionWhenAccountNumberNull() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> new BankAccount(null, 0.0));
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    // TC-006: Kiểm tra constructor ném IllegalArgumentException khi accountNumber là chuỗi rỗng
    @Test
    void COV_retry_2_constructor_throwsExceptionWhenAccountNumberEmpty() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> new BankAccount("", 0.0));
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    // TC-007: Kiểm tra constructor ném IllegalArgumentException khi accountNumber chỉ có khoảng trắng
    @Test
    void COV_retry_2_constructor_throwsExceptionWhenAccountNumberWhitespace() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> new BankAccount("   ", 0.0));
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    // TC-008: Kiểm tra constructor ném IllegalArgumentException khi initialBalance âm
    @Test
    void COV_retry_2_constructor_throwsExceptionWhenInitialBalanceNegative() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> new BankAccount("ACC123", -100.0));
        assertEquals("Initial balance cannot be negative", exception.getMessage());
    }

    // TC-009: Kiểm tra deposit thành công tăng số dư
    @Test
    void COV_retry_2_deposit_successIncreasesBalance() {
        BankAccount account = new BankAccount("ACC123", 100.0);
        account.deposit(50.0);
        assertEquals(150.0, account.getBalance(), 0.001);
    }

    // TC-010: Kiểm tra deposit ném IllegalArgumentException khi amount bằng 0
    @Test
    void COV_retry_2_deposit_throwsExceptionWhenAmountZero() {
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> account.deposit(0.0));
        assertEquals("Deposit amount must be positive", exception.getMessage());
    }

    // TC-011: Kiểm tra deposit ném IllegalArgumentException khi amount âm
    @Test
    void COV_retry_2_deposit_throwsExceptionWhenAmountNegative() {
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> account.deposit(-50.0));
        assertEquals("Deposit amount must be positive", exception.getMessage());
    }

    // TC-012: Kiểm tra withdraw thành công giảm số dư
    @Test
    void COV_retry_2_withdraw_successDecreasesBalance() {
        BankAccount account = new BankAccount("ACC123", 100.0);
        account.withdraw(50.0);
        assertEquals(50.0, account.getBalance(), 0.001);
    }

    // TC-013: Kiểm tra withdraw ném IllegalArgumentException khi amount bằng 0
    @Test
    void COV_retry_2_withdraw_throwsExceptionWhenAmountZero() {
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> account.withdraw(0.0));
        assertEquals("Withdraw amount must be positive", exception.getMessage());
    }

    // TC-014: Kiểm tra withdraw ném IllegalArgumentException khi amount âm
    @Test
    void COV_retry_2_withdraw_throwsExceptionWhenAmountNegative() {
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> account.withdraw(-50.0));
        assertEquals("Withdraw amount must be positive", exception.getMessage());
    }

    // TC-015: Kiểm tra withdraw ném IllegalStateException khi số dư không đủ
    @Test
    void COV_retry_2_withdraw_throwsExceptionWhenInsufficientFunds() {
        BankAccount account = new BankAccount("ACC123", 50.0);
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> account.withdraw(100.0));
        assertEquals("Insufficient funds", exception.getMessage());
    }

    // TC-016: Kiểm tra withdraw ném IllegalStateException khi tài khoản không active
    @Test
    void COV_retry_2_withdraw_throwsExceptionWhenAccountInactive() {
        BankAccount account = new BankAccount("ACC123", 0.0);
        account.deactivate();
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> account.withdraw(50.0));
        assertEquals("Account is inactive", exception.getMessage());
    }

    // TC-017: Kiểm tra transfer ném IllegalArgumentException khi targetAccount là null
    @Test
    void COV_retry_2_transfer_throwsExceptionWhenTargetAccountNull() {
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> account.transfer(null, 50.0));
        assertEquals("Target account cannot be null", exception.getMessage());
    }

    // TC-018: Kiểm tra transfer ném IllegalStateException khi targetAccount không active
    @Test
    void COV_retry_2_transfer_throwsExceptionWhenTargetAccountInactive() {
        BankAccount sourceAccount = new BankAccount("ACC123", 100.0);
        BankAccount targetAccount = new BankAccount("ACC456", 0.0);
        targetAccount.deactivate();
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> sourceAccount.transfer(targetAccount, 50.0));
        assertEquals("Target account is inactive", exception.getMessage());
    }

    // TC-019: Kiểm tra transfer thành công chuyển tiền giữa hai tài khoản
    @Test
    void COV_retry_2_transfer_successTransfersBetweenAccounts() {
        BankAccount sourceAccount = new BankAccount("ACC123", 100.0);
        BankAccount targetAccount = new BankAccount("ACC456", 50.0);
        sourceAccount.transfer(targetAccount, 30.0);
        assertEquals(70.0, sourceAccount.getBalance(), 0.001);
        assertEquals(80.0, targetAccount.getBalance(), 0.001);
    }

    // TC-020: Kiểm tra deactivate thành công khi số dư bằng 0
    @Test
    void COV_retry_2_deactivate_successWhenBalanceZero() {
        BankAccount account = new BankAccount("ACC123", 0.0);
        account.deactivate();
        assertFalse(account.isActive());
    }

    // TC-021: Kiểm tra deactivate ném IllegalStateException khi số dư dương
    @Test
    void COV_retry_2_deactivate_throwsExceptionWhenBalancePositive() {
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> account.deactivate());
        assertEquals("Cannot deactivate account with non-zero balance", exception.getMessage());
    }
}
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

class BankAccountTest {

    @Test
    @DisplayName("TC-001: Verify getAccountNumber returns the initialized account number")
    void getAccountNumber_validInput_returnsAccountNumber() {
        // Kiểm tra phương thức getAccountNumber trả về số tài khoản đúng
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertEquals("ACC123", account.getAccountNumber());
    }

    @Test
    @DisplayName("TC-002: Verify getBalance returns the initialized balance")
    void getBalance_validInput_returnsBalance() {
        // Kiểm tra phương thức getBalance trả về số dư đúng
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertEquals(1000.0, account.getBalance(), 0.001);
    }

    @Test
    @DisplayName("TC-003: Verify isActive returns true for newly created active account")
    void isActive_newAccount_returnsTrue() {
        // Kiểm tra tài khoản mới được tạo có trạng thái hoạt động là true
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertTrue(account.isActive());
    }

    @Test
    @DisplayName("TC-006: Constructor throws IllegalArgumentException for null account number")
    void constructor_nullAccountNumber_throwsException() {
        // Kiểm tra constructor ném IllegalArgumentException khi accountNumber là null
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount(null, 100.0);
        });
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    @Test
    @DisplayName("TC-007: Constructor throws IllegalArgumentException for empty account number")
    void constructor_emptyAccountNumber_throwsException() {
        // Kiểm tra constructor ném IllegalArgumentException khi accountNumber rỗng
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount("   ", 100.0);
        });
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    @Test
    @DisplayName("TC-008: Constructor throws IllegalArgumentException for negative initial balance")
    void constructor_negativeInitialBalance_throwsException() {
        // Kiểm tra constructor ném IllegalArgumentException khi initialBalance âm
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount("ACC123", -50.0);
        });
        assertEquals("Initial balance cannot be negative", exception.getMessage());
    }

    @Test
    @DisplayName("TC-009: deposit throws IllegalArgumentException for non-positive amount")
    void deposit_nonPositiveAmount_throwsException() {
        // Kiểm tra deposit ném IllegalArgumentException khi số tiền không dương
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            account.deposit(0.0);
        });
        assertEquals("Deposit amount must be positive", exception.getMessage());
    }

    @Test
    @DisplayName("TC-010: withdraw throws IllegalArgumentException for non-positive amount")
    void withdraw_nonPositiveAmount_throwsException() {
        // Kiểm tra withdraw ném IllegalArgumentException khi số tiền không dương
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            account.withdraw(-10.0);
        });
        assertEquals("Withdraw amount must be positive", exception.getMessage());
    }

    @Test
    @DisplayName("TC-011: withdraw throws IllegalStateException when insufficient funds")
    void withdraw_insufficientFunds_throwsException() {
        // Kiểm tra withdraw ném IllegalStateException khi số dư không đủ
        BankAccount account = new BankAccount("ACC123", 50.0);
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            account.withdraw(100.0);
        });
        assertEquals("Insufficient funds", exception.getMessage());
    }

    @Test
    @DisplayName("TC-012: transfer throws IllegalArgumentException when target account is null")
    void transfer_nullTargetAccount_throwsException() {
        // Kiểm tra transfer ném IllegalArgumentException khi tài khoản đích là null
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            account.transfer(null, 10.0);
        });
        assertEquals("Target account cannot be null", exception.getMessage());
    }

    @Test
    @DisplayName("TC-013: transfer throws IllegalStateException when target account is inactive")
    void transfer_inactiveTargetAccount_throwsException() {
        // Kiểm tra transfer ném IllegalStateException khi tài khoản đích không hoạt động
        BankAccount source = new BankAccount("ACC123", 100.0);
        BankAccount target = new BankAccount("ACC456", 0.0);
        target.deactivate();
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            source.transfer(target, 10.0);
        });
        assertEquals("Target account is inactive", exception.getMessage());
    }

    @Test
    @DisplayName("TC-014: deactivate throws IllegalStateException when balance is non-zero")
    void deactivate_nonZeroBalance_throwsException() {
        // Kiểm tra deactivate ném IllegalStateException khi số dư không bằng 0
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            account.deactivate();
        });
        assertEquals("Cannot deactivate account with non-zero balance", exception.getMessage());
    }

    @Test
    @DisplayName("TC-015: deactivate succeeds when balance is zero")
    void deactivate_zeroBalance_succeeds() {
        // Kiểm tra deactivate thành công khi số dư bằng 0
        BankAccount account = new BankAccount("ACC123", 0.0);
        account.deactivate();
        assertFalse(account.isActive());
    }

    @Test
    @DisplayName("TC-004: deposit throws IllegalStateException when account is inactive")
    void deposit_inactiveAccount_throwsException() {
        // Kiểm tra deposit ném IllegalStateException khi tài khoản không hoạt động
        BankAccount account = new BankAccount("ACC123", 0.0);
        account.deactivate();
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            account.deposit(100.0);
        });
        assertEquals("Account is inactive", exception.getMessage());
    }

    @Test
    @DisplayName("TC-005: withdraw does not throw when account is active")
    void withdraw_activeAccount_succeeds() {
        // Kiểm tra withdraw thành công khi tài khoản hoạt động
        BankAccount account = new BankAccount("ACC123", 200.0);
        account.withdraw(100.0);
        assertEquals(100.0, account.getBalance(), 0.001);
    }

    @Test
    @DisplayName("TC-004: withdraw throws IllegalStateException when account is inactive")
    void withdraw_inactiveAccount_throwsException() {
        // Kiểm tra withdraw ném IllegalStateException khi tài khoản không hoạt động
        BankAccount account = new BankAccount("ACC123", 0.0);
        account.deactivate();
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            account.withdraw(100.0);
        });
        assertEquals("Account is inactive", exception.getMessage());
    }

    @Test
    @DisplayName("TC-004: transfer throws IllegalStateException when account is inactive")
    void transfer_inactiveSourceAccount_throwsException() {
        // Kiểm tra transfer ném IllegalStateException khi tài khoản nguồn không hoạt động
        BankAccount source = new BankAccount("ACC123", 0.0);
        source.deactivate();
        BankAccount target = new BankAccount("ACC456", 0.0);
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            source.transfer(target, 10.0);
        });
        assertEquals("Account is inactive", exception.getMessage());
    }
}
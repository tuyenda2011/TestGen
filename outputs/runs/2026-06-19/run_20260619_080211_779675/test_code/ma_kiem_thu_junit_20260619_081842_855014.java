// Plan: TC-006, TC-007, TC-008, TC-009
// Skipped TC-001 to TC-005, TC-010 to TC-013: out_of_scope (JUnit framework features) or clarification

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BankAccountTest {

    // TC-006: Kiểm tra các getter của BankAccount trả về đúng giá trị trường nội bộ
    @Test
    void TC_006_gettersReturnInitializedFieldValues() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        
        assertEquals("ACC123", account.getAccountNumber(), "getAccountNumber should return the account number");
        assertEquals(1000.0, account.getBalance(), 0.001, "getBalance should return the initial balance");
        assertTrue(account.isActive(), "isActive should return true for newly created account");
    }

    // TC-007: checkActive ném IllegalStateException khi tài khoản không active
    @Test
    void TC_007_checkActiveThrowsExceptionWhenAccountInactive() {
        BankAccount account = createInactiveAccount("ACC456", 0.0);
        
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            account.withdraw(10);
        }, "withdraw should throw IllegalStateException when account is inactive");
        
        assertEquals("Account is inactive", exception.getMessage(), "Exception message should be 'Account is inactive'");
    }

    // TC-008: Deposit với số tiền không dương ném IllegalArgumentException
    @Test
    void TC_008_depositNonPositiveAmountThrowsException() {
        BankAccount account = new BankAccount("ACC789", 100.0);
        
        IllegalArgumentException exceptionZero = assertThrows(IllegalArgumentException.class, () -> {
            account.deposit(0);
        }, "deposit(0) should throw IllegalArgumentException");
        
        assertEquals("Deposit amount must be positive", exceptionZero.getMessage());
        
        IllegalArgumentException exceptionNegative = assertThrows(IllegalArgumentException.class, () -> {
            account.deposit(-5);
        }, "deposit(-5) should throw IllegalArgumentException");
        
        assertEquals("Deposit amount must be positive", exceptionNegative.getMessage());
    }

    // TC-009: Withdraw vượt quá số dư ném IllegalStateException
    @Test
    void TC_009_withdrawMoreThanBalanceThrowsException() {
        BankAccount account = new BankAccount("ACC999", 50.0);
        
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            account.withdraw(100);
        }, "withdraw(100) should throw IllegalStateException when balance is 50.0");
        
        assertEquals("Insufficient funds", exception.getMessage(), "Exception message should be 'Insufficient funds'");
    }

    // TC-COV-001: Kiểm tra constructor ném IllegalArgumentException khi accountNumber là null
    @Test
    void COV_001_constructorThrowsExceptionForNullAccountNumber() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount(null, 100.0);
        }, "Constructor should throw IllegalArgumentException when accountNumber is null");
        
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    // TC-COV-002: Kiểm tra constructor ném IllegalArgumentException khi accountNumber là chuỗi rỗng
    @Test
    void COV_002_constructorThrowsExceptionForEmptyAccountNumber() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount("", 100.0);
        }, "Constructor should throw IllegalArgumentException when accountNumber is empty");
        
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    // TC-COV-003: Kiểm tra constructor ném IllegalArgumentException khi accountNumber chỉ có khoảng trắng
    @Test
    void COV_003_constructorThrowsExceptionForWhitespaceAccountNumber() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount("   ", 100.0);
        }, "Constructor should throw IllegalArgumentException when accountNumber is whitespace only");
        
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    // TC-COV-004: Kiểm tra constructor ném IllegalArgumentException khi initialBalance âm
    @Test
    void COV_004_constructorThrowsExceptionForNegativeInitialBalance() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            new BankAccount("ACC001", -100.0);
        }, "Constructor should throw IllegalArgumentException when initialBalance is negative");
        
        assertEquals("Initial balance cannot be negative", exception.getMessage());
    }

    // TC-COV-005: Kiểm tra withdraw với số tiền không dương ném IllegalArgumentException
    @Test
    void COV_005_withdrawNonPositiveAmountThrowsException() {
        BankAccount account = new BankAccount("ACC002", 100.0);
        
        IllegalArgumentException exceptionZero = assertThrows(IllegalArgumentException.class, () -> {
            account.withdraw(0);
        }, "withdraw(0) should throw IllegalArgumentException");
        
        assertEquals("Withdraw amount must be positive", exceptionZero.getMessage());
        
        IllegalArgumentException exceptionNegative = assertThrows(IllegalArgumentException.class, () -> {
            account.withdraw(-10);
        }, "withdraw(-10) should throw IllegalArgumentException");
        
        assertEquals("Withdraw amount must be positive", exceptionNegative.getMessage());
    }

    // TC-COV-006: Kiểm tra transfer với target account null ném IllegalArgumentException
    @Test
    void COV_006_transferWithNullTargetThrowsException() {
        BankAccount account = new BankAccount("ACC003", 100.0);
        
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> {
            account.transfer(null, 50.0);
        }, "transfer with null target should throw IllegalArgumentException");
        
        assertEquals("Target account cannot be null", exception.getMessage());
    }

    // TC-COV-007: Kiểm tra transfer tới tài khoản không active ném IllegalStateException
    @Test
    void COV_007_transferToInactiveTargetThrowsException() {
        BankAccount source = new BankAccount("ACC004", 100.0);
        BankAccount target = createInactiveAccount("ACC005", 0.0);
        
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            source.transfer(target, 50.0);
        }, "transfer to inactive account should throw IllegalStateException");
        
        assertEquals("Target account is inactive", exception.getMessage());
    }

    // TC-COV-008: Kiểm tra deactivate với số dư không bằng 0 ném IllegalStateException
    @Test
    void COV_008_deactivateWithNonZeroBalanceThrowsException() {
        BankAccount account = new BankAccount("ACC006", 100.0);
        
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> {
            account.deactivate();
        }, "deactivate with non-zero balance should throw IllegalStateException");
        
        assertEquals("Cannot deactivate account with non-zero balance", exception.getMessage());
    }

    // TC-COV-009: Kiểm tra deactivate thành công khi số dư bằng 0
    @Test
    void COV_009_deactivateSucceedsWithZeroBalance() {
        BankAccount account = new BankAccount("ACC007", 0.0);
        
        assertTrue(account.isActive(), "Account should be active initially");
        account.deactivate();
        assertFalse(account.isActive(), "Account should be inactive after deactivate");
    }

    // TC-COV-010: Kiểm tra deposit tăng balance đúng
    @Test
    void COV_010_depositIncreasesBalance() {
        BankAccount account = new BankAccount("ACC008", 100.0);
        
        account.deposit(50.0);
        assertEquals(150.0, account.getBalance(), 0.001, "Balance should increase by deposit amount");
    }

    // TC-COV-011: Kiểm tra withdraw giảm balance đúng
    @Test
    void COV_011_withdrawDecreasesBalance() {
        BankAccount account = new BankAccount("ACC009", 100.0);
        
        account.withdraw(30.0);
        assertEquals(70.0, account.getBalance(), 0.001, "Balance should decrease by withdraw amount");
    }

    // TC-COV-012: Kiểm tra transfer chuyển tiền giữa hai tài khoản
    @Test
    void COV_012_transferMovesMoneyBetweenAccounts() {
        BankAccount source = new BankAccount("ACC010", 100.0);
        BankAccount target = new BankAccount("ACC011", 50.0);
        
        source.transfer(target, 30.0);
        
        assertEquals(70.0, source.getBalance(), 0.001, "Source balance should decrease by transfer amount");
        assertEquals(80.0, target.getBalance(), 0.001, "Target balance should increase by transfer amount");
    }

    // Helper method để tạo tài khoản không active, giảm phụ thuộc vào việc gọi deactivate() sau khi tạo
    private BankAccount createInactiveAccount(String accountNumber, double balance) {
        BankAccount account = new BankAccount(accountNumber, balance);
        account.deactivate();
        return account;
    }
}
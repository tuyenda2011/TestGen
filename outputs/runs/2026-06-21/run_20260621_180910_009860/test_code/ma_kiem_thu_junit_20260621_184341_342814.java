import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Test class cho BankAccount - kiểm thử các chức năng tài khoản ngân hàng
 */
class BankAccountTest {

    // TC-001: Tạo tài khoản với accountNumber và initialBalance hợp lệ
    @Test
    @DisplayName("TC-001: Create BankAccount with valid accountNumber and non-negative initialBalance")
    void testCreateAccountWithValidParameters() {
        BankAccount account = new BankAccount("ACC12345", 1000.0);
        assertTrue(account.isActive(), "Tài khoản mới tạo phải ở trạng thái hoạt động");
        assertEquals(1000.0, account.getBalance(), 0.001, "Số dư ban đầu phải bằng initialBalance");
        assertEquals("ACC12345", account.getAccountNumber(), "Số tài khoản phải trả về đúng giá trị đã truyền");
    }

    // TC-002: Constructor ném IllegalArgumentException khi accountNumber là null
    @Test
    @DisplayName("TC-002: Constructor throws IllegalArgumentException when accountNumber is null")
    void testConstructorThrowsWhenAccountNumberIsNull() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, 
            () -> new BankAccount(null, 500.0));
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    // TC-003: Constructor ném IllegalArgumentException khi accountNumber là chuỗi rỗng
    @Test
    @DisplayName("TC-003: Constructor throws IllegalArgumentException when accountNumber is empty string")
    void testConstructorThrowsWhenAccountNumberIsEmpty() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, 
            () -> new BankAccount("", 500.0));
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    // TC-004: Constructor ném IllegalArgumentException khi accountNumber chỉ chứa khoảng trắng
    @Test
    @DisplayName("TC-004: Constructor throws IllegalArgumentException when accountNumber contains only whitespace")
    void testConstructorThrowsWhenAccountNumberIsWhitespaceOnly() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, 
            () -> new BankAccount("   ", 500.0));
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    // TC-005: Constructor ném IllegalArgumentException khi initialBalance âm
    @Test
    @DisplayName("TC-005: Constructor throws IllegalArgumentException when initialBalance is negative")
    void testConstructorThrowsWhenInitialBalanceIsNegative() {
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, 
            () -> new BankAccount("ACC98765", -10.0));
        assertEquals("Initial balance cannot be negative", exception.getMessage());
    }

    // TC-006: getAccountNumber trả về đúng giá trị đã truyền vào constructor
    @Test
    @DisplayName("TC-006: getAccountNumber returns the exact value passed to constructor")
    void testGetAccountNumberReturnsCorrectValue() {
        BankAccount account = new BankAccount("ACC001", 0.0);
        assertEquals("ACC001", account.getAccountNumber(), "Phải trả về đúng số tài khoản đã khởi tạo");
    }

    // TC-007: isActive trả về true cho tài khoản vừa được tạo
    @Test
    @DisplayName("TC-007: isActive returns true for a newly created valid account")
    void testIsActiveReturnsTrueForNewAccount() {
        BankAccount account = new BankAccount("ACC002", 0.0);
        assertTrue(account.isActive(), "Tài khoản mới tạo phải ở trạng thái hoạt động");
    }

    // TC-008: Nạp tiền dương cập nhật số dư đúng
    @Test
    @DisplayName("TC-008: Deposit a positive amount updates balance correctly")
    void testDepositPositiveAmountUpdatesBalance() {
        BankAccount account = new BankAccount("ACC003", 200.0);
        account.deposit(150.0);
        assertEquals(350.0, account.getBalance(), 0.001, "Số dư sau deposit phải là 350.0");
    }

    // TC-009: Deposit ném IllegalArgumentException khi amount bằng 0
    @Test
    @DisplayName("TC-009: Deposit throws IllegalArgumentException when amount is zero")
    void testDepositThrowsWhenAmountIsZero() {
        BankAccount account = new BankAccount("ACC004", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, 
            () -> account.deposit(0.0));
        assertEquals("Deposit amount must be positive", exception.getMessage());
    }

    // TC-010: Deposit ném IllegalArgumentException khi amount âm
    @Test
    @DisplayName("TC-010: Deposit throws IllegalArgumentException when amount is negative")
    void testDepositThrowsWhenAmountIsNegative() {
        BankAccount account = new BankAccount("ACC005", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, 
            () -> account.deposit(-50.0));
        assertEquals("Deposit amount must be positive", exception.getMessage());
    }

    // TC-011: Rút tiền hợp lệ giảm số dư đúng
    @Test
    @DisplayName("TC-011: Withdraw a valid amount reduces balance correctly")
    void testWithdrawValidAmountReducesBalance() {
        BankAccount account = new BankAccount("ACC006", 500.0);
        account.withdraw(200.0);
        assertEquals(300.0, account.getBalance(), 0.001, "Số dư sau withdraw phải là 300.0");
    }

    // TC-012: Withdraw ném IllegalArgumentException khi amount bằng 0
    @Test
    @DisplayName("TC-012: Withdraw throws IllegalArgumentException when amount is zero")
    void testWithdrawThrowsWhenAmountIsZero() {
        BankAccount account = new BankAccount("ACC007", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, 
            () -> account.withdraw(0.0));
        assertEquals("Withdraw amount must be positive", exception.getMessage());
    }

    // TC-013: Withdraw ném IllegalArgumentException khi amount âm
    @Test
    @DisplayName("TC-013: Withdraw throws IllegalArgumentException when amount is negative")
    void testWithdrawThrowsWhenAmountIsNegative() {
        BankAccount account = new BankAccount("ACC008", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, 
            () -> account.withdraw(-30.0));
        assertEquals("Withdraw amount must be positive", exception.getMessage());
    }

    // TC-014: Withdraw ném IllegalStateException khi amount vượt quá số dư
    @Test
    @DisplayName("TC-014: Withdraw throws IllegalStateException when amount exceeds current balance")
    void testWithdrawThrowsWhenInsufficientFunds() {
        BankAccount account = new BankAccount("ACC009", 100.0);
        IllegalStateException exception = assertThrows(IllegalStateException.class, 
            () -> account.withdraw(150.0));
        assertEquals("Insufficient funds", exception.getMessage());
    }

    // TC-015: Chuyển tiền thành công cập nhật số dư của cả hai tài khoản
    @Test
    @DisplayName("TC-015: Transfer a positive amount to an active target account updates both balances")
    void testTransferToActiveTargetUpdatesBothBalances() {
        BankAccount source = new BankAccount("SRC", 400.0);
        BankAccount target = new BankAccount("TGT", 100.0);
        source.transfer(target, 150.0);
        assertEquals(250.0, source.getBalance(), 0.001, "Số dư tài khoản nguồn phải là 250.0");
        assertEquals(250.0, target.getBalance(), 0.001, "Số dư tài khoản đích phải là 250.0");
    }

    // TC-016: Transfer ném IllegalArgumentException khi targetAccount là null
    @Test
    @DisplayName("TC-016: Transfer throws IllegalArgumentException when targetAccount is null")
    void testTransferThrowsWhenTargetAccountIsNull() {
        BankAccount source = new BankAccount("SRC", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, 
            () -> source.transfer(null, 50.0));
        assertEquals("Target account cannot be null", exception.getMessage());
    }

    // TC-017: Transfer ném IllegalStateException khi tài khoản đích không hoạt động
    @Test
    @DisplayName("TC-017: Transfer throws IllegalStateException when target account is inactive")
    void testTransferThrowsWhenTargetAccountIsInactive() {
        BankAccount source = new BankAccount("SRC", 100.0);
        BankAccount target = new BankAccount("TGT", 0.0);
        target.deactivate();
        IllegalStateException exception = assertThrows(IllegalStateException.class, 
            () -> source.transfer(target, 30.0));
        assertEquals("Target account is inactive", exception.getMessage());
    }

    // TC-018: Transfer ném IllegalArgumentException khi amount bằng 0
    @Test
    @DisplayName("TC-018: Transfer throws IllegalArgumentException when amount is zero")
    void testTransferThrowsWhenAmountIsZero() {
        BankAccount source = new BankAccount("SRC", 100.0);
        BankAccount target = new BankAccount("TGT", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, 
            () -> source.transfer(target, 0.0));
        assertEquals("Withdraw amount must be positive", exception.getMessage());
    }

    // TC-019: Transfer ném IllegalArgumentException khi amount âm
    @Test
    @DisplayName("TC-019: Transfer throws IllegalArgumentException when amount is negative")
    void testTransferThrowsWhenAmountIsNegative() {
        BankAccount source = new BankAccount("SRC", 100.0);
        BankAccount target = new BankAccount("TGT", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, 
            () -> source.transfer(target, -20.0));
        assertEquals("Withdraw amount must be positive", exception.getMessage());
    }

    // TC-020: Deactivate ném IllegalStateException khi số dư > 0
    @Test
    @DisplayName("TC-020: Deactivate throws IllegalStateException when balance is greater than zero")
    void testDeactivateThrowsWhenBalanceIsGreaterThanZero() {
        BankAccount account = new BankAccount("ACC010", 100.0);
        IllegalStateException exception = assertThrows(IllegalStateException.class, 
            () -> account.deactivate());
        assertEquals("Cannot deactivate account with non-zero balance", exception.getMessage());
    }
}
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

public class BankAccountTest {

    // Kiểm tra getAccountNumber trả về đúng số tài khoản sau khi tạo
    @Test
    @DisplayName("TC-001: Verify getAccountNumber returns correct account number after construction")
    void testGetAccountNumber() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertEquals("ACC123", account.getAccountNumber());
    }

    // Kiểm tra getBalance trả về đúng số dư ban đầu sau khi tạo
    @Test
    @DisplayName("TC-002: Verify getBalance returns correct initial balance after construction")
    void testGetBalance() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertEquals(1000.0, account.getBalance(), 0.001);
    }

    // Kiểm tra isActive trả về true cho tài khoản mới tạo
    @Test
    @DisplayName("TC-003: Verify isActive returns true for newly created account")
    void testIsActiveTrue() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertTrue(account.isActive());
    }

    // Kiểm tra checkActive không ném ngoại lệ khi tài khoản đang hoạt động
    @Test
    @DisplayName("TC-004: Verify checkActive does not throw exception when account is active")
    void testCheckActiveNoException() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertDoesNotThrow(() -> account.deposit(100.0));
    }

    // Kiểm tra checkActive ném IllegalStateException khi tài khoản không hoạt động
    @Test
    @DisplayName("TC-005: Verify checkActive throws IllegalStateException when account is inactive")
    void testCheckActiveThrowsException() {
        BankAccount account = new BankAccount("ACC123", 0.0);
        account.deactivate();
        assertThrows(IllegalStateException.class, () -> account.deposit(100.0));
    }

    // Kiểm tra isActive trả về false sau khi gọi deactivate
    @Test
    @DisplayName("TC-006: Verify isActive returns false after calling deactivate")
    void testIsActiveFalseAfterDeactivate() {
        BankAccount account = new BankAccount("ACC123", 0.0);
        account.deactivate();
        assertFalse(account.isActive());
    }

    // Kiểm tra deposit tăng số dư cho tài khoản đang hoạt động
    @Test
    @DisplayName("TC-007: Verify deposit increases balance for active account")
    void testDepositIncreasesBalance() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        account.deposit(500.0);
        assertEquals(1500.0, account.getBalance(), 0.001);
    }

    // Kiểm tra deposit ném IllegalArgumentException cho số tiền âm
    @Test
    @DisplayName("TC-008: Verify deposit throws exception for negative amount")
    void testDepositNegativeAmount() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertThrows(IllegalArgumentException.class, () -> account.deposit(-100.0));
    }

    // Kiểm tra deposit ném IllegalStateException khi tài khoản không hoạt động
    @Test
    @DisplayName("TC-009: Verify deposit throws exception when account is inactive")
    void testDepositInactiveAccount() {
        BankAccount account = new BankAccount("ACC123", 0.0);
        account.deactivate();
        assertThrows(IllegalStateException.class, () -> account.deposit(500.0));
    }

    // Kiểm tra withdraw giảm số dư khi đủ tiền
    @Test
    @DisplayName("TC-010: Verify withdraw decreases balance for sufficient funds and active account")
    void testWithdrawDecreasesBalance() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        account.withdraw(300.0);
        assertEquals(700.0, account.getBalance(), 0.001);
    }

    // Kiểm tra withdraw ném IllegalStateException cho số tiền vượt quá số dư
    @Test
    @DisplayName("TC-011: Verify withdraw throws exception for insufficient funds")
    void testWithdrawInsufficientFunds() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertThrows(IllegalStateException.class, () -> account.withdraw(1500.0));
    }

    // Kiểm tra withdraw ném IllegalArgumentException cho số tiền âm
    @Test
    @DisplayName("TC-012: Verify withdraw throws exception for negative amount")
    void testWithdrawNegativeAmount() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(-100.0));
    }

    // Kiểm tra withdraw ném IllegalStateException khi tài khoản không hoạt động
    @Test
    @DisplayName("TC-013: Verify withdraw throws exception when account is inactive")
    void testWithdrawInactiveAccount() {
        BankAccount account = new BankAccount("ACC123", 0.0);
        account.deactivate();
        assertThrows(IllegalStateException.class, () -> account.withdraw(100.0));
    }

    // Kiểm tra transfer chuyển tiền giữa hai tài khoản đang hoạt động
    @Test
    @DisplayName("TC-014: Verify transfer moves funds between active accounts")
    void testTransferBetweenActiveAccounts() {
        BankAccount source = new BankAccount("ACC123", 1000.0);
        BankAccount target = new BankAccount("ACC456", 500.0);
        source.transfer(target, 200.0);
        assertEquals(800.0, source.getBalance(), 0.001);
        assertEquals(700.0, target.getBalance(), 0.001);
    }

    // Kiểm tra transfer ném IllegalStateException khi tài khoản nguồn không hoạt động
    @Test
    @DisplayName("TC-015: Verify transfer throws exception when source account is inactive")
    void testTransferInactiveSource() {
        BankAccount source = new BankAccount("ACC123", 0.0);
        source.deactivate();
        BankAccount target = new BankAccount("ACC456", 500.0);
        assertThrows(IllegalStateException.class, () -> source.transfer(target, 200.0));
    }

    // Kiểm tra transfer ném IllegalStateException khi tài khoản đích không hoạt động
    @Test
    @DisplayName("TC-016: Verify transfer throws exception when target account is inactive")
    void testTransferInactiveTarget() {
        BankAccount source = new BankAccount("ACC123", 1000.0);
        BankAccount target = new BankAccount("ACC456", 0.0);
        target.deactivate();
        assertThrows(IllegalStateException.class, () -> source.transfer(target, 200.0));
    }

    // Kiểm tra constructor xử lý số dư ban đầu bằng 0
    @Test
    @DisplayName("TC-017: Verify constructor handles zero initial balance")
    void testConstructorZeroBalance() {
        BankAccount account = new BankAccount("ACC001", 0.0);
        assertEquals(0.0, account.getBalance(), 0.001);
        assertTrue(account.isActive());
    }

    // Kiểm tra constructor ném IllegalArgumentException cho số dư âm
    @Test
    @DisplayName("TC-018: Verify constructor throws exception for negative initial balance")
    void testConstructorNegativeBalance() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("ACC001", -100.0));
    }

    // Kiểm tra constructor ném IllegalArgumentException cho accountNumber rỗng
    @Test
    @DisplayName("TC-019: Verify constructor throws exception for empty account number")
    void testConstructorEmptyAccountNumber() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("", 1000.0));
    }

    // Kiểm tra constructor ném IllegalArgumentException cho accountNumber null
    @Test
    @DisplayName("TC-020: Verify constructor throws exception for null account number")
    void testConstructorNullAccountNumber() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount(null, 1000.0));
    }

    // Kiểm tra deactivate ném IllegalStateException khi số dư > 0
    @Test
    @DisplayName("TC-021: Verify deactivate throws exception when balance is non-zero")
    void testDeactivateNonZeroBalance() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertThrows(IllegalStateException.class, () -> account.deactivate());
    }

    // Kiểm tra transfer ném IllegalArgumentException cho target account null
    @Test
    @DisplayName("TC-022: Verify transfer throws exception for null target account")
    void testTransferNullTarget() {
        BankAccount source = new BankAccount("ACC123", 1000.0);
        assertThrows(IllegalArgumentException.class, () -> source.transfer(null, 200.0));
    }

    // Kiểm tra transfer ném IllegalArgumentException cho số tiền <= 0
    @Test
    @DisplayName("TC-023: Verify transfer throws exception for non-positive amount")
    void testTransferNonPositiveAmount() {
        BankAccount source = new BankAccount("ACC123", 1000.0);
        BankAccount target = new BankAccount("ACC456", 500.0);
        assertThrows(IllegalArgumentException.class, () -> source.transfer(target, 0.0));
    }
}
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

public class BankAccountTest {

    @Test
    void test_getAccountNumber_returns_initialized_value() {
        // Kiểm tra getAccountNumber() trả về accountNumber đã khởi tạo
        BankAccount account = new BankAccount("ACC123", 100.0);
        assertEquals("ACC123", account.getAccountNumber());
    }

    @Test
    void test_getBalance_returns_initialized_value() {
        // Kiểm tra getBalance() trả về số dư đã khởi tạo
        BankAccount account = new BankAccount("ACC123", 500.0);
        assertEquals(500.0, account.getBalance(), 0.001);
    }

    @Test
    void test_isActive_returns_true_when_account_is_active() {
        // Kiểm tra isActive() trả về true khi tài khoản đang hoạt động
        BankAccount account = new BankAccount("ACC123", 100.0);
        assertTrue(account.isActive());
    }

    @Test
    void test_deposit_throws_IllegalStateException_when_account_inactive() {
        // Kiểm tra deposit() ném IllegalStateException khi tài khoản không hoạt động
        BankAccount account = new BankAccount("ACC123", 0.0);
        account.deactivate();
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> account.deposit(100.0));
        assertEquals("Account is inactive", exception.getMessage());
    }

    @Test
    void test_withdraw_throws_IllegalStateException_when_account_inactive() {
        // Kiểm tra withdraw() ném IllegalStateException khi tài khoản không hoạt động
        BankAccount account = new BankAccount("ACC123", 0.0);
        account.deactivate();
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> account.withdraw(50.0));
        assertEquals("Account is inactive", exception.getMessage());
    }

    @Test
    void test_transfer_throws_IllegalStateException_when_target_account_inactive() {
        // Kiểm tra transfer() ném IllegalStateException khi tài khoản đích không hoạt động
        BankAccount source = new BankAccount("SRC123", 200.0);
        BankAccount target = new BankAccount("TGT123", 0.0);
        target.deactivate();
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> source.transfer(target, 50.0));
        assertEquals("Target account is inactive", exception.getMessage());
    }

    @Test
    void test_transfer_throws_IllegalArgumentException_when_target_account_null() {
        // Kiểm tra transfer() ném IllegalArgumentException khi tài khoản đích là null
        BankAccount source = new BankAccount("SRC123", 200.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> source.transfer(null, 50.0));
        assertEquals("Target account cannot be null", exception.getMessage());
    }

    @Test
    void test_deposit_throws_IllegalArgumentException_for_zero_amount() {
        // Kiểm tra deposit() ném IllegalArgumentException khi số tiền bằng không
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> account.deposit(0.0));
        assertEquals("Deposit amount must be positive", exception.getMessage());
    }

    @Test
    void test_withdraw_throws_IllegalArgumentException_for_negative_amount() {
        // Kiểm tra withdraw() ném IllegalArgumentException khi số tiền âm
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> account.withdraw(-10.0));
        assertEquals("Withdraw amount must be positive", exception.getMessage());
    }

    @Test
    void test_withdraw_throws_IllegalStateException_when_insufficient_funds() {
        // Kiểm tra withdraw() ném IllegalStateException khi số dư không đủ
        BankAccount account = new BankAccount("ACC123", 30.0);
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> account.withdraw(50.0));
        assertEquals("Insufficient funds", exception.getMessage());
    }

    @Test
    void test_deactivate_succeeds_when_balance_is_zero() {
        // Kiểm tra deactivate() thành công khi số dư bằng không
        BankAccount account = new BankAccount("ACC123", 0.0);
        account.deactivate();
        assertFalse(account.isActive());
    }

    @Test
    void test_deactivate_throws_IllegalStateException_when_balance_non_zero() {
        // Kiểm tra deactivate() ném IllegalStateException khi số dư khác không
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalStateException exception = assertThrows(IllegalStateException.class, () -> account.deactivate());
        assertEquals("Cannot deactivate account with non-zero balance", exception.getMessage());
    }


    // ===== Targeted retry tests =====

@Test
    void retry_2_constructor_throws_for_null_account_number() {
        // Kiểm tra constructor ném IllegalArgumentException khi accountNumber là null
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> new BankAccount(null, 100.0));
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    @Test
    void retry_2_constructor_throws_for_empty_account_number() {
        // Kiểm tra constructor ném IllegalArgumentException khi accountNumber rỗng
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> new BankAccount("", 100.0));
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    @Test
    void retry_2_constructor_throws_for_whitespace_account_number() {
        // Kiểm tra constructor ném IllegalArgumentException khi accountNumber chỉ chứa khoảng trắng
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> new BankAccount("   ", 100.0));
        assertEquals("Account number cannot be empty", exception.getMessage());
    }

    @Test
    void retry_2_constructor_throws_for_negative_initial_balance() {
        // Kiểm tra constructor ném IllegalArgumentException khi initialBalance âm
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> new BankAccount("ACC123", -50.0));
        assertEquals("Initial balance cannot be negative", exception.getMessage());
    }

    @Test
    void retry_2_deposit_increases_balance() {
        // Kiểm tra deposit() tăng số dư khi số tiền hợp lệ
        BankAccount account = new BankAccount("ACC123", 100.0);
        account.deposit(50.0);
        assertEquals(150.0, account.getBalance(), 0.001);
    }

    @Test
    void retry_2_withdraw_decreases_balance() {
        // Kiểm tra withdraw() giảm số dư khi số tiền hợp lệ
        BankAccount account = new BankAccount("ACC123", 100.0);
        account.withdraw(30.0);
        assertEquals(70.0, account.getBalance(), 0.001);
    }

    @Test
    void retry_2_transfer_succeeds_between_active_accounts() {
        // Kiểm tra transfer() chuyển tiền thành công giữa hai tài khoản hoạt động
        BankAccount source = new BankAccount("SRC123", 200.0);
        BankAccount target = new BankAccount("TGT123", 50.0);
        source.transfer(target, 75.0);
        assertEquals(125.0, source.getBalance(), 0.001);
        assertEquals(125.0, target.getBalance(), 0.001);
    }

    @Test
    void retry_2_withdraw_throws_IllegalArgumentException_for_zero_amount() {
        // Kiểm tra withdraw() ném IllegalArgumentException khi số tiền bằng không
        BankAccount account = new BankAccount("ACC123", 100.0);
        IllegalArgumentException exception = assertThrows(IllegalArgumentException.class, () -> account.withdraw(0.0));
        assertEquals("Withdraw amount must be positive", exception.getMessage());
    }
}
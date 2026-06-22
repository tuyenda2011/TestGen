import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class BankAccountTest {

    // TC-001: Tạo tài khoản hợp lệ với số dư ban đầu bằng 0
    @Test
    void testCreateAccountWithZeroBalance() {
        BankAccount account = new BankAccount("ACC12345", 0.0);
        assertEquals("ACC12345", account.getAccountNumber(), "Số tài khoản phải khớp");
        assertTrue(account.isActive(), "Tài khoản mới phải ở trạng thái active");
        assertEquals(0.0, account.getBalance(), 0.0001, "Số dư phải bằng 0");
    }

    // TC-002: Tạo tài khoản hợp lệ với số dư dương
    @Test
    void testCreateAccountWithPositiveBalance() {
        BankAccount account = new BankAccount("ACC98765", 1500.75);
        assertEquals("ACC98765", account.getAccountNumber());
        assertTrue(account.isActive());
        assertEquals(1500.75, account.getBalance(), 0.0001);
    }

    // TC-003: Tạo tài khoản với accountNumber null -> ném IllegalArgumentException
    @Test
    void testCreateAccountNullNumberThrows() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount(null, 100.0));
    }

    // TC-004: Tạo tài khoản với accountNumber rỗng -> ném IllegalArgumentException
    @Test
    void testCreateAccountEmptyNumberThrows() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("", 100.0));
    }

    // TC-005: Tạo tài khoản với accountNumber chỉ chứa khoảng trắng -> ném IllegalArgumentException
    @Test
    void testCreateAccountWhitespaceNumberThrows() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("   ", 100.0));
    }

    // TC-006: Tạo tài khoản với số dư âm -> ném IllegalArgumentException
    @Test
    void testCreateAccountNegativeBalanceThrows() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("ACC001", -50.0));
    }

    // TC-007: Gửi tiền vào tài khoản đang hoạt động
    @Test
    void testDepositPositiveAmount() {
        BankAccount account = new BankAccount("ACC100", 200.0);
        account.deposit(150.0);
        assertEquals(350.0, account.getBalance(), 0.0001);
    }

    // TC-008: Gửi tiền 0 -> ném IllegalArgumentException
    @Test
    void testDepositZeroAmountThrows() {
        BankAccount account = new BankAccount("ACC101", 100.0);
        assertThrows(IllegalArgumentException.class, () -> account.deposit(0.0));
    }

    // TC-009: Gửi tiền âm -> ném IllegalArgumentException
    @Test
    void testDepositNegativeAmountThrows() {
        BankAccount account = new BankAccount("ACC102", 100.0);
        assertThrows(IllegalArgumentException.class, () -> account.deposit(-20.0));
    }

    // TC-010: Rút tiền hợp lệ
    @Test
    void testWithdrawValidAmount() {
        BankAccount account = new BankAccount("ACC200", 500.0);
        account.withdraw(200.0);
        assertEquals(300.0, account.getBalance(), 0.0001);
    }

    // TC-011: Rút tiền bằng toàn bộ số dư
    @Test
    void testWithdrawExactBalance() {
        BankAccount account = new BankAccount("ACC201", 250.0);
        account.withdraw(250.0);
        assertEquals(0.0, account.getBalance(), 0.0001);
    }

    // TC-012: Rút tiền 0 -> ném IllegalArgumentException
    @Test
    void testWithdrawZeroAmountThrows() {
        BankAccount account = new BankAccount("ACC202", 100.0);
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(0.0));
    }

    // TC-013: Rút tiền âm -> ném IllegalArgumentException
    @Test
    void testWithdrawNegativeAmountThrows() {
        BankAccount account = new BankAccount("ACC203", 100.0);
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(-30.0));
    }

    // TC-014: Rút tiền vượt quá số dư -> ném IllegalStateException
    @Test
    void testWithdrawExceedBalanceThrows() {
        BankAccount account = new BankAccount("ACC204", 80.0);
        assertThrows(IllegalStateException.class, () -> account.withdraw(100.0));
    }

    // TC-015: Chuyển tiền hợp lệ giữa hai tài khoản hoạt động
    @Test
    void testTransferValid() {
        BankAccount source = new BankAccount("ACC300", 400.0);
        BankAccount target = new BankAccount("ACC301", 150.0);
        source.transfer(target, 200.0);
        assertEquals(200.0, source.getBalance(), 0.0001);
        assertEquals(350.0, target.getBalance(), 0.0001);
    }

    // TC-016: Chuyển tiền tới tài khoản null -> ném IllegalArgumentException
    @Test
    void testTransferToNullTargetThrows() {
        BankAccount source = new BankAccount("ACC302", 300.0);
        assertThrows(IllegalArgumentException.class, () -> source.transfer(null, 50.0));
    }

    // TC-017: Chuyển tiền tới tài khoản không hoạt động -> ném IllegalStateException
    @Test
    void testTransferToInactiveTargetThrows() {
        BankAccount source = new BankAccount("ACC303", 300.0);
        BankAccount target = new BankAccount("ACC304", 0.0); // zero balance to allow deactivation
        target.deactivate(); // làm cho target không hoạt động
        assertThrows(IllegalStateException.class, () -> source.transfer(target, 50.0));
    }

    // TC-018: Chuyển tiền số 0 -> ném IllegalArgumentException (do withdraw kiểm tra)
    @Test
    void testTransferZeroAmountThrows() {
        BankAccount source = new BankAccount("ACC305", 200.0);
        BankAccount target = new BankAccount("ACC306", 100.0);
        assertThrows(IllegalArgumentException.class, () -> source.transfer(target, 0.0));
    }

    // TC-019: Hủy tài khoản khi còn số dư > 0 -> ném IllegalStateException
    @Test
    void testDeactivateWithNonZeroBalanceThrows() {
        BankAccount account = new BankAccount("ACC400", 50.0);
        assertThrows(IllegalStateException.class, account::deactivate);
    }

    // TC-020: Hủy tài khoản khi số dư = 0 -> thành công và isActive = false
    @Test
    void testDeactivateWithZeroBalance() {
        BankAccount account = new BankAccount("ACC401", 0.0);
        account.deactivate();
        assertFalse(account.isActive(), "Tài khoản sau khi hủy phải không còn active");
    }

    // TC-021: Gửi tiền vào tài khoản đã hủy -> ném IllegalStateException
    @Test
    void testDepositOnInactiveAccountThrows() {
        BankAccount account = new BankAccount("ACC500", 0.0);
        account.deactivate();
        assertThrows(IllegalStateException.class, () -> account.deposit(100.0));
    }

    // TC-022: Rút tiền từ tài khoản đã hủy -> ném IllegalStateException
    @Test
    void testWithdrawOnInactiveAccountThrows() {
        BankAccount account = new BankAccount("ACC501", 0.0);
        account.deactivate();
        assertThrows(IllegalStateException.class, () -> account.withdraw(10.0));
    }
}
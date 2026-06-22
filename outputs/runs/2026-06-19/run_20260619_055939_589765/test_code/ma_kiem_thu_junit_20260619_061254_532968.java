import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.function.Executable;
import java.lang.reflect.Method;
import java.lang.reflect.InvocationTargetException;

import static org.junit.jupiter.api.Assertions.*;

public class BankAccountTest {

    /** 
     * Tạo một tài khoản với trạng thái hoạt động hoặc không hoạt động tùy ý.
     * Giúp giảm lặp mã trong các test cần khởi tạo đối tượng.
     */
    private BankAccount createAccount(String number, double balance, boolean active) {
        BankAccount account = new BankAccount(number, balance);
        if (!active) {
            // Đặt trạng thái không hoạt động bằng cách gọi checkActive() thông qua reflection
            // để tránh thay đổi mức truy cập của phương thức trong lớp sản phẩm.
            try {
                Method checkActive = BankAccount.class.getDeclaredMethod("checkActive");
                checkActive.setAccessible(true);
                // Không thực hiện gì, chỉ để thay đổi trạng thái nếu cần (không có cách khác)
            } catch (NoSuchMethodException e) {
                // Không xảy ra vì phương thức tồn tại
            }
            // Để tài khoản không hoạt động, gọi deactivate() khi balance = 0
            if (balance == 0) {
                account.deactivate();
            } else {
                // Nếu balance > 0, giảm về 0 rồi deactivate()
                account.withdraw(balance);
                account.deactivate();
            }
        }
        return account;
    }

    // TC-001: Kiểm tra tạo tài khoản hợp lệ và các getter trả về giá trị đúng
    @Test
    void testCreateAccountValid_TC001() {
        BankAccount account = new BankAccount("ACC123", 1000.0);
        assertEquals("ACC123", account.getAccountNumber());
        assertEquals(1000.0, account.getBalance(), 0.001);
        assertTrue(account.isActive());
    }

    // TC-002: Kiểm tra constructor ném IllegalArgumentException khi accountNumber null
    @Test
    void testConstructorNullAccountNumber_TC002() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> new BankAccount(null, 500.0));
        assertEquals("Account number cannot be empty", ex.getMessage());
    }

    // TC-003: Kiểm tra constructor ném IllegalArgumentException khi accountNumber rỗng
    @Test
    void testConstructorBlankAccountNumber_TC003() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> new BankAccount("   ", 500.0));
        assertEquals("Account number cannot be empty", ex.getMessage());
    }

    // TC-004: Kiểm tra constructor ném IllegalArgumentException khi balance âm
    @Test
    void testConstructorNegativeBalance_TC004() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> new BankAccount("ACC124", -10.0));
        assertEquals("Initial balance cannot be negative", ex.getMessage());
    }

    // TC-005: Kiểm tra deposit số tiền dương cập nhật balance
    @Test
    void testDepositPositiveAmount_TC005() {
        BankAccount account = new BankAccount("ACC200", 200.0);
        account.deposit(150.0);
        assertEquals(350.0, account.getBalance(), 0.001);
    }

    // TC-006: Kiểm tra deposit ném IllegalArgumentException khi amount <= 0
    @Test
    void testDepositNonPositiveAmount_TC006() {
        BankAccount account = new BankAccount("ACC201", 200.0);
        IllegalArgumentException exZero = assertThrows(IllegalArgumentException.class,
                () -> account.deposit(0.0));
        assertEquals("Deposit amount must be positive", exZero.getMessage());

        IllegalArgumentException exNeg = assertThrows(IllegalArgumentException.class,
                () -> account.deposit(-5.0));
        assertEquals("Deposit amount must be positive", exNeg.getMessage());
    }

    // TC-007: Kiểm tra withdraw ném IllegalArgumentException khi amount âm
    @Test
    void testWithdrawNegativeAmount_TC007() {
        BankAccount account = new BankAccount("ACC300", 300.0);
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> account.withdraw(-50.0));
        assertEquals("Withdraw amount must be positive", ex.getMessage());
    }

    // TC-008: Kiểm tra withdraw ném IllegalStateException khi số tiền vượt quá balance
    @Test
    void testWithdrawExceedsBalance_TC008() {
        BankAccount account = new BankAccount("ACC301", 100.0);
        IllegalStateException ex = assertThrows(IllegalStateException.class,
                () -> account.withdraw(150.0));
        assertEquals("Insufficient funds", ex.getMessage());
    }

    // TC-009: Kiểm tra withdraw hợp lệ giảm balance
    @Test
    void testWithdrawValidAmount_TC009() {
        BankAccount account = new BankAccount("ACC302", 500.0);
        account.withdraw(200.0);
        assertEquals(300.0, account.getBalance(), 0.001);
    }

    // TC-010: Kiểm tra transfer thành công giữa hai tài khoản hoạt động và đủ tiền
    @Test
    void testTransferSuccessful_TC010() {
        BankAccount source = new BankAccount("SRC", 400.0);
        BankAccount target = new BankAccount("TGT", 100.0);
        source.transfer(target, 150.0);
        assertEquals(250.0, source.getBalance(), 0.001);
        assertEquals(250.0, target.getBalance(), 0.001);
    }

    // TC-011: Kiểm tra transfer ném IllegalArgumentException khi targetAccount null
    @Test
    void testTransferNullTarget_TC011() {
        BankAccount source = new BankAccount("SRC2", 400.0);
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> source.transfer(null, 50.0));
        assertEquals("Target account cannot be null", ex.getMessage());
    }

    // TC-012: Kiểm tra transfer ném IllegalStateException khi targetAccount không hoạt động
    @Test
    void testTransferInactiveTarget_TC012() {
        BankAccount source = new BankAccount("SRC3", 400.0);
        BankAccount inactiveTarget = createAccount("TGT2", 0.0, false);
        IllegalStateException ex = assertThrows(IllegalStateException.class,
                () -> source.transfer(inactiveTarget, 50.0));
        assertEquals("Target account is inactive", ex.getMessage());
    }

    // TC-013: Kiểm tra deactivate tài khoản có số dư 0 thành công
    @Test
    void testDeactivateZeroBalance_TC013() {
        BankAccount account = createAccount("ACC_DEACT", 0.0, true);
        assertDoesNotThrow(account::deactivate);
        assertFalse(account.isActive());
    }

    // TC-014: Kiểm tra deactivate ném IllegalStateException khi balance > 0
    @Test
    void testDeactivateNonZeroBalance_TC014() {
        BankAccount account = new BankAccount("ACC_DEACT2", 10.0);
        IllegalStateException ex = assertThrows(IllegalStateException.class,
                account::deactivate);
        assertEquals("Cannot deactivate account with non-zero balance", ex.getMessage());
    }

    // TC-015: Kiểm tra checkActive không ném khi tài khoản đang hoạt động
    @Test
    void testCheckActiveWhenActive_TC015() throws Exception {
        BankAccount account = new BankAccount("ACC_ACT", 100.0);
        Method checkActive = BankAccount.class.getDeclaredMethod("checkActive");
        checkActive.setAccessible(true);
        assertDoesNotThrow(() -> checkActive.invoke(account));
    }

    // TC-016: Kiểm tra checkActive ném IllegalStateException khi tài khoản không hoạt động
    @Test
    void testCheckActiveWhenInactive_TC016() throws Exception {
        BankAccount account = createAccount("ACC_INACT", 0.0, false);
        Method checkActive = BankAccount.class.getDeclaredMethod("checkActive");
        checkActive.setAccessible(true);
        InvocationTargetException ex = assertThrows(InvocationTargetException.class,
                () -> checkActive.invoke(account));
        assertTrue(ex.getCause() instanceof IllegalStateException);
        assertEquals("Account is inactive", ex.getCause().getMessage());
    }
}
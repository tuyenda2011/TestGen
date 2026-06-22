import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BankAccountTest {

    /** Kiểm tra tạo tài khoản hợp lệ, trả về các giá trị khởi tạo đúng */
    @Test
    void testCreateAccountValid() {
        BankAccount account = new BankAccount("ACC123", 100.0);
        assertEquals("ACC123", account.getAccountNumber());
        assertEquals(100.0, account.getBalance(), 0.001);
        assertTrue(account.isActive());
    }

    /** Kiểm tra constructor ném IllegalArgumentException khi accountNumber null */
    @Test
    void testConstructorNullAccountNumber() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount(null, 50.0));
    }

    /** Kiểm tra constructor ném IllegalArgumentException khi accountNumber rỗng */
    @Test
    void testConstructorEmptyAccountNumber() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("   ", 50.0));
    }

    /** Kiểm tra constructor ném IllegalArgumentException khi số dư ban đầu âm */
    @Test
    void testConstructorNegativeInitialBalance() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("ACC124", -10.0));
    }

    /** Nạp tiền dương vào tài khoản đang hoạt động, số dư tăng đúng */
    @Test
    void testDepositPositiveAmount() {
        BankAccount account = new BankAccount("ACC200", 100.0);
        account.deposit(50.0);
        assertEquals(150.0, account.getBalance(), 0.001);
    }

    /** Nạp tiền không dương (0) vào tài khoản, ném IllegalArgumentException */
    @Test
    void testDepositZeroOrNegativeAmount() {
        BankAccount account = new BankAccount("ACC201", 100.0);
        assertThrows(IllegalArgumentException.class, () -> account.deposit(0.0));
    }

    /** Nạp tiền vào tài khoản không hoạt động, ném IllegalStateException */
    @Test
    void testDepositIntoInactiveAccount() {
        BankAccount account = new BankAccount("ACC202", 0.0); // balance zero to allow deactivation
        account.deactivate();
        assertThrows(IllegalStateException.class, () -> account.deposit(20.0));
    }

    /** Rút tiền hợp lệ từ tài khoản hoạt động, số dư giảm đúng */
    @Test
    void testWithdrawValidAmount() {
        BankAccount account = new BankAccount("ACC300", 200.0);
        account.withdraw(80.0);
        assertEquals(120.0, account.getBalance(), 0.001);
    }

    /** Rút tiền vượt quá số dư, ném IllegalStateException */
    @Test
    void testWithdrawInsufficientFunds() {
        BankAccount account = new BankAccount("ACC301", 50.0);
        assertThrows(IllegalStateException.class, () -> account.withdraw(75.0));
    }

    /** Rút tiền không dương, ném IllegalArgumentException */
    @Test
    void testWithdrawZeroOrNegativeAmount() {
        BankAccount account = new BankAccount("ACC302", 100.0);
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(-10.0));
    }

    /** Rút tiền từ tài khoản không hoạt động, ném IllegalStateException */
    @Test
    void testWithdrawFromInactiveAccount() {
        BankAccount account = new BankAccount("ACC303", 0.0);
        account.deactivate();
        assertThrows(IllegalStateException.class, () -> account.withdraw(30.0));
    }

    /** Chuyển tiền hợp lệ giữa hai tài khoản hoạt động */
    @Test
    void testTransferValid() {
        BankAccount source = new BankAccount("SRC", 200.0);
        BankAccount target = new BankAccount("TGT", 50.0);
        source.transfer(target, 70.0);
        assertEquals(130.0, source.getBalance(), 0.001);
        assertEquals(120.0, target.getBalance(), 0.001);
    }

    /** Chuyển tiền tới tài khoản null, ném IllegalArgumentException */
    @Test
    void testTransferToNullTarget() {
        BankAccount source = new BankAccount("SRC2", 100.0);
        assertThrows(IllegalArgumentException.class, () -> source.transfer(null, 30.0));
    }

    /** Chuyển tiền tới tài khoản không hoạt động, ném IllegalStateException */
    @Test
    void testTransferToInactiveTarget() {
        BankAccount source = new BankAccount("SRC3", 100.0);
        BankAccount target = new BankAccount("TGT2", 0.0);
        target.deactivate();
        assertThrows(IllegalStateException.class, () -> source.transfer(target, 40.0));
    }

    /** Chuyển tiền vượt quá số dư nguồn, ném IllegalStateException */
    @Test
    void testTransferInsufficientFunds() {
        BankAccount source = new BankAccount("SRC4", 30.0);
        BankAccount target = new BankAccount("TGT3", 10.0);
        assertThrows(IllegalStateException.class, () -> source.transfer(target, 50.0));
    }

    /** Deactivate tài khoản có số dư khác 0, ném IllegalStateException */
    @Test
    void testDeactivateWithNonZeroBalance() {
        BankAccount account = new BankAccount("ACC400", 10.0);
        assertThrows(IllegalStateException.class, account::deactivate);
    }

    /** Deactivate tài khoản có số dư 0, thành công và isActive trả về false */
    @Test
    void testDeactivateWithZeroBalance() {
        BankAccount account = new BankAccount("ACC401", 0.0);
        account.deactivate();
        assertFalse(account.isActive());
    }

    /** Gọi getBalance trên tài khoản không hoạt động, trả về số dư hiện tại */
    @Test
    void testGetBalanceOnInactiveAccount() {
        BankAccount account = new BankAccount("ACC500", 0.0);
        account.deactivate();
        assertEquals(0.0, account.getBalance(), 0.001);
    }

    /** Kiểm tra các getter trên tài khoản hoạt động */
    @Test
    void testRetrieveAccountInfo() {
        BankAccount account = new BankAccount("ACC999", 250.0);
        assertEquals("ACC999", account.getAccountNumber());
        assertTrue(account.isActive());
        assertEquals(250.0, account.getBalance(), 0.001);
    }
}
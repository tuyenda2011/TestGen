import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BankAccountTest {

    // TC-001: Kiểm tra tạo tài khoản hợp lệ và các getter trả về giá trị đúng
    @Test
    void testCreateAccountValid_TC_001() {
        BankAccount account = new BankAccount("ACC12345", 100.0);
        assertEquals("ACC12345", account.getAccountNumber(), "Số tài khoản phải khớp");
        assertEquals(100.0, account.getBalance(), 0.001, "Số dư phải khớp");
    }

    // TC-002: Kiểm tra constructor ném IllegalArgumentException khi accountNumber null
    @Test
    void testConstructorNullAccountNumber_TC_002() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount(null, 50.0));
    }

    // TC-003: Kiểm tra constructor ném IllegalArgumentException khi accountNumber rỗng
    @Test
    void testConstructorBlankAccountNumber_TC_003() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("   ", 50.0));
    }

    // TC-004: Kiểm tra constructor ném IllegalArgumentException khi balance âm
    @Test
    void testConstructorNegativeBalance_TC_004() {
        assertThrows(IllegalArgumentException.class, () -> new BankAccount("ACC9876", -10.0));
    }

    // TC-005: Nạp tiền vào tài khoản đang hoạt động
    @Test
    void testDepositPositiveAmountActiveAccount_TC_005() {
        BankAccount account = new BankAccount("ACC001", 100.0);
        account.deposit(50.0);
        assertEquals(150.0, account.getBalance(), 0.001, "Số dư sau khi nạp phải tăng");
    }

    // TC-006: Nạp tiền với số tiền không dương
    @Test
    void testDepositNonPositiveAmount_TC_006() {
        BankAccount account = new BankAccount("ACC002", 100.0);
        assertThrows(IllegalArgumentException.class, () -> account.deposit(0.0));
        assertThrows(IllegalArgumentException.class, () -> account.deposit(-5.0));
    }

    // TC-007: Nạp tiền khi tài khoản không hoạt động
    @Test
    void testDepositWhenInactive_TC_007() {
        BankAccount account = new BankAccount("ACC003", 100.0);
        // Deactivate account (balance must be zero, nên withdraw hết)
        account.withdraw(100.0);
        account.deactivate();
        assertFalse(account.isActive(), "Tài khoản phải không hoạt động");
        assertThrows(IllegalStateException.class, () -> account.deposit(20.0));
    }

    // TC-008: Rút tiền hợp lệ từ tài khoản hoạt động
    @Test
    void testWithdrawValidAmountActiveAccount_TC_008() {
        BankAccount account = new BankAccount("ACC004", 200.0);
        account.withdraw(80.0);
        assertEquals(120.0, account.getBalance(), 0.001, "Số dư sau khi rút phải giảm");
    }

    // TC-009: Rút tiền với số tiền âm
    @Test
    void testWithdrawNegativeAmount_TC_009() {
        BankAccount account = new BankAccount("ACC005", 200.0);
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(-10.0));
    }

    // TC-010: Rút tiền khi không đủ số dư
    @Test
    void testWithdrawInsufficientFunds_TC_010() {
        BankAccount account = new BankAccount("ACC006", 50.0);
        assertThrows(IllegalStateException.class, () -> account.withdraw(75.0));
    }

    // TC-011: Rút tiền khi tài khoản không hoạt động
    @Test
    void testWithdrawWhenInactive_TC_011() {
        BankAccount account = new BankAccount("ACC007", 100.0);
        account.withdraw(100.0);
        account.deactivate();
        assertThrows(IllegalStateException.class, () -> account.withdraw(30.0));
    }

    // TC-012: Chuyển tiền giữa hai tài khoản hoạt động
    @Test
    void testTransferBetweenActiveAccounts_TC_012() {
        BankAccount source = new BankAccount("SRC001", 200.0);
        BankAccount target = new BankAccount("TGT001", 50.0);
        source.transfer(target, 70.0);
        assertEquals(130.0, source.getBalance(), 0.001, "Số dư nguồn sau chuyển phải giảm");
        assertEquals(120.0, target.getBalance(), 0.001, "Số dư đích sau chuyển phải tăng");
    }

    // TC-013: Chuyển tiền khi tài khoản đích null
    @Test
    void testTransferToNullTarget_TC_013() {
        BankAccount source = new BankAccount("SRC002", 200.0);
        assertThrows(IllegalArgumentException.class, () -> source.transfer(null, 30.0));
    }

    // TC-014: Chuyển tiền khi tài khoản đích không hoạt động
    @Test
    void testTransferToInactiveTarget_TC_014() {
        BankAccount source = new BankAccount("SRC003", 200.0);
        BankAccount inactiveTarget = new BankAccount("TGT002", 50.0);
        // Đánh dấu tài khoản đích không hoạt động
        inactiveTarget.withdraw(50.0);
        inactiveTarget.deactivate();
        assertThrows(IllegalStateException.class, () -> source.transfer(inactiveTarget, 30.0));
    }

    // TC-015: Chuyển tiền khi tài khoản nguồn không hoạt động
    @Test
    void testTransferFromInactiveSource_TC_015() {
        BankAccount source = new BankAccount("SRC004", 200.0);
        BankAccount target = new BankAccount("TGT003", 50.0);
        // Đánh dấu tài khoản nguồn không hoạt động
        source.withdraw(200.0);
        source.deactivate();
        assertThrows(IllegalStateException.class, () -> source.transfer(target, 30.0));
    }
}
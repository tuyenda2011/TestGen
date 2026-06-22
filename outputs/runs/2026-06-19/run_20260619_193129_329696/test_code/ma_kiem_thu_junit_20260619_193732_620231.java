// Plan: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013, TC-014, TC-015
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class BankAccountTest {

    // TC-001: Create BankAccount with valid account number and non‑negative balance
    @Test
    void testCreateBankAccountValid_TC001() {
        // Kiểm tra tạo tài khoản hợp lệ và các getter trả về giá trị đúng
        BankAccount account = new BankAccount("ACC123", 100.0);
        assertEquals("ACC123", account.getAccountNumber(), "Số tài khoản phải khớp");
        assertEquals(100.0, account.getBalance(), 0.001, "Số dư phải khớp");
        assertTrue(account.isActive(), "Tài khoản phải ở trạng thái active");
    }

    // TC-002: Constructor throws when account number is null
    @Test
    void testConstructorNullAccountNumber_TC002() {
        // Kiểm tra ném IllegalArgumentException khi accountNumber null
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> new BankAccount(null, 50.0));
        assertEquals("Account number cannot be empty", ex.getMessage(),
                "Thông báo lỗi phải đúng khi accountNumber null");
    }

    // TC-003: Constructor throws when account number is blank
    @Test
    void testConstructorBlankAccountNumber_TC003() {
        // Kiểm tra ném IllegalArgumentException khi accountNumber chỉ chứa khoảng trắng
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> new BankAccount("   ", 50.0));
        assertEquals("Account number cannot be empty", ex.getMessage(),
                "Thông báo lỗi phải đúng khi accountNumber blank");
    }

    // TC-004: Constructor throws when initial balance is negative
    @Test
    void testConstructorNegativeBalance_TC004() {
        // Kiểm tra ném IllegalArgumentException khi initialBalance < 0
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> new BankAccount("ACC124", -10.0));
        assertEquals("Initial balance cannot be negative", ex.getMessage(),
                "Thông báo lỗi phải đúng khi balance âm");
    }

    // TC-005: Deposit positive amount updates balance
    @Test
    void testDepositPositiveAmount_TC005() {
        // Kiểm tra nạp tiền thành công và cập nhật số dư
        BankAccount account = new BankAccount("ACC001", 100.0);
        account.deposit(50.0);
        assertEquals(150.0, account.getBalance(), 0.001, "Số dư sau khi nạp phải tăng");
    }

    // TC-006: Deposit throws when amount is zero or negative
    @Test
    void testDepositZeroOrNegative_TC006() {
        // Kiểm tra nạp tiền với số tiền không dương gây IllegalArgumentException
        BankAccount account = new BankAccount("ACC002", 100.0);
        assertThrows(IllegalArgumentException.class, () -> account.deposit(0.0));
        assertThrows(IllegalArgumentException.class, () -> account.deposit(-10.0));
    }

    // TC-007: Withdraw valid amount reduces balance
    @Test
    void testWithdrawValidAmount_TC007() {
        // Kiểm tra rút tiền hợp lệ và giảm số dư
        BankAccount account = new BankAccount("ACC003", 200.0);
        account.withdraw(80.0);
        assertEquals(120.0, account.getBalance(), 0.001, "Số dư sau khi rút phải giảm");
    }

    // TC-008: Withdraw throws when amount is negative
    @Test
    void testWithdrawNegativeAmount_TC008() {
        // Kiểm tra rút tiền với số tiền âm gây IllegalArgumentException
        BankAccount account = new BankAccount("ACC004", 200.0);
        assertThrows(IllegalArgumentException.class, () -> account.withdraw(-20.0));
    }

    // TC-009: Withdraw throws when amount exceeds balance
    @Test
    void testWithdrawExceedsBalance_TC009() {
        // Kiểm tra rút tiền vượt quá số dư gây IllegalStateException
        BankAccount account = new BankAccount("ACC005", 50.0);
        assertThrows(IllegalStateException.class, () -> account.withdraw(100.0));
    }

    // TC-010: Transfer to active target account moves funds
    @Test
    void testTransferToActiveTarget_TC010() {
        // Kiểm tra chuyển tiền giữa hai tài khoản hoạt động
        BankAccount source = new BankAccount("SRC001", 150.0);
        BankAccount target = new BankAccount("TGT001", 30.0);
        source.transfer(target, 50.0);
        assertEquals(100.0, source.getBalance(), 0.001, "Số dư nguồn sau chuyển phải giảm");
        assertEquals(80.0, target.getBalance(), 0.001, "Số dư đích sau chuyển phải tăng");
    }

    // TC-011: Transfer throws when target account is null
    @Test
    void testTransferNullTarget_TC011() {
        // Kiểm tra chuyển tiền khi tài khoản đích null gây IllegalArgumentException
        BankAccount source = new BankAccount("SRC002", 100.0);
        assertThrows(IllegalArgumentException.class, () -> source.transfer(null, 20.0));
    }

    // TC-012: Transfer throws when target account is inactive
    @Test
    void testTransferToInactiveTarget_TC012() {
        // Kiểm tra chuyển tiền tới tài khoản không hoạt động gây IllegalStateException
        BankAccount source = new BankAccount("SRC003", 100.0);
        BankAccount inactiveTarget = new BankAccount("TGT002", 0.0);
        inactiveTarget.deactivate(); // làm cho tài khoản đích không hoạt động
        assertThrows(IllegalStateException.class, () -> source.transfer(inactiveTarget, 10.0));
    }

    // TC-013: Deactivate throws when balance is non‑zero
    @Test
    void testDeactivateWithNonZeroBalance_TC013() {
        // Kiểm tra deactivate khi số dư > 0 gây IllegalStateException
        BankAccount account = new BankAccount("ACC006", 10.0);
        IllegalStateException ex = assertThrows(IllegalStateException.class, account::deactivate);
        assertEquals("Cannot deactivate account with non-zero balance", ex.getMessage(),
                "Thông báo lỗi phải đúng khi deactivate với số dư không zero");
    }

    // TC-014: Deactivate succeeds when balance is zero
    @Test
    void testDeactivateWhenZeroBalance_TC014() {
        // Kiểm tra deactivate thành công khi số dư = 0
        BankAccount account = new BankAccount("ACC007", 0.0);
        account.deactivate();
        assertFalse(account.isActive(), "Tài khoản phải không hoạt động sau deactivate");
    }

    // TC-015: checkActive throws when account is inactive
    @Test
    void testOperationOnInactiveAccountThrows_TC015() {
        // Kiểm tra rằng bất kỳ thao tác nào yêu cầu tài khoản active (deposit) sẽ ném IllegalStateException với thông điệp đúng
        BankAccount account = new BankAccount("ACC008", 0.0);
        account.deactivate();
        IllegalStateException ex = assertThrows(IllegalStateException.class, () -> account.deposit(10.0));
        assertEquals("Account is inactive", ex.getMessage(),
                "Thông báo lỗi phải đúng khi thực hiện thao tác trên tài khoản không active");
    }
}